import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import RequirementList from './pages/RequirementList';
import Login from './pages/Login';
import UserManagement from './pages/UserManagement';
import TemplateManagement from './pages/TemplateManagement';
import { authService } from './services/api';

// 私有路由组件
const PrivateRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);

  if (isAuthenticated === null) {
    return <div>加载中...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

// 登出组件
const Logout = () => {
  useEffect(() => {
    authService.logout();
    window.location.href = '/login';
  }, []);
  return null;
};

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <RequirementList />
              </PrivateRoute>
            }
          />
          <Route
            path="/users"
            element={
              <PrivateRoute>
                <UserManagement />
              </PrivateRoute>
            }
          />
          <Route
            path="/templates"
            element={
              <PrivateRoute>
                <TemplateManagement />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
