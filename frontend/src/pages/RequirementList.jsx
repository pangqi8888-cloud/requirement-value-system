import React, { useState, useEffect } from 'react';
import {
  Layout,
  Button,
  Table,
  Tag,
  Space,
  Modal,
  message,
  Select,
  Card,
  Statistic,
  Row,
  Col,
  Dropdown,
  Avatar,
} from 'antd';
import {
  PlusOutlined,
  ReloadOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  ExportOutlined,
  LogoutOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import RequirementForm from '../components/RequirementForm';
import ScoreCard from '../components/ScoreCard';
import { requirementService, authService } from '../services/api';

const { Header, Content } = Layout;
const { Option } = Select;

const RequirementList = () => {
  const [requirements, setRequirements] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formVisible, setFormVisible] = useState(false);
  const [editingRequirement, setEditingRequirement] = useState(null);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedRequirement, setSelectedRequirement] = useState(null);
  const [sortBy, setSortBy] = useState('total_score');
  const [order, setOrder] = useState('desc');
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    // 获取当前用户信息
    const user = authService.getUser();
    setCurrentUser(user);
    fetchRequirements();
  }, [sortBy, order]);

  // 导出需求
  const handleExport = async () => {
    try {
      const blob = await requirementService.exportRequirements('csv');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `requirements_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      message.success('导出成功！');
    } catch (error) {
      console.error('导出失败:', error);
      message.error('导出失败');
    }
  };

  // 登出
  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  // 用户菜单
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: `${currentUser?.full_name || currentUser?.username || '用户'} (${currentUser?.role === 'admin' ? '管理员' : currentUser?.role === 'editor' ? '编辑者' : '查看者'})`,
      disabled: true,
    },
    {
      type: 'divider',
    },
    ...(currentUser?.role === 'admin' ? [{
      key: 'users',
      icon: <UserOutlined />,
      label: '用户管理',
      onClick: () => navigate('/users'),
    }] : []),
    {
      key: 'templates',
      icon: <UserOutlined />,
      label: '模版管理',
      onClick: () => navigate('/templates'),
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout,
    },
  ];

  const fetchRequirements = async () => {
    setLoading(true);
    try {
      const response = await requirementService.getRequirements({
        sort_by: sortBy,
        order: order,
      });
      setRequirements(response.data);
    } catch (error) {
      console.error('获取需求列表失败:', error);
      message.error('获取需求列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    // 检查权限
    if (currentUser?.role === 'viewer') {
      message.error('您没有删除权限');
      return;
    }

    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个需求吗？',
      okText: '确定',
      cancelText: '取消',
      onOk: async () => {
        try {
          await requirementService.deleteRequirement(id);
          message.success('删除成功');
          fetchRequirements();
        } catch (error) {
          console.error('删除失败:', error);
          message.error(error.response?.data?.detail || '删除失败');
        }
      },
    });
  };

  const handleViewDetail = async (record) => {
    setSelectedRequirement(record);
    setDetailVisible(true);
  };

  const handleEdit = (record) => {
    setEditingRequirement(record);
    setFormVisible(true);
  };

  const handleCloseForm = () => {
    setFormVisible(false);
    setEditingRequirement(null);
  };

  const getTypeTag = (type) => {
    const typeMap = {
      feature: { color: 'blue', text: '功能需求' },
      optimization: { color: 'green', text: '优化需求' },
      bug_fix: { color: 'red', text: 'Bug修复' },
    };
    const config = typeMap[type] || { color: 'default', text: type };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const getStatusTag = (status) => {
    const statusMap = {
      pending: { color: 'default', text: '待评审' },
      approved: { color: 'blue', text: '已批准' },
      in_progress: { color: 'processing', text: '开发中' },
      completed: { color: 'success', text: '已完成' },
      rejected: { color: 'error', text: '已拒绝' },
    };
    const config = statusMap[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const getPriorityTag = (score) => {
    if (score >= 80) return <Tag color="red">高</Tag>;
    if (score >= 60) return <Tag color="orange">中</Tag>;
    return <Tag color="default">低</Tag>;
  };

  const columns = [
    {
      title: '排名',
      key: 'rank',
      width: 60,
      render: (_, __, index) => (
        <span style={{ fontWeight: 'bold', fontSize: 16 }}>#{index + 1}</span>
      ),
    },
    {
      title: '需求标题',
      dataIndex: 'title',
      key: 'title',
      width: 250,
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type) => getTypeTag(type),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => getStatusTag(status),
    },
    {
      title: '综合得分',
      dataIndex: 'total_score',
      key: 'total_score',
      width: 120,
      render: (score) => (
        <span style={{ fontSize: 18, fontWeight: 'bold', color: score >= 80 ? '#52c41a' : score >= 60 ? '#1890ff' : '#666' }}>
          {score.toFixed(1)}
        </span>
      ),
    },
    {
      title: '优先级',
      dataIndex: 'total_score',
      key: 'priority',
      width: 80,
      render: (score) => getPriorityTag(score),
    },
    {
      title: '普适性',
      dataIndex: 'universality_score',
      key: 'universality_score',
      width: 100,
      render: (score) => (score || 0).toFixed(1),
    },
    {
      title: '竞品对比',
      dataIndex: 'competitor_score',
      key: 'competitor_score',
      width: 100,
      render: (score) => (score || 0).toFixed(1),
    },
    {
      title: '收益潜力',
      dataIndex: 'revenue_score',
      key: 'revenue_score',
      width: 100,
      render: (score) => (score || 0).toFixed(1),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (time) => new Date(time).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      fixed: 'right',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleViewDetail(record)}
          >
            查看
          </Button>
          {currentUser?.role !== 'viewer' && (
            <>
              <Button
                type="link"
                icon={<EditOutlined />}
                onClick={() => handleEdit(record)}
              >
                编辑
              </Button>
              <Button
                type="link"
                danger
                icon={<DeleteOutlined />}
                onClick={() => handleDelete(record.id)}
              >
                删除
              </Button>
            </>
          )}
        </Space>
      ),
    },
  ];

  // 统计数据
  const stats = {
    total: requirements.length,
    high: requirements.filter((r) => r.total_score >= 80).length,
    medium: requirements.filter((r) => r.total_score >= 60 && r.total_score < 80).length,
    low: requirements.filter((r) => r.total_score < 60).length,
    avgScore: requirements.length > 0
      ? (requirements.reduce((sum, r) => sum + r.total_score, 0) / requirements.length).toFixed(1)
      : 0,
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', padding: '0 24px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '100%' }}>
          <h1 style={{ margin: 0, fontSize: 24 }}>需求价值评估系统</h1>
          <Space>
            <Button
              icon={<ExportOutlined />}
              onClick={handleExport}
            >
              导出
            </Button>
            {currentUser?.role !== 'viewer' && (
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setFormVisible(true)}
              >
                创建需求
              </Button>
            )}
            <Button icon={<ReloadOutlined />} onClick={fetchRequirements}>
              刷新
            </Button>
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <Button icon={<UserOutlined />}>
                {currentUser?.full_name || currentUser?.username || '用户'}
              </Button>
            </Dropdown>
          </Space>
        </div>
      </Header>

      <Content style={{ padding: 24 }}>
        {/* 统计卡片 */}
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic title="需求总数" value={stats.total} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="高优先级" value={stats.high} valueStyle={{ color: '#cf1322' }} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="中优先级" value={stats.medium} valueStyle={{ color: '#fa8c16' }} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="平均得分" value={stats.avgScore} valueStyle={{ color: '#1890ff' }} />
            </Card>
          </Col>
        </Row>

        {/* 排序控制 */}
        <Card style={{ marginBottom: 16 }}>
          <Space>
            <span>排序方式：</span>
            <Select value={sortBy} onChange={setSortBy} style={{ width: 150 }}>
              <Option value="total_score">综合得分</Option>
              <Option value="created_at">创建时间</Option>
            </Select>
            <Select value={order} onChange={setOrder} style={{ width: 120 }}>
              <Option value="desc">降序</Option>
              <Option value="asc">升序</Option>
            </Select>
          </Space>
        </Card>

        {/* 需求列表 */}
        <Card>
          <Table
            columns={columns}
            dataSource={requirements}
            rowKey="id"
            loading={loading}
            scroll={{ x: 1500 }}
            pagination={{
              pageSize: 10,
              showTotal: (total) => `共 ${total} 条`,
            }}
          />
        </Card>
      </Content>

      {/* 创建/编辑需求表单 */}
      <RequirementForm
        visible={formVisible}
        onClose={handleCloseForm}
        onSuccess={fetchRequirements}
        editingRequirement={editingRequirement}
      />

      {/* 需求详情 */}
      <Modal
        title="需求详情"
        open={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={null}
        width={1000}
      >
        {selectedRequirement && (
          <div>
            <Card title="基本信息" style={{ marginBottom: 16 }}>
              <p><strong>标题：</strong>{selectedRequirement.title}</p>
              <p><strong>类型：</strong>{getTypeTag(selectedRequirement.type)}</p>
              <p><strong>状态：</strong>{getStatusTag(selectedRequirement.status)}</p>
              <p><strong>描述：</strong>{selectedRequirement.description}</p>
              {selectedRequirement.business_background && (
                <p><strong>业务背景：</strong>{selectedRequirement.business_background}</p>
              )}
              {selectedRequirement.target_users && (
                <p><strong>目标用户：</strong>{selectedRequirement.target_users}</p>
              )}
              {selectedRequirement.expected_benefit && (
                <p><strong>预期收益：</strong>{selectedRequirement.expected_benefit}</p>
              )}
              {selectedRequirement.affected_user_count && (
                <p><strong>影响用户数：</strong>{selectedRequirement.affected_user_count.toLocaleString()}</p>
              )}
              {selectedRequirement.implementation_cost && (
                <p><strong>实现成本：</strong>{selectedRequirement.implementation_cost}</p>
              )}
            </Card>

            <ScoreCard requirement={selectedRequirement} />
          </div>
        )}
      </Modal>
    </Layout>
  );
};

export default RequirementList;
