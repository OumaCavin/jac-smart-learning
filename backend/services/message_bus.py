"""
Mock Message Bus Service for Development
Minimal implementation to satisfy dependencies

Author: Cavin Otieno
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable

class MockMessageBus:
    """Mock Message Bus for development"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Dict[str, Any]] = []
    
    async def start(self):
        """Start message bus"""
        print("📡 Mock message bus started")
    
    async def stop(self):
        """Stop message bus"""
        print("📡 Mock message bus stopped")
    
    async def publish(self, subject: str, message: Dict[str, Any]):
        """Publish message"""
        print(f"📤 Publishing to {subject}: {message}")
        
        # Store in history
        self.message_history.append({
            "subject": subject,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Notify subscribers
        if subject in self.subscribers:
            for callback in self.subscribers[subject]:
                try:
                    await callback(message)
                except Exception as e:
                    print(f"Error in subscriber: {e}")
    
    async def subscribe(self, subject: str, callback: Callable):
        """Subscribe to subject"""
        if subject not in self.subscribers:
            self.subscribers[subject] = []
        self.subscribers[subject].append(callback)
        print(f"📨 Subscribed to {subject}")
    
    async def health_check(self) -> str:
        """Health check"""
        return "healthy"

# Keep the same class name for compatibility
MessageBus = MockMessageBus