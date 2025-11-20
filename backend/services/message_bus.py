"""
Message Bus Service
NATS-based message bus for inter-agent communication and orchestration

Author: Cavin Otieno
"""

import asyncio
import json
import uuid
import time
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import nats
from nats.js import JetStreamContext, Message
from nats.js.api import ConsumerConfig, StreamConfig, StorageType

from loguru import logger

from backend.core.config import settings


class MessageType(Enum):
    """Message types for different communication patterns"""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    BROADCAST = "broadcast"
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class Priority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MessageContent:
    """Message content with metadata"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None
    message_type: MessageType = MessageType.EVENT
    sender_id: Optional[str] = None
    recipient_id: Optional[str] = None
    subject: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: Priority = Priority.NORMAL
    expires_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "message_id": self.message_id,
            "correlation_id": self.correlation_id,
            "message_type": self.message_type.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "subject": self.subject,
            "payload": self.payload,
            "priority": self.priority.value,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageContent':
        """Create message from dictionary"""
        return cls(
            message_id=data["message_id"],
            correlation_id=data.get("correlation_id"),
            message_type=MessageType(data["message_type"]),
            sender_id=data.get("sender_id"),
            recipient_id=data.get("recipient_id"),
            subject=data.get("subject", ""),
            payload=data.get("payload", {}),
            priority=Priority(data.get("priority", Priority.NORMAL.value)),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            created_at=datetime.fromisoformat(data["created_at"])
        )


@dataclass
class MessageHandler:
    """Message handler configuration"""
    subject: str
    callback: Callable
    auto_ack: bool = True
    priority: Priority = Priority.NORMAL
    max_concurrent: int = 10
    handler_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class MessageBus:
    """
    Message Bus Service
    
    Provides robust message-based communication between agents and services:
    - Request/Response patterns
    - Event-driven communication
    - Task distribution and result collection
    - Broadcasting to multiple recipients
    - Message persistence and reliability
    """
    
    def __init__(self):
        self._nc: Optional[nats.NATS] = None
        self._js: Optional[JetStreamContext] = None
        self._running = False
        self._handlers: Dict[str, MessageHandler] = {}
        self._subscriptions: Dict[str, Any] = {}
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._message_counters = {
            "sent": 0,
            "received": 0,
            "failed": 0,
            "retried": 0
        }
        
        # Subject patterns
        self._subjects = {
            "events": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.events.*",
            "tasks": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.tasks.*",
            "responses": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.responses.*",
            "broadcasts": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.broadcasts.*",
            "heartbeats": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.heartbeats.*",
            "errors": f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.errors.*"
        }
        
        logger.info("📡 Message Bus initialized")
    
    async def start(self):
        """Start the message bus service"""
        try:
            # Connect to NATS
            self._nc = await nats.connect(
                settings.NATS_URL,
                allow_reconnect=True,
                max_reconnect_attempts=10,
                reconnect_time_wait=5,
                name=f"{settings.NATS_CLIENT_ID}-message-bus"
            )
            
            # Initialize JetStream
            if settings.NATS_JETSTREAM_ENABLED:
                self._js = self._nc.jetstream()
                
                # Create streams
                await self._create_streams()
                
                # Create consumers
                await self._create_consumers()
            
            self._running = True
            
            # Start background tasks
            asyncio.create_task(self._heartbeat_loop())
            asyncio.create_task(self._cleanup_expired_messages())
            
            logger.info("🚀 Message Bus started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Message Bus: {str(e)}")
            raise
    
    async def stop(self):
        """Stop the message bus service"""
        self._running = False
        
        # Cancel pending requests
        for future in self._pending_requests.values():
            if not future.done():
                future.cancel()
        
        self._pending_requests.clear()
        
        # Unsubscribe from all subjects
        for subscription in self._subscriptions.values():
            try:
                await subscription.drain()
            except Exception as e:
                logger.error(f"Error draining subscription: {str(e)}")
        
        # Close NATS connection
        if self._nc:
            await self._nc.drain()
        
        logger.info("🔄 Message Bus stopped")
    
    async def _create_streams(self):
        """Create JetStream streams"""
        if not self._js:
            return
        
        streams = [
            {
                "name": "EMAS_EVENTS",
                "subjects": [self._subjects["events"]],
                "storage": StorageType.FILE,
                "max_msgs": 100000,
                "max_age": timedelta(hours=24)
            },
            {
                "name": "EMAS_TASKS",
                "subjects": [self._subjects["tasks"]],
                "storage": StorageType.FILE,
                "max_msgs": 50000,
                "max_age": timedelta(hours=12)
            },
            {
                "name": "EMAS_RESPONSES",
                "subjects": [self._subjects["responses"]],
                "storage": StorageType.FILE,
                "max_msgs": 100000,
                "max_age": timedelta(hours=6)
            },
            {
                "name": "EMAS_BROADCASTS",
                "subjects": [self._subjects["broadcasts"]],
                "storage": StorageType.MEMORY,
                "max_msgs": 1000
            }
        ]
        
        for stream_config in streams:
            try:
                await self._js.add_stream(
                    StreamConfig(**stream_config)
                )
                logger.info(f"Created stream: {stream_config['name']}")
            except Exception as e:
                if "name already in use" not in str(e).lower():
                    logger.error(f"Error creating stream {stream_config['name']}: {str(e)}")
    
    async def _create_consumers(self):
        """Create consumers for streams"""
        # This would be implemented to create durable consumers
        # for reliable message processing
        pass
    
    async def publish(self, subject: str, message: MessageContent, 
                     use_jetstream: bool = True) -> bool:
        """
        Publish a message
        
        Args:
            subject: Subject to publish to
            message: Message content
            use_jetstream: Whether to use JetStream for persistence
            
        Returns:
            True if message was published successfully
        """
        try:
            message_json = json.dumps(message.to_dict())
            
            if use_jetstream and self._js:
                # Publish with JetStream for persistence
                await self._js.publish(
                    subject,
                    message_json.encode(),
                    headers={
                        "message-type": message.message_type.value,
                        "priority": str(message.priority.value),
                        "correlation-id": message.correlation_id or ""
                    }
                )
            else:
                # Direct publish without persistence
                await self._nc.publish(subject, message_json.encode())
            
            self._message_counters["sent"] += 1
            
            logger.debug(f"Message published to {subject}: {message.message_id}")
            return True
            
        except Exception as e:
            self._message_counters["failed"] += 1
            logger.error(f"Failed to publish message to {subject}: {str(e)}")
            return False
    
    async def request(self, subject: str, message: MessageContent, 
                     timeout: float = 30.0) -> Optional[MessageContent]:
        """
        Send a request and wait for response
        
        Args:
            subject: Subject to send request to
            message: Request message
            timeout: Request timeout in seconds
            
        Returns:
            Response message or None if timeout
        """
        request_id = str(uuid.uuid4())
        response_subject = f"{subject}.response.{request_id}"
        
        # Create response future
        response_future = asyncio.Future()
        self._pending_requests[request_id] = response_future
        
        # Set up response handler
        response_handler = await self._nc.subscribe(response_subject)
        
        try:
            # Send the request
            message.correlation_id = request_id
            message.sender_id = message.sender_id or "message-bus"
            
            success = await self.publish(subject, message)
            if not success:
                return None
            
            # Wait for response with timeout
            try:
                response_msg = await asyncio.wait_for(
                    response_future,
                    timeout=timeout
                )
                return response_msg
                
            except asyncio.TimeoutError:
                logger.warning(f"Request timeout for {request_id}")
                return None
                
        finally:
            # Cleanup
            self._pending_requests.pop(request_id, None)
            await response_handler.drain()
    
    async def subscribe(self, subject: str, handler: Callable[[MessageContent], Any],
                       auto_ack: bool = True, priority: Priority = Priority.NORMAL) -> str:
        """
        Subscribe to a subject
        
        Args:
            subject: Subject pattern to subscribe to
            handler: Message handler function
            auto_ack: Whether to automatically acknowledge messages
            priority: Handler priority
            
        Returns:
            Subscription ID
        """
        subscription_id = str(uuid.uuid4())
        
        # Create message handler
        msg_handler = MessageHandler(
            subject=subject,
            callback=handler,
            auto_ack=auto_ack,
            priority=priority
        )
        
        self._handlers[subscription_id] = msg_handler
        
        # Subscribe to NATS subject
        async def nats_handler(msg):
            try:
                message_data = json.loads(msg.data.decode())
                message = MessageContent.from_dict(message_data)
                
                # Execute handler
                await handler(message)
                
                if auto_ack:
                    await msg.ack()
                    
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                if not auto_ack:
                    await msg.nak()
        
        subscription = await self._nc.subscribe(subject, cb=nats_handler)
        self._subscriptions[subscription_id] = subscription
        
        logger.info(f"Subscribed to {subject}: {subscription_id}")
        
        return subscription_id
    
    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a subject"""
        if subscription_id in self._subscriptions:
            subscription = self._subscriptions.pop(subscription_id)
            await subscription.drain()
            self._handlers.pop(subscription_id, None)
            
            logger.info(f"Unsubscribed: {subscription_id}")
    
    async def send_event(self, event_type: str, payload: Dict[str, Any], 
                        source_id: Optional[str] = None) -> bool:
        """Send an event message"""
        message = MessageContent(
            message_type=MessageType.EVENT,
            sender_id=source_id,
            subject=event_type,
            payload=payload,
            correlation_id=str(uuid.uuid4())
        )
        
        subject = self._subjects["events"].replace("*", event_type)
        return await self.publish(subject, message)
    
    async def distribute_task(self, task_type: str, payload: Dict[str, Any],
                            agent_type: Optional[str] = None,
                            priority: Priority = Priority.NORMAL) -> str:
        """
        Distribute a task to available agents
        
        Args:
            task_type: Type of task to distribute
            payload: Task data
            agent_type: Specific agent type to target
            priority: Task priority
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        message = MessageContent(
            message_type=MessageType.TASK,
            subject=task_type,
            payload={
                "task_id": task_id,
                "data": payload,
                "priority": priority.value
            },
            priority=priority
        )
        
        if agent_type:
            subject = f"{settings.NATS_JETSTREAM_SUBJECT_PREFIX}.tasks.{agent_type}.*"
        else:
            subject = self._subjects["tasks"].replace("*", task_type)
        
        await self.publish(subject, message)
        
        logger.info(f"Task distributed: {task_id} ({task_type})")
        
        return task_id
    
    async def broadcast(self, message_type: str, payload: Dict[str, Any],
                       source_id: Optional[str] = None) -> bool:
        """Broadcast a message to all subscribers"""
        message = MessageContent(
            message_type=MessageType.BROADCAST,
            sender_id=source_id,
            subject=message_type,
            payload=payload
        )
        
        return await self.publish(self._subjects["broadcasts"], message)
    
    async def send_heartbeat(self, agent_id: str, status: Dict[str, Any]):
        """Send a heartbeat message from an agent"""
        message = MessageContent(
            message_type=MessageType.HEARTBEAT,
            sender_id=agent_id,
            subject="agent.heartbeat",
            payload=status
        )
        
        return await self.publish(self._subjects["heartbeats"], message)
    
    async def _heartbeat_loop(self):
        """Background task for monitoring message bus health"""
        while self._running:
            try:
                if self._nc and self._nc.is_connected:
                    await self.send_event("message_bus.heartbeat", {
                        "status": "healthy",
                        "timestamp": datetime.now().isoformat(),
                        "counters": self._message_counters
                    })
                
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat loop error: {str(e)}")
                await asyncio.sleep(30)
    
    async def _cleanup_expired_messages(self):
        """Background task for cleaning up expired messages"""
        while self._running:
            try:
                current_time = datetime.now()
                expired_requests = []
                
                for request_id, future in self._pending_requests.items():
                    # Check if request has been pending too long
                    # This would need request timestamp tracking
                    pass
                
                await asyncio.sleep(300)  # Run every 5 minutes
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup error: {str(e)}")
                await asyncio.sleep(300)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check message bus health"""
        try:
            health_status = {
                "status": "healthy",
                "connected": self._nc.is_connected() if self._nc else False,
                "jetstream_enabled": self._js is not None,
                "active_handlers": len(self._handlers),
                "active_subscriptions": len(self._subscriptions),
                "pending_requests": len(self._pending_requests),
                "counters": self._message_counters.copy()
            }
            
            # Test connection
            if self._nc and self._nc.is_connected:
                try:
                    await self._nc.subscribe("health.test")
                    health_status["connection_test"] = "passed"
                except Exception:
                    health_status["connection_test"] = "failed"
                    health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connected": False,
                "jetstream_enabled": False
            }
    
    def get_message_statistics(self) -> Dict[str, Any]:
        """Get message bus statistics"""
        return {
            "counters": self._message_counters.copy(),
            "active_handlers": len(self._handlers),
            "active_subscriptions": len(self._subscriptions),
            "pending_requests": len(self._pending_requests),
            "subject_patterns": {
                "events": self._subjects["events"],
                "tasks": self._subjects["tasks"],
                "responses": self._subjects["responses"],
                "broadcasts": self._subjects["broadcasts"],
                "heartbeats": self._subjects["heartbeats"],
                "errors": self._subjects["errors"]
            }
        }
    
    # Utility methods for common patterns
    
    async def create_agent_channel(self, agent_id: str) -> str:
        """Create a dedicated channel for an agent"""
        channel_name = f"agent.{agent_id}"
        
        async def agent_handler(message: MessageContent):
            # Route message to specific agent
            logger.debug(f"Agent message for {agent_id}: {message.subject}")
        
        await self.subscribe(f"{channel_name}.*", agent_handler)
        
        return channel_name
    
    async def create_task_queue(self, queue_name: str, max_workers: int = 5):
        """Create a task queue for specific task types"""
        # This would implement a work queue pattern
        # where tasks are distributed among available workers
        pass
    
    async def enable_stream_processing(self, stream_name: str, processor: Callable):
        """Enable stream processing for a specific stream"""
        # This would implement stream processing patterns
        # for handling large volumes of messages
        pass


