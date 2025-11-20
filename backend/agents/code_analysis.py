"""
Mock Code Analysis Agent for Development
Minimal implementation to satisfy agent registration

Author: Cavin Otieno
"""

class MockCodeAnalysisAgent:
    """Mock Code Analysis Agent"""
    
    def __init__(self):
        self.agent_id = "code_analysis_001"
        self.agent_type = "code_analysis"
        self.status = "ready"
    
    async def process_task(self, task_data):
        """Process a code analysis task"""
        return {
            "status": "completed",
            "result": "Mock analysis completed successfully"
        }
    
    async def health_check(self):
        """Health check"""
        return "healthy"

CodeAnalysisAgent = MockCodeAnalysisAgent