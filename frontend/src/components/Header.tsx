import { motion } from 'framer-motion'

interface HeaderProps {
  connected: boolean
  onMenuToggle: () => void
}

const Header = ({ connected, onMenuToggle }: HeaderProps) => {
  return (
    <header className="bg-white bg-opacity-90 border-bottom border-light px-4 py-4 shadow-sm" style={{ backdropFilter: 'blur(16px)' }}>
      <div className="d-flex align-items-center justify-content-between">
        <div className="d-flex align-items-center">
          <motion.button
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            onClick={onMenuToggle}
            className="btn btn-outline-secondary border-0 rounded-3 p-3 d-lg-none me-3"
            style={{ transition: 'all 0.2s' }}
          >
            <i className="fas fa-bars text-muted"></i>
          </motion.button>
          
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <h2 className="h3 fw-bold mb-1" style={{
              background: 'linear-gradient(45deg, #495057, #6c757d)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>
              Enterprise Multi-Agent System
            </h2>
            <p className="small text-muted fw-medium mb-0">
              Real-time multi-agent orchestration and monitoring
            </p>
          </motion.div>
        </div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="d-flex align-items-center gap-3"
        >
          {/* Connection Status */}
          <div className="d-flex align-items-center gap-2 px-3 py-2 rounded-pill" style={{
            background: connected 
              ? 'linear-gradient(135deg, #d4edda, #c3e6cb)' 
              : 'linear-gradient(135deg, #f8d7da, #f5c6cb)',
            border: '1px solid rgba(0,0,0,0.1)'
          }}>
            <i className={`fas ${connected ? 'fa-wifi text-success' : 'fa-wifi-slash text-danger'}`}></i>
            <span className={`small fw-semibold ${connected ? 'text-success' : 'text-danger'}`}>
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Notifications */}
          <button className="btn btn-outline-secondary border-0 rounded-3 p-3 position-relative" style={{ transition: 'all 0.2s' }}>
            <i className="fas fa-bell text-muted"></i>
            <span className="position-absolute top-0 end-0 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '0.65rem' }}>
              3
            </span>
          </button>

          {/* System Status Indicator */}
          <div className="d-flex align-items-center gap-2 px-3 py-2 rounded-pill" style={{
            background: 'linear-gradient(135deg, #d1edff, #b8e6ff)',
            border: '1px solid rgba(25, 135, 84, 0.2)'
          }}>
            <div className="rounded-circle" style={{
              width: '8px',
              height: '8px',
              background: 'linear-gradient(45deg, #198754, #20c997)',
              animation: 'pulse 2s infinite'
            }}></div>
            <span className="small text-success fw-semibold">System Healthy</span>
          </div>
        </motion.div>
      </div>
    </header>
  )
}

export default Header