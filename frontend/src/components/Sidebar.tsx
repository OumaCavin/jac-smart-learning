import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
}

const Sidebar = ({ collapsed, onToggle }: SidebarProps) => {
  const location = useLocation()

  const navigation = [
    {
      name: 'Dashboard',
      href: '/',
      icon: 'fa-house',
      current: location.pathname === '/'
    },
    {
      name: 'Agents',
      href: '/agents',
      icon: 'fa-robot',
      current: location.pathname === '/agents'
    },
    {
      name: 'Projects',
      href: '/projects',
      icon: 'fa-folder',
      current: location.pathname === '/projects'
    },
    {
      name: 'Monitoring',
      href: '/monitoring',
      icon: 'fa-chart-line',
      current: location.pathname === '/monitoring'
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: 'fa-gear',
      current: location.pathname === '/settings'
    }
  ]

  const sidebarClasses = `d-flex flex-column bg-white bg-opacity-95 backdrop-blur-sm border-end border-light transition-all duration-500 shadow-lg ${
    collapsed ? 'width-80' : 'width-300'
  }`

  return (
    <div className={sidebarClasses} style={{
      backdropFilter: 'blur(16px)',
      minHeight: '100vh'
    }}>
      <div className="d-flex align-items-center justify-content-between p-4 border-bottom border-light bg-gradient-to-r from-white to-light">
        <div className="d-flex align-items-center">
          <div className="rounded-3 p-3 me-3" style={{
            background: 'linear-gradient(135deg, #0d6efd, #6610f2)',
            boxShadow: '0 4px 15px rgba(13, 110, 253, 0.3)'
          }}>
            <i className="fas fa-robot text-white fs-4"></i>
          </div>
          {!collapsed && (
            <div>
              <h1 className="h4 fw-bold mb-0" style={{
                background: 'linear-gradient(45deg, #495057, #6c757d)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>EMAS</h1>
              <p className="small text-muted fw-semibold mb-0">Multi-Agent System</p>
            </div>
          )}
        </div>
        <button
          onClick={onToggle}
          className="btn btn-outline-secondary border-0 rounded-3 p-2"
          style={{ transition: 'all 0.2s' }}
        >
          {collapsed ? (
            <i className="fas fa-chevron-right text-muted"></i>
          ) : (
            <i className="fas fa-chevron-left text-muted"></i>
          )}
        </button>
      </div>

      <nav className="flex-grow-1 p-3">
        <div className="d-flex flex-column gap-2">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={`d-flex align-items-center p-3 rounded-3 text-decoration-none transition-all ${
                item.current 
                  ? 'bg-primary bg-opacity-10 text-primary fw-semibold' 
                  : 'text-muted hover:text-dark hover-bg-light'
              }`}
            >
              <i className={`fas ${item.icon} fs-5`}></i>
              {!collapsed && (
                <span className="ms-3 fw-medium">{item.name}</span>
              )}
            </Link>
          ))}
        </div>
      </nav>

      <div className="p-4 border-top border-light bg-gradient-to-r from-light to-white">
        <div className="d-flex align-items-center">
          <div className="rounded-3 p-3 me-3" style={{
            background: 'linear-gradient(135deg, #6c757d, #495057)',
            boxShadow: '0 2px 8px rgba(108, 117, 125, 0.2)'
          }}>
            <span className="small fw-bold text-white">CO</span>
          </div>
          {!collapsed && (
            <div className="flex-grow-1">
              <p className="small fw-semibold text-dark mb-1">
                Cavin Otieno
              </p>
              <p className="small text-muted mb-0">
                cavin.otieno012@gmail.com
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Sidebar