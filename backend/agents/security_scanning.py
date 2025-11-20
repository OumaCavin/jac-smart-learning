"""
Mock Security Scanning Agent for Development
Minimal implementation to satisfy agent registration

Author: Cavin Otieno
"""

class MockSecurityScanningAgent:
    """Mock Security Scanning Agent"""
    
    def __init__(self):
        self.agent_id = "security_scanning_001"
        self.agent_type = "security_scanning"
        self.status = "ready"
    
    async def process_task(self, task_data):
        """Process a security scanning task"""
        return {
            "status": "completed",
            "result": "Mock security scan completed successfully"
        }
    
    async def health_check(self):
        """Health check"""
        return "healthy"

SecurityScanningAgent = MockSecurityScanningAgent