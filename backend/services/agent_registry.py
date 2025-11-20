"""
Agent Registry Service
Manages agent lifecycle, registration, discovery, and coordination

Author: Cavin Otieno
"""

import asyncio
import uuid
import time
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from loguru import logger

from backend.core.config import settings


class AgentStatus(Enum):
    """Agent status enumeration"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    STOPPING = "stopping"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"


class AgentType(Enum):
    """Available agent types"""
    CODE_ANALYSIS = "code_analysis"
    TEST_GENERATION = "test_generation"
    SECURITY_SCANNING = "security_scanning"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    DOCUMENTATION = "documentation"
    QUALITY_ASSESSMENT = "quality_assessment"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    CUSTOM = "custom"


@dataclass
class AgentMetadata:
    """Agent metadata and configuration"""
    agent_id: str
    name: str
    agent_type: AgentType
    version: str
    description: str
    capabilities: List[str]
    requirements: Dict[str, Any]
    config: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: AgentStatus = AgentStatus.INITIALIZING
    
    # Performance metrics
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time: float = 0.0
    last_execution_time: Optional[datetime] = None
    
    # Resource usage
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_type": self.agent_type.value,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "requirements": self.requirements,
            "config": self.config,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "average_execution_time": self.average_execution_time,
            "last_execution_time": self.last_execution_time.isoformat() if self.last_execution_time else None,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_usage": self.disk_usage,
            "success_rate": (self.successful_executions / max(1, self.total_executions)) * 100
        }


class AgentRegistry:
    """
    Agent Registry Service
    
    Manages the lifecycle of all agents in the system:
    - Registration and discovery
    - Health monitoring
    - Load balancing
    - Failure detection and recovery
    """
    
    def __init__(self):
        self._agents: Dict[str, AgentMetadata] = {}
        self._agent_instances: Dict[str, Any] = {}
        self._agent_types: Dict[str, List[str]] = {}
        self._status_callbacks: Dict[str, List[Callable]] = {}
        self._health_check_interval = settings.AGENT_HEALTH_CHECK_INTERVAL
        self._running = False
        self._health_check_task: Optional[asyncio.Task] = None
        
        # Initialize agent type mappings
        self._initialize_agent_types()
        
        logger.info("🤖 Agent Registry initialized")
    
    def _initialize_agent_types(self):
        """Initialize agent type mappings"""
        self._agent_types = {
            AgentType.CODE_ANALYSIS: ["code_analysis"],
            AgentType.TEST_GENERATION: ["test_generation", "unit_tests", "integration_tests"],
            AgentType.SECURITY_SCANNING: ["security_analysis", "vulnerability_scan", "static_analysis"],
            AgentType.PERFORMANCE_ANALYSIS: ["performance_analysis", "profiling", "optimization"],
            AgentType.DOCUMENTATION: ["documentation", "api_docs", "user_guides"],
            AgentType.QUALITY_ASSESSMENT: ["quality_metrics", "code_review", "standards_compliance"],
            AgentType.DEPLOYMENT: ["deployment", "ci_cd", "release_management"],
            AgentType.MONITORING: ["monitoring", "alerting", "health_checks"],
            AgentType.CUSTOM: ["custom", "extension", "plugin"]
        }
    
    async def start(self):
        """Start the agent registry service"""
        self._running = True
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        logger.info("🚀 Agent Registry started")
    
    async def stop(self):
        """Stop the agent registry service"""
        self._running = False
        
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        
        # Stop all registered agents
        stop_tasks = []
        for agent_id in list(self._agents.keys()):
            stop_tasks.append(self.stop_agent(agent_id))
        
        if stop_tasks:
            await asyncio.gather(*stop_tasks, return_exceptions=True)
        
        logger.info("🔄 Agent Registry stopped")
    
    async def register_agent(self, agent_instance: Any) -> str:
        """
        Register a new agent
        
        Args:
            agent_instance: Agent instance implementing the agent interface
            
        Returns:
            Agent ID assigned to the registered agent
        """
        agent_id = str(uuid.uuid4())
        
        # Create agent metadata
        metadata = AgentMetadata(
            agent_id=agent_id,
            name=getattr(agent_instance, 'name', f'Agent-{agent_id[:8]}'),
            agent_type=getattr(agent_instance, 'agent_type', AgentType.CUSTOM),
            version=getattr(agent_instance, 'version', '1.0.0'),
            description=getattr(agent_instance, 'description', 'Unspecified agent'),
            capabilities=getattr(agent_instance, 'capabilities', []),
            requirements=getattr(agent_instance, 'requirements', {}),
            config=getattr(agent_instance, 'config', {})
        )
        
        # Register the agent
        self._agents[agent_id] = metadata
        self._agent_instances[agent_id] = agent_instance
        
        # Update status
        await self.update_agent_status(agent_id, AgentStatus.RUNNING)
        
        logger.info(f"✅ Agent registered: {metadata.name} ({agent_id})")
        
        return agent_id
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            True if agent was unregistered, False if not found
        """
        if agent_id not in self._agents:
            logger.warning(f"Agent not found: {agent_id}")
            return False
        
        # Stop the agent
        await self.stop_agent(agent_id)
        
        # Remove from registry
        metadata = self._agents.pop(agent_id)
        self._agent_instances.pop(agent_id, None)
        self._status_callbacks.pop(agent_id, None)
        
        logger.info(f"🗑️ Agent unregistered: {metadata.name} ({agent_id})")
        
        return True
    
    async def get_agent(self, agent_id: str) -> Optional[AgentMetadata]:
        """Get agent metadata by ID"""
        return self._agents.get(agent_id)
    
    async def list_agents(self, agent_type: Optional[AgentType] = None, 
                         status: Optional[AgentStatus] = None) -> List[AgentMetadata]:
        """
        List all agents, optionally filtered by type and status
        
        Args:
            agent_type: Filter by agent type
            status: Filter by agent status
            
        Returns:
            List of matching agents
        """
        agents = list(self._agents.values())
        
        if agent_type:
            agents = [a for a in agents if a.agent_type == agent_type]
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    async def find_agents_by_capability(self, capability: str) -> List[AgentMetadata]:
        """Find agents that support a specific capability"""
        matching_agents = []
        
        for agent in self._agents.values():
            if capability in agent.capabilities:
                matching_agents.append(agent)
        
        return matching_agents
    
    async def get_healthy_agents(self, agent_type: Optional[AgentType] = None) -> List[AgentMetadata]:
        """Get all healthy agents, optionally filtered by type"""
        healthy_statuses = [AgentStatus.RUNNING, AgentStatus.IDLE, AgentStatus.BUSY]
        agents = list(self._agents.values())
        
        if agent_type:
            agents = [a for a in agents if a.agent_type == agent_type]
        
        return [a for a in agents if a.status in healthy_statuses]
    
    async def update_agent_status(self, agent_id: str, status: AgentStatus, 
                                 metadata: Optional[Dict[str, Any]] = None):
        """Update agent status and optionally additional metadata"""
        if agent_id not in self._agents:
            logger.warning(f"Agent not found for status update: {agent_id}")
            return
        
        agent = self._agents[agent_id]
        agent.status = status
        agent.updated_at = datetime.now()
        
        # Update additional metadata if provided
        if metadata:
            for key, value in metadata.items():
                if hasattr(agent, key):
                    setattr(agent, key, value)
        
        # Execute status callbacks
        if agent_id in self._status_callbacks:
            for callback in self._status_callbacks[agent_id]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(agent_id, status, metadata)
                    else:
                        callback(agent_id, status, metadata)
                except Exception as e:
                    logger.error(f"Error executing status callback for agent {agent_id}: {str(e)}")
        
        logger.debug(f"Agent {agent_id} status updated to: {status.value}")
    
    async def start_agent(self, agent_id: str) -> bool:
        """Start a stopped agent"""
        if agent_id not in self._agents:
            logger.warning(f"Agent not found: {agent_id}")
            return False
        
        agent = self._agents[agent_id]
        
        try:
            # Get agent instance
            agent_instance = self._agent_instances.get(agent_id)
            
            if agent_instance and hasattr(agent_instance, 'start'):
                await agent_instance.start()
            
            await self.update_agent_status(agent_id, AgentStatus.RUNNING)
            logger.info(f"Agent started: {agent.name} ({agent_id})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start agent {agent_id}: {str(e)}")
            await self.update_agent_status(agent_id, AgentStatus.ERROR)
            return False
    
    async def stop_agent(self, agent_id: str) -> bool:
        """Stop a running agent"""
        if agent_id not in self._agents:
            logger.warning(f"Agent not found: {agent_id}")
            return False
        
        agent = self._agents[agent_id]
        
        try:
            await self.update_agent_status(agent_id, AgentStatus.STOPPING)
            
            # Get agent instance
            agent_instance = self._agent_instances.get(agent_id)
            
            if agent_instance and hasattr(agent_instance, 'stop'):
                await agent_instance.stop()
            
            await self.update_agent_status(agent_id, AgentStatus.STOPPED)
            logger.info(f"Agent stopped: {agent.name} ({agent_id})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop agent {agent_id}: {str(e)}")
            await self.update_agent_status(agent_id, AgentStatus.ERROR)
            return False
    
    async def execute_agent_task(self, agent_id: str, task_type: str, 
                               task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task on a specific agent
        
        Args:
            agent_id: ID of the agent to execute the task
            task_type: Type of task to execute
            task_data: Data for the task execution
            
        Returns:
            Task execution result
        """
        if agent_id not in self._agents:
            raise ValueError(f"Agent not found: {agent_id}")
        
        agent = self._agents[agent_id]
        agent_instance = self._agent_instances.get(agent_id)
        
        if not agent_instance:
            raise ValueError(f"Agent instance not found: {agent_id}")
        
        # Update agent status
        await self.update_agent_status(agent_id, AgentStatus.BUSY)
        
        start_time = time.time()
        
        try:
            # Execute the task
            if hasattr(agent_instance, 'execute_task'):
                result = await agent_instance.execute_task(task_type, task_data)
            else:
                raise NotImplementedError(f"Agent {agent_id} does not implement execute_task")
            
            # Update metrics
            execution_time = time.time() - start_time
            agent.total_executions += 1
            agent.successful_executions += 1
            agent.average_execution_time = (
                (agent.average_execution_time * (agent.total_executions - 1) + execution_time) 
                / agent.total_executions
            )
            agent.last_execution_time = datetime.now()
            
            # Update agent status back to idle
            await self.update_agent_status(agent_id, AgentStatus.IDLE)
            
            logger.info(f"Task executed successfully on agent {agent_id}: {task_type}")
            
            return {
                "success": True,
                "agent_id": agent_id,
                "task_type": task_type,
                "execution_time": execution_time,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Update metrics for failure
            execution_time = time.time() - start_time
            agent.total_executions += 1
            agent.failed_executions += 1
            
            await self.update_agent_status(agent_id, AgentStatus.IDLE)
            
            logger.error(f"Task execution failed on agent {agent_id}: {str(e)}")
            
            return {
                "success": False,
                "agent_id": agent_id,
                "task_type": task_type,
                "execution_time": execution_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents"""
        health_status = {
            "status": "healthy",
            "total_agents": len(self._agents),
            "running_agents": 0,
            "error_agents": 0,
            "agent_details": {}
        }
        
        for agent_id, agent in self._agents.items():
            agent_health = {
                "status": agent.status.value,
                "last_execution": agent.last_execution_time.isoformat() if agent.last_execution_time else None,
                "success_rate": (agent.successful_executions / max(1, agent.total_executions)) * 100,
                "average_execution_time": agent.average_execution_time
            }
            
            health_status["agent_details"][agent_id] = agent_health
            
            # Count statuses
            if agent.status == AgentStatus.ERROR:
                health_status["error_agents"] += 1
            elif agent.status in [AgentStatus.RUNNING, AgentStatus.IDLE, AgentStatus.BUSY]:
                health_status["running_agents"] += 1
        
        # Determine overall health
        if health_status["error_agents"] > 0:
            health_status["status"] = "degraded"
        
        if health_status["running_agents"] == 0:
            health_status["status"] = "unhealthy"
        
        return health_status
    
    async def _health_check_loop(self):
        """Background task for periodic health checks"""
        while self._running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self._health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check loop error: {str(e)}")
                await asyncio.sleep(self._health_check_interval)
    
    async def _perform_health_checks(self):
        """Perform health checks on individual agents"""
        for agent_id, agent in self._agents.items():
            try:
                agent_instance = self._agent_instances.get(agent_id)
                
                if agent_instance and hasattr(agent_instance, 'health_check'):
                    is_healthy = await agent_instance.health_check()
                    
                    if not is_healthy and agent.status == AgentStatus.RUNNING:
                        logger.warning(f"Agent {agent_id} failed health check, marking as error")
                        await self.update_agent_status(agent_id, AgentStatus.ERROR)
                
            except Exception as e:
                logger.error(f"Health check failed for agent {agent_id}: {str(e)}")
                if agent.status == AgentStatus.RUNNING:
                    await self.update_agent_status(agent_id, AgentStatus.ERROR)
    
    def register_status_callback(self, agent_id: str, callback: Callable):
        """Register a callback for agent status changes"""
        if agent_id not in self._status_callbacks:
            self._status_callbacks[agent_id] = []
        
        self._status_callbacks[agent_id].append(callback)
    
    def unregister_status_callback(self, agent_id: str, callback: Callable):
        """Unregister a status change callback"""
        if agent_id in self._status_callbacks:
            try:
                self._status_callbacks[agent_id].remove(callback)
            except ValueError:
                pass
    
    async def get_load_balanced_agent(self, agent_type: AgentType) -> Optional[str]:
        """Get the least loaded agent of a specific type"""
        available_agents = await self.get_healthy_agents(agent_type)
        
        if not available_agents:
            return None
        
        # Sort by load (number of executions and average time)
        available_agents.sort(key=lambda a: (
            a.total_executions,
            a.average_execution_time
        ))
        
        return available_agents[0].agent_id
    
    async def cleanup_stale_agents(self, stale_threshold: int = 3600):
        """Remove agents that haven't been active for a specified time"""
        current_time = datetime.now()
        stale_agents = []
        
        for agent_id, agent in self._agents.items():
            if agent.last_execution_time:
                time_since_last_execution = (
                    current_time - agent.last_execution_time
                ).total_seconds()
                
                if time_since_last_execution > stale_threshold:
                    stale_agents.append(agent_id)
        
        # Remove stale agents
        for agent_id in stale_agents:
            agent = self._agents[agent_id]
            logger.info(f"Cleaning up stale agent: {agent.name} ({agent_id})")
            await self.unregister_agent(agent_id)
    
    def get_registry_statistics(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics"""
        total_agents = len(self._agents)
        status_counts = {}
        type_counts = {}
        
        for agent in self._agents.values():
            # Count by status
            status = agent.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by type
            agent_type = agent.agent_type.value
            type_counts[agent_type] = type_counts.get(agent_type, 0) + 1
        
        return {
            "total_agents": total_agents,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "uptime": "N/A",  # Would need to track registry start time
            "health_check_interval": self._health_check_interval
        }