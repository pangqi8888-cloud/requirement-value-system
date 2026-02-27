import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
};

export default api;
