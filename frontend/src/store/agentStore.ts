import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

export interface Agent {
  id: string
  name: string
  type: string
  status: 'idle' | 'running' | 'busy' | 'error' | 'stopped'
  version: string
  description: string
  capabilities: string[]
  lastActivity: string
  performance: {
    tasksCompleted: number
    successRate: number
    averageExecutionTime: number
  }
}

interface AgentState {
  agents: Agent[]
  isLoading: boolean
  error: string | null
  
  // Actions
  setAgents: (agents: Agent[]) => void
  addAgent: (agent: Agent) => void
  updateAgentStatus: (agentId: string, status: Agent['status']) => void
  removeAgent: (agentId: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  loadAgents: () => Promise<void>
}

export const useAgentStore = create<AgentState>()(
  devtools(
    (set, get) => ({
      agents: [
        {
          id: '1',
          name: 'Code Analysis Agent',
          type: 'code_analysis',
          status: 'running',
          version: '1.0.0',
          description: 'Analyzes code quality, complexity, and maintainability',
          capabilities: ['ast_parsing', 'complexity_analysis', 'code_smells'],
          lastActivity: '2024-01-15T10:30:00Z',
          performance: {
            tasksCompleted: 156,
            successRate: 98.5,
            averageExecutionTime: 2.3
          }
        },
        {
          id: '2',
          name: 'Test Generation Agent',
          type: 'test_generation',
          status: 'idle',
          version: '1.2.0',
          description: 'Generates comprehensive test suites from code analysis',
          capabilities: ['unit_tests', 'integration_tests', 'property_based_tests'],
          lastActivity: '2024-01-15T09:45:00Z',
          performance: {
            tasksCompleted: 89,
            successRate: 95.2,
            averageExecutionTime: 5.1
          }
        },
        {
          id: '3',
          name: 'Security Scanning Agent',
          type: 'security_scanning',
          status: 'busy',
          version: '1.1.0',
          description: 'Scans code for security vulnerabilities and compliance issues',
          capabilities: ['vulnerability_scan', 'dependency_check', 'compliance_check'],
          lastActivity: '2024-01-15T11:15:00Z',
          performance: {
            tasksCompleted: 234,
            successRate: 99.1,
            averageExecutionTime: 3.7
          }
        },
        {
          id: '4',
          name: 'Performance Analysis Agent',
          type: 'performance_analysis',
          status: 'running',
          version: '1.0.5',
          description: 'Analyzes code performance and suggests optimizations',
          capabilities: ['profiling', 'bottleneck_detection', 'optimization_suggestions'],
          lastActivity: '2024-01-15T10:50:00Z',
          performance: {
            tasksCompleted: 67,
            successRate: 92.3,
            averageExecutionTime: 8.2
          }
        },
        {
          id: '5',
          name: 'Documentation Agent',
          type: 'documentation',
          status: 'idle',
          version: '1.0.0',
          description: 'Generates and maintains code documentation',
          capabilities: ['api_docs', 'user_guides', 'readme_generation'],
          lastActivity: '2024-01-15T08:20:00Z',
          performance: {
            tasksCompleted: 45,
            successRate: 88.9,
            averageExecutionTime: 4.5
          }
        }
      ],
      isLoading: false,
      error: null,
      
      setAgents: (agents) => set({ agents }),
      
      addAgent: (agent) => set((state) => ({
        agents: [...state.agents, agent]
      })),
      
      updateAgentStatus: (agentId, status) => set((state) => ({
        agents: state.agents.map(agent => 
          agent.id === agentId ? { ...agent, status } : agent
        )
      })),
      
      removeAgent: (agentId) => set((state) => ({
        agents: state.agents.filter(agent => agent.id !== agentId)
      })),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      loadAgents: async () => {
        set({ isLoading: true, error: null })
        try {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 1000))
          // In real implementation, this would fetch from backend API
        } catch (error) {
          set({ error: 'Failed to load agents' })
        } finally {
          set({ isLoading: false })
        }
      }
    }),
    {
      name: 'agent-store'
    }
  )
)