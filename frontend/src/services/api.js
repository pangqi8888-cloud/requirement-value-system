import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 自动添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理 401 错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证服务
export const authService = {
  // 登录
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      // 获取用户信息
      const userResponse = await api.get('/auth/me');
      localStorage.setItem('user', JSON.stringify(userResponse.data));
    }
    
    return response.data;
  },

  // 注册
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // 获取当前用户
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // 登出
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  // 检查是否已登录
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  // 获取存储的用户信息
  getUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
};

export const requirementService = {
  // 创建需求
  createRequirement: (data) => api.post('/requirements/', data),

  // 获取需求列表
  getRequirements: (params = {}) => api.get('/requirements/', { params }),

  // 获取单个需求
  getRequirement: (id) => api.get(`/requirements/${id}`),

  // 更新需求
  updateRequirement: (id, data) => api.put(`/requirements/${id}`, data),

  // 删除需求
  deleteRequirement: (id) => api.delete(`/requirements/${id}`),

  // 导出需求
  exportRequirements: (format = 'csv') => {
    const token = localStorage.getItem('access_token');
    const url = `${API_BASE_URL}/requirements/export?format=${format}`;
    const link = document.createElement('a');
    link.href = url;
    if (token) {
      link.setAttribute('Authorization', `Bearer ${token}`);
    }
    // 通过 fetch 下载文件
    return fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }).then(response => response.blob());
  },
};

export default api;
