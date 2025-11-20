import { motion } from 'framer-motion'
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
      icon: 'fa-check-circle',
      color: 'text-success'
    },
    {
      id: 2,
      type: 'agent_start',
      message: 'Test Generation Agent started new test suite generation',
      timestamp: '5 minutes ago',
      icon: 'fa-bolt',
      color: 'text-primary'
    },
    {
      id: 3,
      type: 'project_created',
      message: 'New project "AI Chatbot" created with 5 agents assigned',
      timestamp: '12 minutes ago',
      icon: 'fa-code',
      color: 'text-info'
    },
    {
      id: 4,
      type: 'warning',
      message: 'Security Scanning Agent detected potential vulnerabilities',
      timestamp: '18 minutes ago',
      icon: 'fa-exclamation-triangle',
      color: 'text-warning'
    }
  ]

  return (
    <div className="min-vh-100" style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      backgroundAttachment: 'fixed'
    }}>
      <div className="container-fluid py-5">
        {/* Header */}
        <div className="mb-5">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="card border-0 shadow-lg backdrop-filter backdrop-blur bg-white bg-opacity-90 rounded-4"
          >
            <div className="card-body p-5">
              <h1 className="display-4 fw-bold mb-3" style={{
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                Dashboard
              </h1>
              <p className="lead text-muted mb-0">
                Monitor your multi-agent system in real-time
              </p>
            </div>
          </motion.div>
        </div>

        {/* Key Metrics */}
        <div className="row g-4 mb-5">
          <div className="col-12 col-md-6 col-lg-3">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="card border-0 shadow-lg h-100 rounded-4 overflow-hidden cursor-pointer transition-all hover:scale-105"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="position-absolute top-0 start-0 w-100" style={{ height: '4px', background: 'linear-gradient(90deg, #0d6efd, #6610f2)' }}></div>
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between">
                  <div>
                    <p className="text-uppercase fw-bold text-muted small mb-2">Active Agents</p>
                    <h2 className="display-4 fw-bold text-dark mb-2">{activeAgents}</h2>
                    <p className="text-muted small mb-0">of {totalAgents} total</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #e3f2fd, #bbdefb)',
                    boxShadow: '0 4px 15px rgba(13, 110, 253, 0.2)'
                  }}>
                    <i className="fas fa-robot fs-2 text-primary"></i>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="col-12 col-md-6 col-lg-3">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="card border-0 shadow-lg h-100 rounded-4 overflow-hidden cursor-pointer transition-all hover:scale-105"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="position-absolute top-0 start-0 w-100" style={{ height: '4px', background: 'linear-gradient(90deg, #198754, #20c997)' }}></div>
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between">
                  <div>
                    <p className="text-uppercase fw-bold text-muted small mb-2">Active Projects</p>
                    <h2 className="display-4 fw-bold text-dark mb-2">{totalProjects}</h2>
                    <p className="text-muted small mb-0">running tasks</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #d1edff, #b8e6ff)',
                    boxShadow: '0 4px 15px rgba(25, 135, 84, 0.2)'
                  }}>
                    <i className="fas fa-project-diagram fs-2 text-success"></i>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="col-12 col-md-6 col-lg-3">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="card border-0 shadow-lg h-100 rounded-4 overflow-hidden cursor-pointer transition-all hover:scale-105"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="position-absolute top-0 start-0 w-100" style={{ height: '4px', background: 'linear-gradient(90deg, #6f42c1, #e83e8c)' }}></div>
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between">
                  <div>
                    <p className="text-uppercase fw-bold text-muted small mb-2">Completed Tasks</p>
                    <h2 className="display-4 fw-bold text-dark mb-2">{completedTasks}</h2>
                    <p className="text-muted small mb-0">this week</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #f3e5f5, #e1bee7)',
                    boxShadow: '0 4px 15px rgba(111, 66, 193, 0.2)'
                  }}>
                    <i className="fas fa-check-circle fs-2 text-warning"></i>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="col-12 col-md-6 col-lg-3">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="card border-0 shadow-lg h-100 rounded-4 overflow-hidden cursor-pointer transition-all hover:scale-105"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="position-absolute top-0 start-0 w-100" style={{ height: '4px', background: 'linear-gradient(90deg, #fd7e14, #dc3545)' }}></div>
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between">
                  <div>
                    <p className="text-uppercase fw-bold text-muted small mb-2">Pending Tasks</p>
                    <h2 className="display-4 fw-bold text-dark mb-2">{pendingTasks}</h2>
                    <p className="text-muted small mb-0">in queue</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #fff3cd, #ffe69c)',
                    boxShadow: '0 4px 15px rgba(253, 126, 20, 0.2)'
                  }}>
                    <i className="fas fa-clock fs-2 text-danger"></i>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="row g-4 mb-5">
          {/* Performance Chart */}
          <div className="col-12 col-lg-8">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="card border-0 shadow-lg rounded-4"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between mb-4">
                  <div>
                    <h3 className="h3 fw-bold text-dark mb-2">System Performance</h3>
                    <p className="text-muted mb-0">Real-time task and agent metrics</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #d4edda, #c3e6cb)',
                    boxShadow: '0 4px 15px rgba(25, 135, 84, 0.2)'
                  }}>
                    <i className="fas fa-chart-line fs-4 text-success"></i>
                  </div>
                </div>
                <div style={{ height: '320px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={performanceData}>
                      <defs>
                        <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#0d6efd" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#0d6efd" stopOpacity={0.1}/>
                        </linearGradient>
                        <linearGradient id="colorAgents" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#198754" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#198754" stopOpacity={0.1}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" />
                      <XAxis 
                        dataKey="time" 
                        stroke="#6c757d" 
                        fontSize={12}
                        fontWeight={500}
                      />
                      <YAxis 
                        stroke="#6c757d" 
                        fontSize={12}
                        fontWeight={500}
                      />
                      <Tooltip 
                        contentStyle={{
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          border: '1px solid rgba(222, 226, 230, 0.8)',
                          borderRadius: '12px',
                          backdropFilter: 'blur(10px)',
                          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)',
                          fontSize: '14px'
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="tasks"
                        stroke="#0d6efd"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorTasks)"
                        name="Tasks Completed"
                      />
                      <Area
                        type="monotone"
                        dataKey="agents"
                        stroke="#198754"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorAgents)"
                        name="Active Agents"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Agent Status Chart */}
          <div className="col-12 col-lg-4">
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="card border-0 shadow-lg rounded-4 h-100"
              style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
            >
              <div className="card-body p-4">
                <div className="d-flex align-items-center justify-content-between mb-4">
                  <div>
                    <h3 className="h4 fw-bold text-dark mb-2">Agent Status</h3>
                    <p className="text-muted mb-0">Current agent states</p>
                  </div>
                  <div className="rounded-3 p-3" style={{ 
                    background: 'linear-gradient(135deg, #e3f2fd, #bbdefb)',
                    boxShadow: '0 4px 15px rgba(13, 110, 253, 0.2)'
                  }}>
                    <i className="fas fa-robot fs-4 text-primary"></i>
                  </div>
                </div>
                <div style={{ height: '200px', marginBottom: '24px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={agentStatusData}
                        cx="50%"
                        cy="50%"
                        innerRadius={30}
                        outerRadius={70}
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
                          border: '1px solid rgba(222, 226, 230, 0.8)',
                          borderRadius: '12px',
                          backdropFilter: 'blur(10px)',
                          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)',
                          fontSize: '14px'
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="d-flex flex-column gap-3">
                  {agentStatusData.map((entry, index) => (
                    <div key={index} className="d-flex align-items-center justify-content-between p-3 rounded-3 hover:bg-light transition-all cursor-pointer">
                      <div className="d-flex align-items-center">
                        <div 
                          className="rounded-circle me-3"
                          style={{ 
                            width: '12px', 
                            height: '12px', 
                            backgroundColor: entry.color,
                            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                          }}
                        ></div>
                        <span className="fw-semibold text-dark">{entry.name}</span>
                      </div>
                      <span className="h5 fw-bold text-dark">{entry.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="card border-0 shadow-lg rounded-4"
          style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.95)' }}
        >
          <div className="card-body p-5">
            <div className="d-flex align-items-center justify-content-between mb-5">
              <div>
                <h3 className="h3 fw-bold text-dark mb-2">Recent Activity</h3>
                <p className="text-muted mb-0">Latest system events and updates</p>
              </div>
              <div className="rounded-3 p-3" style={{ 
                background: 'linear-gradient(135deg, #e8eaf6, #c5cae9)',
                boxShadow: '0 4px 15px rgba(103, 58, 183, 0.2)'
              }}>
                <i className="fas fa-history fs-4 text-info"></i>
              </div>
            </div>
            <div className="d-flex flex-column gap-4">
              {recentActivities.map((activity) => (
                <motion.div 
                  key={activity.id} 
                  className="d-flex align-items-start p-4 rounded-4 border-0 shadow-sm hover:shadow transition-all cursor-pointer"
                  style={{ backdropFilter: 'blur(16px)', background: 'rgba(255, 255, 255, 0.8)' }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="rounded-3 p-3 me-4 flex-shrink-0" style={{ 
                    background: 'linear-gradient(135deg, #f8f9fa, #e9ecef)',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
                  }}>
                    <i className={`fas ${activity.icon} fs-5 ${activity.color}`}></i>
                  </div>
                  <div className="flex-grow-1">
                    <p className="fw-semibold text-dark mb-2 lh-base">{activity.message}</p>
                    <p className="text-muted small mb-0">{activity.timestamp}</p>
                  </div>
                  <div className="rounded-circle flex-shrink-0 mt-2" style={{ 
                    width: '12px', 
                    height: '12px',
                    background: 'linear-gradient(45deg, #0d6efd, #6610f2)',
                    opacity: '0.7'
                  }}></div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard