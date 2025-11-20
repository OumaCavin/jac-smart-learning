-- JAC Smart Learning Database Initialization
-- This script creates the initial database structure

-- Create user (if not exists)
CREATE USER IF NOT EXISTS cavin WITH PASSWORD '';

-- Create database (if not exists)  
CREATE DATABASE jac_learning OWNER cavin;

-- Connect to jac_learning database
\c jac_learning;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT users_email_check CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT users_username_check CHECK (length(username) >= 3)
);

-- Create user profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(255),
    learning_preferences JSONB DEFAULT '{}',
    progress_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create learning sessions table
CREATE TABLE IF NOT EXISTS learning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL, -- 'lesson', 'practice', 'quiz', 'project'
    language VARCHAR(20) NOT NULL, -- 'jac', 'python', 'javascript', etc.
    topic VARCHAR(100) NOT NULL,
    content JSONB NOT NULL DEFAULT '{}',
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'paused', 'failed'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    score DECIMAL(5,2), -- 0.00 to 100.00
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create code submissions table
CREATE TABLE IF NOT EXISTS code_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES learning_sessions(id) ON DELETE CASCADE,
    language VARCHAR(20) NOT NULL,
    code_content TEXT NOT NULL,
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    execution_result JSONB DEFAULT '{}',
    quality_score DECIMAL(5,2), -- 0.00 to 100.00
    ccg_analysis JSONB DEFAULT '{}', -- Code Context Graph analysis results
    quality_assessment JSONB DEFAULT '{}', -- Quality assessment results
    execution_time_ms INTEGER,
    memory_usage_mb DECIMAL(8,2),
    errors TEXT,
    status VARCHAR(20) DEFAULT 'submitted', -- 'submitted', 'running', 'completed', 'failed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create agent tasks table (for multi-agent system)
CREATE TABLE IF NOT EXISTS agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL, -- 'code_analysis', 'test_generation', 'security_scan', etc.
    agent_type VARCHAR(50) NOT NULL, -- 'code_agent', 'test_agent', 'security_agent', etc.
    task_data JSONB NOT NULL DEFAULT '{}',
    priority INTEGER DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed', 'cancelled'
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    result JSONB DEFAULT '{}',
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create system metrics table
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,6) NOT NULL,
    metric_unit VARCHAR(20),
    labels JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_type ON learning_sessions(session_type);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_language ON learning_sessions(language);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_status ON learning_sessions(status);
CREATE INDEX IF NOT EXISTS idx_code_submissions_user_id ON code_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_session_id ON code_submissions(session_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_language ON code_submissions(language);
CREATE INDEX IF NOT EXISTS idx_code_submissions_status ON code_submissions(status);
CREATE INDEX IF NOT EXISTS idx_agent_tasks_user_id ON agent_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_tasks_type ON agent_tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_agent_tasks_status ON agent_tasks(status);
CREATE INDEX IF NOT EXISTS idx_system_metrics_name ON system_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_learning_sessions_updated_at BEFORE UPDATE ON learning_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_code_submissions_updated_at BEFORE UPDATE ON code_submissions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agent_tasks_updated_at BEFORE UPDATE ON agent_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin user (password: admin123)
INSERT INTO users (username, email, password_hash, first_name, last_name, is_active, is_verified)
VALUES (
    'admin',
    'admin@jac-learning.com',
    crypt('admin123', gen_salt('bf')),
    'Admin',
    'User',
    true,
    true
) ON CONFLICT (username) DO NOTHING;

-- Insert sample learning content
INSERT INTO learning_sessions (user_id, session_type, language, topic, content, progress, status)
SELECT 
    u.id,
    'lesson',
    'jac',
    'Introduction to JAC Programming',
    '{"title": "Basic JAC Concepts", "content": "Learn the fundamentals of JAC programming language", "examples": ["hello_world.jac", "variables.jac"]}',
    0,
    'active'
FROM users u WHERE u.username = 'admin'
ON CONFLICT DO NOTHING;

COMMIT;