import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '../utils/cn'
import {
  Home,
  Bot,
  FolderOpen,
  Activity,
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

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
      icon: Home,
      current: location.pathname === '/'
    },
    {
      name: 'Agents',
      href: '/agents',
      icon: Bot,
      current: location.pathname === '/agents'
    },
    {
      name: 'Projects',
      href: '/projects',
      icon: FolderOpen,
      current: location.pathname === '/projects'
    },
    {
      name: 'Monitoring',
      href: '/monitoring',
      icon: Activity,
      current: location.pathname === '/monitoring'
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: Settings,
      current: location.pathname === '/settings'
    }
  ]

  return (
    <div className={cn(
      'flex flex-col bg-white/95 backdrop-blur-sm border-r border-gray-100 transition-all duration-500 shadow-lg',
      collapsed ? 'w-20' : 'w-72'
    )}>
      <div className="flex items-center justify-between h-20 px-6 border-b border-gray-100 bg-gradient-to-r from-white to-gray-50">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
          {!collapsed && (
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">EMAS</h1>
              <p className="text-xs text-gray-500 font-medium">Multi-Agent System</p>
            </div>
          )}
        </div>
        <button
          onClick={onToggle}
          className="p-2 rounded-xl hover:bg-gray-100 transition-all duration-200 transform hover:scale-105"
        >
          {collapsed ? (
            <ChevronRight className="w-4 h-4 text-gray-600" />
          ) : (
            <ChevronLeft className="w-4 h-4 text-gray-600" />
          )}
        </button>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                item.current ? 'sidebar-nav-item-active' : 'sidebar-nav-item-inactive'
              )}
            >
              <Icon
                className={cn(
                  'flex-shrink-0 w-5 h-5',
                  item.current ? 'text-blue-700' : 'text-gray-400 group-hover:text-gray-600'
                )}
              />
              {!collapsed && (
                <span className="ml-3 font-medium">{item.name}</span>
              )}
            </Link>
          )
        })}
      </nav>

      <div className="p-6 border-t border-gray-100 bg-gradient-to-r from-gray-50 to-white">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-r from-gray-400 to-gray-500 rounded-2xl flex items-center justify-center shadow-md">
            <span className="text-sm font-bold text-white">CO</span>
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-900 truncate">
                Cavin Otieno
              </p>
              <p className="text-xs text-gray-500 truncate">
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