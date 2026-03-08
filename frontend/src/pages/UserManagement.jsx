import React, { useState, useEffect } from 'react';
import { Table, Button, Select, message, Popconfirm, Card, Tag } from 'antd';
import { DeleteOutlined, UserOutlined } from '@ant-design/icons';
import { userService, authService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const currentUser = authService.getUser();

  useEffect(() => {
    // 检查是否是管理员
    if (currentUser?.role !== 'admin') {
      message.error('您没有权限访问此页面');
      navigate('/');
      return;
    }
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await userService.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('获取用户列表失败:', error);
      message.error('获取用户列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await userService.updateUserRole(userId, newRole);
      message.success('角色更新成功');
      fetchUsers();
    } catch (error) {
      console.error('更新角色失败:', error);
      message.error(error.response?.data?.detail || '更新角色失败');
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await userService.deleteUser(userId);
      message.success('用户删除成功');
      fetchUsers();
    } catch (error) {
      console.error('删除用户失败:', error);
      message.error(error.response?.data?.detail || '删除用户失败');
    }
  };

  const getRoleTag = (role) => {
    const roleMap = {
      admin: { color: 'red', text: '管理员' },
      editor: { color: 'blue', text: '编辑者' },
      viewer: { color: 'default', text: '查看者' },
    };
    const config = roleMap[role] || roleMap.viewer;
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: '姓名',
      dataIndex: 'full_name',
      key: 'full_name',
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role, record) => {
        if (record.id === currentUser?.id) {
          return getRoleTag(role);
        }
        return (
          <Select
            value={role}
            style={{ width: 120 }}
            onChange={(value) => handleRoleChange(record.id, value)}
          >
            <Select.Option value="admin">管理员</Select.Option>
            <Select.Option value="editor">编辑者</Select.Option>
            <Select.Option value="viewer">查看者</Select.Option>
          </Select>
        );
      },
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? '活跃' : '禁用'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => {
        if (record.id === currentUser?.id) {
          return <span style={{ color: '#999' }}>当前用户</span>;
        }
        return (
          <Popconfirm
            title="确定要删除此用户吗？"
            onConfirm={() => handleDeleteUser(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        );
      },
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card
        title={
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <UserOutlined style={{ marginRight: 8 }} />
            用户管理
          </div>
        }
        extra={
          <Button onClick={() => navigate('/')}>返回首页</Button>
        }
      >
        <Table
          columns={columns}
          dataSource={users}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default UserManagement;
