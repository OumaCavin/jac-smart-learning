"""
Mock Test Generation Agent for Development
Minimal implementation to satisfy agent registration

Author: Cavin Otieno
"""

class MockTestGenerationAgent:
    """Mock Test Generation Agent"""
    
    def __init__(self):
        self.agent_id = "test_generation_001"
        self.agent_type = "test_generation"
        self.status = "ready"
    
    async def process_task(self, task_data):
        """Process a test generation task"""
        return {
            "status": "completed",
            "result": "Mock tests generated successfully"
        }
    
    async def health_check(self):
        """Health check"""
        return "healthy"

TestGenerationAgent = MockTestGenerationAgent