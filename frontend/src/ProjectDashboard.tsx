import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

export default function ProjectDashboard() {
  const { id } = useParams();
  const [project, setProject] = useState<any>(null);
  const token = localStorage.getItem('token') || '';

  useEffect(() => {
    fetch(`/projects/${id}/status`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(setProject);
  }, [id, token]);

  if (!project) return <div>Loading...</div>;

  return (
    <div>
      <h2>Project {id}</h2>
      <pre>{JSON.stringify(project, null, 2)}</pre>
    </div>
  );
}
