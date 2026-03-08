import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Switch, message, Popconfirm, Card, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, FileTextOutlined } from '@ant-design/icons';
import { templateService, authService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const TemplateManagement = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const currentUser = authService.getUser();

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await templateService.getTemplates();
      setTemplates(response.data);
    } catch (error) {
      console.error('获取模版列表失败:', error);
      message.error('获取模版列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingTemplate(null);
    form.resetFields();
    form.setFieldsValue({
      fields_config: JSON.stringify({
        title: { required: true, default: '' },
        description: { required: true, default: '' },
        type: { required: true, default: 'feature' },
        business_background: { required: false, default: '' },
        expected_benefit: { required: false, default: '' },
        implementation_cost: { required: false, default: '' },
      }, null, 2),
      is_default: false,
    });
    setModalVisible(true);
  };

  const handleEdit = (template) => {
    setEditingTemplate(template);
    form.setFieldsValue({
      name: template.name,
      description: template.description,
      fields_config: JSON.stringify(template.fields_config, null, 2),
      is_default: template.is_default,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await templateService.deleteTemplate(id);
      message.success('模版删除成功');
      fetchTemplates();
    } catch (error) {
      console.error('删除模版失败:', error);
      message.error(error.response?.data?.detail || '删除模版失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();

      // 解析 JSON 配置
      let fieldsConfig;
      try {
        fieldsConfig = JSON.parse(values.fields_config);
      } catch (e) {
        message.error('字段配置格式错误，请输入有效的 JSON');
        return;
      }

      const data = {
        name: values.name,
        description: values.description,
        fields_config: fieldsConfig,
        is_default: values.is_default || false,
      };

      if (editingTemplate) {
        await templateService.updateTemplate(editingTemplate.id, data);
        message.success('模版更新成功');
      } else {
        await templateService.createTemplate(data);
        message.success('模版创建成功');
      }

      setModalVisible(false);
      fetchTemplates();
    } catch (error) {
      if (error.errorFields) {
        return;
      }
      console.error('保存模版失败:', error);
      message.error(error.response?.data?.detail || '保存模版失败');
    }
  };

  const canEdit = (template) => {
    return currentUser?.role === 'admin' || template.created_by === currentUser?.id;
  };

  const canDelete = () => {
    return currentUser?.role === 'admin';
  };

  const canCreate = () => {
    return currentUser?.role === 'admin' || currentUser?.role === 'editor';
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '模版名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '默认模版',
      dataIndex: 'is_default',
      key: 'is_default',
      render: (isDefault) => (isDefault ? '是' : '否'),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          {canEdit(record) && (
            <Button
              type="link"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            >
              编辑
            </Button>
          )}
          {canDelete() && (
            <Popconfirm
              title="确定要删除此模版吗？"
              onConfirm={() => handleDelete(record.id)}
              okText="确定"
              cancelText="取消"
            >
              <Button type="link" danger icon={<DeleteOutlined />}>
                删除
              </Button>
            </Popconfirm>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card
        title={
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <FileTextOutlined style={{ marginRight: 8 }} />
            需求模版管理
          </div>
        }
        extra={
          <Space>
            {canCreate() && (
              <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                新建模版
              </Button>
            )}
            <Button onClick={() => navigate('/')}>返回首页</Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={templates}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingTemplate ? '编辑模版' : '新建模版'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={700}
        okText="保存"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="模版名称"
            rules={[{ required: true, message: '请输入模版名称' }]}
          >
            <Input placeholder="例如：标准需求模版" />
          </Form.Item>

          <Form.Item name="description" label="描述">
            <Input.TextArea rows={2} placeholder="模版的用途说明" />
          </Form.Item>

          <Form.Item
            name="fields_config"
            label="字段配置（JSON格式）"
            rules={[{ required: true, message: '请输入字段配置' }]}
            extra="配置每个字段是否必填及默认值"
          >
            <Input.TextArea
              rows={12}
              placeholder='{"title": {"required": true, "default": ""}}'
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>

          <Form.Item name="is_default" label="设为默认模版" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TemplateManagement;
