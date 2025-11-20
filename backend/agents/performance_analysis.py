"""
Mock Performance Analysis Agent for Development
Minimal implementation to satisfy agent registration

Author: Cavin Otieno
"""

class MockPerformanceAnalysisAgent:
    """Mock Performance Analysis Agent"""
    
    def __init__(self):
        self.agent_id = "performance_analysis_001"
        self.agent_type = "performance_analysis"
        self.status = "ready"
    
    async def process_task(self, task_data):
        """Process a performance analysis task"""
        return {
            "status": "completed",
            "result": "Mock performance analysis completed successfully"
        }
    
    async def health_check(self):
        """Health check"""
        return "healthy"

PerformanceAnalysisAgent = MockPerformanceAnalysisAgent