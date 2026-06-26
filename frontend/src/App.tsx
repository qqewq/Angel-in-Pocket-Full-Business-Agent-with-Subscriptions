import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import IdeaForm from './IdeaForm';
import ProjectDashboard from './ProjectDashboard';
import SubscriptionView from './SubscriptionView';
import Login from './Login';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/subscribe">Subscribe</Link>
      </nav>
      <Routes>
        <Route path="/" element={<IdeaForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/subscribe" element={<SubscriptionView />} />
        <Route path="/project/:id" element={<ProjectDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
