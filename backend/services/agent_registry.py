"""
Mock Agent Registry Service for Development
Minimal implementation to satisfy dependencies

Author: Cavin Otieno
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Any

class MockAgentRegistry:
    """Mock Agent Registry for development"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.agent_status: Dict[str, str] = {}
    
    async def start(self):
        """Start agent registry"""
        print("🤖 Mock agent registry started")
    
    async def stop(self):
        """Stop agent registry"""
        print("🤖 Mock agent registry stopped")
    
    async def register_agent(self, agent):
        """Register an agent"""
        agent_id = str(uuid.uuid4())
        self.agents[agent_id] = agent
        self.agent_status[agent_id] = "registered"
        print(f"✅ Registered agent: {agent_id}")
    
    async def unregister_agent(self, agent_id: str):
        """Unregister an agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.agent_status[agent_id]
            print(f"🗑️  Unregistered agent: {agent_id}")
    
    async def health_check(self) -> str:
        """Health check"""
        return "healthy"
    
    def get_registered_agents(self) -> List[str]:
        """Get list of registered agents"""
        return list(self.agents.keys())

# Keep the same class name for compatibility
AgentRegistry = MockAgentRegistry