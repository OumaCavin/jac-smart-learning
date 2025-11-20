import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Activity, Bot, Database, Settings, Users } from 'lucide-react'

import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Projects from './pages/Projects'
import Monitoring from './pages/Monitoring'
import SettingsPage from './pages/Settings'
import { useWebSocket } from './hooks/useWebSocket'
import { useAgentStore } from './store/agentStore'
import { useProjectStore } from './store/projectStore'

const App = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const { isConnected } = useWebSocket()
  const { agents, updateAgentStatus } = useAgentStore()
  const { projects, loadProjects } = useProjectStore()

  useEffect(() => {
    loadProjects()
  }, [loadProjects])

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      // Update agent statuses randomly for demo
      if (agents.length > 0) {
        const randomAgent = agents[Math.floor(Math.random() * agents.length)]
        if (randomAgent) {
          const statuses = ['idle', 'running', 'busy']
          const randomStatus = statuses[Math.floor(Math.random() * statuses.length)]
          updateAgentStatus(randomAgent.id, randomStatus)
        }
      }
    }, 10000) // Update every 10 seconds

    return () => clearInterval(interval)
  }, [agents, updateAgentStatus])

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        collapsed={sidebarCollapsed} 
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          connected={isConnected}
          onMenuToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="container mx-auto px-6 py-8"
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/monitoring" element={<Monitoring />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </motion.div>
        </main>
      </div>
    </div>
  )
}

export default App