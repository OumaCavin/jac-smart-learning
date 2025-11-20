import React from 'react';

const Projects: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h1>📁 Project Management</h1>
      <div style={{ background: '#f0fff0', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
        <p>Organize and manage your AI projects here. This page provides project overview and management capabilities.</p>
        <ul style={{ marginTop: '15px', paddingLeft: '20px' }}>
          <li>View all active projects</li>
          <li>Create new AI projects</li>
          <li>Manage project resources</li>
          <li>Track project progress</li>
        </ul>
      </div>
    </div>
  );
};

export default Projects;