# Message correlation utilities

async def create_request_response_pattern(message_bus: MessageBus, 
                                        request_subject: str,
                                        request_data: Dict[str, Any],
                                        timeout: float = 30.0) -> Optional[MessageContent]:
    """
    Helper function for request-response pattern
    
    Args:
        message_bus: Message bus instance
        request_subject: Subject for request
        request_data: Request data
        timeout: Request timeout
        
    Returns:
        Response message
    """
    message = MessageContent(
        message_type=MessageType.REQUEST,
        payload=request_data
    )
    
    return await message_bus.request(request_subject, message, timeout)


async def create_event_subscription(message_bus: MessageBus,
                                   event_type: str,
                                   handler: Callable[[Dict[str, Any]], Any]):
    """
    Helper function for event subscription
    
    Args:
        message_bus: Message bus instance
        event_type: Type of event to subscribe to
        handler: Event handler function
    """
    async def event_handler(message: MessageContent):
        await handler(message.payload)
    
    subject = f"emas.events.{event_type}"
    await message_bus.subscribe(subject, event_handler)


# Advanced messaging patterns

class MessagePatterns:
    """Predefined messaging patterns for common use cases"""
    
    @staticmethod
    async def task_distribution(message_bus: MessageBus, 
                              task_data: Dict[str, Any],
                              agent_types: List[str],
                              min_responses: int = 1):
        """
        Distribute task to multiple agent types and collect responses
        """
        responses = []
        
        for agent_type in agent_types:
            task_id = await message_bus.distribute_task(
                "multi_agent_task", 
                task_data, 
                agent_type=agent_type,
                priority=Priority.HIGH
            )
            
            # Set up response collection
            response_subject = f"emas.responses.{task_id}"
            # Would implement response collection logic here
        
        return responses
    
    @staticmethod
    async def event_broadcast_system(message_bus: MessageBus,
                                   event_types: List[str],
                                   broadcast_handler: Callable):
        """
        Set up event broadcasting system
        """
        for event_type in event_types:
            await create_event_subscription(message_bus, event_type, broadcast_handler)