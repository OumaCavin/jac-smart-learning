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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/40 p-6">
      {/* Header */}
      <div className="mb-10">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="glass rounded-3xl p-8 shadow-soft border border-white/50"
        >
          <h1 className="text-5xl font-bold text-gradient mb-4">
            Dashboard
          </h1>
          <p className="text-lg text-gray-600 font-medium leading-relaxed">
            Monitor your multi-agent system in real-time
          </p>
        </motion.div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="card-interactive group"
        >
          <div className="glass rounded-3xl p-8 h-full relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-blue-600"></div>
            <div className="flex items-center justify-between h-full">
              <div className="space-y-3">
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Active Agents</p>
                <p className="text-5xl font-bold text-gray-900 mb-2">{activeAgents}</p>
                <p className="text-sm text-gray-500 font-medium">of {totalAgents} total</p>
              </div>
              <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-blue-200 rounded-3xl flex items-center justify-center shadow-glow group-hover:shadow-xl transition-all duration-300">
                <Bot className="w-10 h-10 text-blue-600" />
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="card-interactive group"
        >
          <div className="glass rounded-3xl p-8 h-full relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-emerald-600"></div>
            <div className="flex items-center justify-between h-full">
              <div className="space-y-3">
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Active Projects</p>
                <p className="text-5xl font-bold text-gray-900 mb-2">{totalProjects}</p>
                <p className="text-sm text-gray-500 font-medium">running tasks</p>
              </div>
              <div className="w-20 h-20 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-3xl flex items-center justify-center shadow-glow group-hover:shadow-xl transition-all duration-300">
                <Activity className="w-10 h-10 text-emerald-600" />
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="card-interactive group"
        >
          <div className="glass rounded-3xl p-8 h-full relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 to-purple-600"></div>
            <div className="flex items-center justify-between h-full">
              <div className="space-y-3">
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Completed Tasks</p>
                <p className="text-5xl font-bold text-gray-900 mb-2">{completedTasks}</p>
                <p className="text-sm text-gray-500 font-medium">this week</p>
              </div>
              <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-purple-200 rounded-3xl flex items-center justify-center shadow-glow group-hover:shadow-xl transition-all duration-300">
                <CheckCircle className="w-10 h-10 text-purple-600" />
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="card-interactive group"
        >
          <div className="glass rounded-3xl p-8 h-full relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500 to-amber-600"></div>
            <div className="flex items-center justify-between h-full">
              <div className="space-y-3">
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Pending Tasks</p>
                <p className="text-5xl font-bold text-gray-900 mb-2">{pendingTasks}</p>
                <p className="text-sm text-gray-500 font-medium">in queue</p>
              </div>
              <div className="w-20 h-20 bg-gradient-to-br from-amber-100 to-amber-200 rounded-3xl flex items-center justify-center shadow-glow group-hover:shadow-xl transition-all duration-300">
                <Clock className="w-10 h-10 text-amber-600" />
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        {/* Performance Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="lg:col-span-2 card p-8"
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">System Performance</h3>
              <p className="text-gray-500 font-medium">Real-time task and agent metrics</p>
            </div>
            <div className="w-14 h-14 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center shadow-glow">
              <TrendingUp className="w-7 h-7 text-emerald-600" />
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorAgents" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="time" 
                  stroke="#6b7280" 
                  fontSize={12}
                  fontWeight={500}
                />
                <YAxis 
                  stroke="#6b7280" 
                  fontSize={12}
                  fontWeight={500}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    border: '1px solid rgba(229, 231, 235, 0.5)',
                    borderRadius: '16px',
                    backdropFilter: 'blur(10px)',
                    boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)',
                    fontSize: '14px'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="tasks"
                  stroke="#3B82F6"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#colorTasks)"
                  name="Tasks Completed"
                />
                <Area
                  type="monotone"
                  dataKey="agents"
                  stroke="#10B981"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#colorAgents)"
                  name="Active Agents"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Agent Status Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="card p-8"
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Agent Status</h3>
              <p className="text-gray-500 font-medium">Current agent states</p>
            </div>
            <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center shadow-glow">
              <Bot className="w-7 h-7 text-blue-600" />
            </div>
          </div>
          <div className="h-56 mb-8">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={agentStatusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={8}
                  dataKey="value"
                  stroke="white"
                  strokeWidth={2}
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
                    boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)',
                    fontSize: '14px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-4">
            {agentStatusData.map((entry, index) => (
              <div key={index} className="flex items-center justify-between p-4 rounded-2xl hover:bg-gray-50 transition-all duration-200 group cursor-pointer">
                <div className="flex items-center space-x-4">
                  <div 
                    className="w-5 h-5 rounded-full shadow-sm group-hover:shadow-md transition-shadow duration-200"
                    style={{ backgroundColor: entry.color }}
                  />
                  <span className="text-sm font-semibold text-gray-700">{entry.name}</span>
                </div>
                <span className="text-xl font-bold text-gray-900">{entry.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, delay: 0.7 }}
        className="card p-8"
      >
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Recent Activity</h3>
            <p className="text-gray-500 font-medium">Latest system events and updates</p>
          </div>
          <div className="w-14 h-14 bg-gradient-to-br from-indigo-100 to-indigo-200 rounded-2xl flex items-center justify-center shadow-glow">
            <Activity className="w-7 h-7 text-indigo-600" />
          </div>
        </div>
        <div className="space-y-6">
          {recentActivities.map((activity) => {
            const Icon = activity.icon
            return (
              <motion.div 
                key={activity.id} 
                className="flex items-start space-x-5 p-6 glass rounded-2xl hover:shadow-glow transition-all duration-300 group cursor-pointer"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-sm group-hover:shadow-md transition-all duration-300 flex-shrink-0`}>
                  <Icon className={`w-7 h-7 ${activity.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-900 leading-relaxed mb-2">{activity.message}</p>
                  <p className="text-xs text-gray-500 font-medium">{activity.timestamp}</p>
                </div>
                <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full opacity-50 group-hover:opacity-100 group-hover:scale-110 transition-all duration-300 flex-shrink-0 mt-2"></div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard