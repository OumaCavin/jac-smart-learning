import { Bell, Menu, Wifi, WifiOff } from 'lucide-react'
import { motion } from 'framer-motion'

interface HeaderProps {
  connected: boolean
  onMenuToggle: () => void
}

const Header = ({ connected, onMenuToggle }: HeaderProps) => {
  return (
    <header className="bg-white/90 backdrop-blur-sm border-b border-gray-100 px-8 py-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <button
            onClick={onMenuToggle}
            className="lg:hidden p-3 rounded-xl hover:bg-gray-100 transition-all duration-200 transform hover:scale-105"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
          
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              Enterprise Multi-Agent System
            </h2>
            <p className="text-sm text-gray-500 font-medium">
              Real-time multi-agent orchestration and monitoring
            </p>
          </motion.div>
        </div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex items-center space-x-6"
        >
          {/* Connection Status */}
          <div className="flex items-center space-x-3 px-4 py-2 rounded-full bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200">
            {connected ? (
              <>
                <Wifi className="w-4 h-4 text-green-500" />
                <span className="text-sm text-green-700 font-semibold">Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-red-500" />
                <span className="text-sm text-red-700 font-semibold">Disconnected</span>
              </>
            )}
          </div>

          {/* Notifications */}
          <button className="relative p-3 rounded-xl hover:bg-gray-100 transition-all duration-200 transform hover:scale-105">
            <Bell className="w-5 h-5 text-gray-600" />
            <span className="absolute top-1 right-1 w-3 h-3 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center">
              <span className="text-xs text-white font-bold">3</span>
            </span>
          </button>

          {/* System Status Indicator */}
          <div className="flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-green-50 to-emerald-50 rounded-full border border-green-200">
            <div className="w-2 h-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-700 font-semibold">System Healthy</span>
          </div>
        </motion.div>
      </div>
    </header>
  )
}

export default Header