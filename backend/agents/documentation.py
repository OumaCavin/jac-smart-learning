"""
Mock Documentation Agent for Development
Minimal implementation to satisfy agent registration

Author: Cavin Otieno
"""

class MockDocumentationAgent:
    """Mock Documentation Agent"""
    
    def __init__(self):
        self.agent_id = "documentation_001"
        self.agent_type = "documentation"
        self.status = "ready"
    
    async def process_task(self, task_data):
        """Process a documentation task"""
        return {
            "status": "completed",
            "result": "Mock documentation generated successfully"
        }
    
    async def health_check(self):
        """Health check"""
        return "healthy"

DocumentationAgent = MockDocumentationAgent