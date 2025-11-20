import { motion } from 'framer-motion'
import { 
  Activity, 
  Bot, 
  CheckCircle, 
  Clock, 
  TrendingUp, 
  AlertTriangle,
  Code,
  Zap
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { useAgentStore } from '../store/agentStore'
import { useProjectStore } from '../store/projectStore'

const Dashboard = () => {
  const { agents } = useAgentStore()
  const { projects } = useProjectStore()

  // Calculate statistics
  const totalAgents = agents.length
  const activeAgents = agents.filter(a => a.status === 'running' || a.status === 'busy').length
  const totalProjects = projects.length
  const completedTasks = projects.reduce((sum, p) => sum + p.completedTasks, 0)
  const pendingTasks = projects.reduce((sum, p) => sum + p.pendingTasks, 0)

  // Mock data for charts
  const performanceData = [
    { time: '09:00', tasks: 12, agents: 5 },
    { time: '10:00', tasks: 19, agents: 7 },
    { time: '11:00', tasks: 15, agents: 6 },
    { time: '12:00', tasks: 23, agents: 8 },
    { time: '13:00', tasks: 18, agents: 7 },
    { time: '14:00', tasks: 25, agents: 9 },
    { time: '15:00', tasks: 22, agents: 8 }
  ]

  const agentStatusData = [
    { name: 'Running', value: agents.filter(a => a.status === 'running').length, color: '#10B981' },
    { name: 'Busy', value: agents.filter(a => a.status === 'busy').length, color: '#F59E0B' },
    { name: 'Idle', value: agents.filter(a => a.status === 'idle').length, color: '#6B7280' },
    { name: 'Error', value: agents.filter(a => a.status === 'error').length, color: '#EF4444' }
  ]

  const recentActivities = [
    {
      id: 1,
      type: 'task_completed',
      message: 'Code analysis agent completed analysis for project "E-Commerce Platform"',
      timestamp: '2 minutes ago',
      icon: CheckCircle,
      color: 'text-green-500'
    },
    {
      id: 2,
      type: 'agent_start',
      message: 'Test Generation Agent started new test suite generation',
      timestamp: '5 minutes ago',
      icon: Zap,
      color: 'text-blue-500'
    },
    {
      id: 3,
      type: 'project_created',
      message: 'New project "AI Chatbot" created with 5 agents assigned',
      timestamp: '12 minutes ago',
      icon: Code,
      color: 'text-purple-500'
    },
    {
      id: 4,
      type: 'warning',
      message: 'Security Scanning Agent detected potential vulnerabilities',
      timestamp: '18 minutes ago',
      icon: AlertTriangle,
      color: 'text-yellow-500'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <motion.h1 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent"
        >
          Dashboard
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-gray-600 font-medium"
        >
          Monitor your multi-agent system in real-time
        </motion.p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="metric-card group cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 font-semibold mb-2">Active Agents</p>
              <p className="text-4xl font-bold text-gray-900 mb-1">{activeAgents}</p>
              <p className="text-sm text-gray-400">of {totalAgents} total</p>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300">
              <Bot className="w-8 h-8 text-blue-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="metric-card group cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 font-semibold mb-2">Active Projects</p>
              <p className="text-4xl font-bold text-gray-900 mb-1">{totalProjects}</p>
              <p className="text-sm text-gray-400">running tasks</p>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300">
              <Activity className="w-8 h-8 text-green-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="metric-card group cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 font-semibold mb-2">Completed Tasks</p>
              <p className="text-4xl font-bold text-gray-900 mb-1">{completedTasks}</p>
              <p className="text-sm text-gray-400">this week</p>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300">
              <CheckCircle className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="metric-card group cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 font-semibold mb-2">Pending Tasks</p>
              <p className="text-4xl font-bold text-gray-900 mb-1">{pendingTasks}</p>
              <p className="text-sm text-gray-400">in queue</p>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-orange-100 to-orange-200 rounded-2xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300">
              <Clock className="w-8 h-8 text-orange-600" />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Performance Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">System Performance</h3>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="time" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="tasks"
                  stackId="1"
                  stroke="#3B82F6"
                  fill="#3B82F6"
                  fillOpacity={0.3}
                  name="Tasks Completed"
                />
                <Area
                  type="monotone"
                  dataKey="agents"
                  stackId="2"
                  stroke="#10B981"
                  fill="#10B981"
                  fillOpacity={0.3}
                  name="Active Agents"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Agent Status Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Agent Status</h3>
            <Bot className="w-6 h-6 text-blue-500" />
          </div>
          <div className="h-48 mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={agentStatusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {agentStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    border: '1px solid rgba(229, 231, 235, 0.5)',
                    borderRadius: '12px',
                    backdropFilter: 'blur(10px)',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3">
            {agentStatusData.map((entry, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors">
                <div className="flex items-center space-x-3">
                  <div 
                    className="w-4 h-4 rounded-full shadow-sm"
                    style={{ backgroundColor: entry.color }}
                  />
                  <span className="text-sm font-semibold text-gray-700">{entry.name}</span>
                </div>
                <span className="text-lg font-bold text-gray-900">{entry.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-xl font-bold text-gray-900">Recent Activity</h3>
          <Activity className="w-6 h-6 text-gray-400" />
        </div>
        <div className="space-y-4">
          {recentActivities.map((activity) => {
            const Icon = activity.icon
            return (
              <div key={activity.id} className="flex items-start space-x-4 p-4 hover:bg-gray-50 rounded-2xl transition-all duration-300 group cursor-pointer">
                <div className={`w-10 h-10 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-sm group-hover:shadow-md transition-all duration-300`}>
                  <Icon className={`w-5 h-5 ${activity.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-900 leading-relaxed">{activity.message}</p>
                  <p className="text-xs text-gray-500 mt-1 font-medium">{activity.timestamp}</p>
                </div>
                <div className="w-2 h-2 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full opacity-50 group-hover:opacity-100 transition-opacity duration-300"></div>
              </div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard