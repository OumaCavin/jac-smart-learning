import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

export interface Project {
  id: string
  name: string
  description: string
  status: 'active' | 'completed' | 'paused' | 'archived'
  createdAt: string
  lastActivity: string
  agents: string[]
  completedTasks: number
  pendingTasks: number
  totalTasks: number
  progress: number
  technology: string[]
  repository?: string
}

interface ProjectState {
  projects: Project[]
  isLoading: boolean
  error: string | null
  
  // Actions
  setProjects: (projects: Project[]) => void
  addProject: (project: Project) => void
  updateProjectStatus: (projectId: string, status: Project['status']) => void
  removeProject: (projectId: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  loadProjects: () => Promise<void>
}

export const useProjectStore = create<ProjectState>()(
  devtools(
    (set, get) => ({
      projects: [
        {
          id: '1',
          name: 'E-Commerce Platform',
          description: 'Full-stack e-commerce platform with microservices architecture',
          status: 'active',
          createdAt: '2024-01-10T09:00:00Z',
          lastActivity: '2024-01-15T11:20:00Z',
          agents: ['1', '2', '3'],
          completedTasks: 45,
          pendingTasks: 8,
          totalTasks: 53,
          progress: 85,
          technology: ['React', 'Node.js', 'PostgreSQL', 'Redis'],
          repository: 'https://github.com/example/ecommerce-platform'
        },
        {
          id: '2',
          name: 'AI Chatbot System',
          description: 'Intelligent chatbot with natural language processing capabilities',
          status: 'active',
          createdAt: '2024-01-12T14:30:00Z',
          lastActivity: '2024-01-15T10:45:00Z',
          agents: ['1', '4', '5'],
          completedTasks: 32,
          pendingTasks: 12,
          totalTasks: 44,
          progress: 73,
          technology: ['Python', 'TensorFlow', 'FastAPI', 'MongoDB']
        },
        {
          id: '3',
          name: 'DevOps Automation Suite',
          description: 'Automated CI/CD pipeline with monitoring and deployment tools',
          status: 'completed',
          createdAt: '2024-01-08T11:15:00Z',
          lastActivity: '2024-01-14T16:00:00Z',
          agents: ['2', '3', '4'],
          completedTasks: 78,
          pendingTasks: 0,
          totalTasks: 78,
          progress: 100,
          technology: ['Kubernetes', 'Docker', 'Jenkins', 'Prometheus']
        },
        {
          id: '4',
          name: 'Real-time Analytics Dashboard',
          description: 'Interactive dashboard for real-time data visualization and analysis',
          status: 'active',
          createdAt: '2024-01-14T08:45:00Z',
          lastActivity: '2024-01-15T09:30:00Z',
          agents: ['1', '4'],
          completedTasks: 18,
          pendingTasks: 15,
          totalTasks: 33,
          progress: 55,
          technology: ['Vue.js', 'D3.js', 'WebSocket', 'InfluxDB']
        },
        {
          id: '5',
          name: 'Mobile App Backend',
          description: 'Scalable backend services for mobile applications',
          status: 'paused',
          createdAt: '2024-01-05T10:20:00Z',
          lastActivity: '2024-01-12T15:30:00Z',
          agents: ['1', '2'],
          completedTasks: 23,
          pendingTasks: 7,
          totalTasks: 30,
          progress: 77,
          technology: ['Go', 'gRPC', 'PostgreSQL', 'Redis']
        }
      ],
      isLoading: false,
      error: null,
      
      setProjects: (projects) => set({ projects }),
      
      addProject: (project) => set((state) => ({
        projects: [...state.projects, project]
      })),
      
      updateProjectStatus: (projectId, status) => set((state) => ({
        projects: state.projects.map(project => 
          project.id === projectId ? { ...project, status } : project
        )
      })),
      
      removeProject: (projectId) => set((state) => ({
        projects: state.projects.filter(project => project.id !== projectId)
      })),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      loadProjects: async () => {
        set({ isLoading: true, error: null })
        try {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 800))
          // In real implementation, this would fetch from backend API
        } catch (error) {
          set({ error: 'Failed to load projects' })
        } finally {
          set({ isLoading: false })
        }
      }
    }),
    {
      name: 'project-store'
    }
  )
)