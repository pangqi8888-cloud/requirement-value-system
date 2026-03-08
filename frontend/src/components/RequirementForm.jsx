import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import { requirementService, templateService } from '../services/api';

const { TextArea } = Input;
const { Option } = Select;

const RequirementForm = ({ visible, onClose, onSuccess, editingRequirement = null }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const isEditMode = !!editingRequirement;

  // 获取模版列表
  useEffect(() => {
    if (visible && !isEditMode) {
      fetchTemplates();
    }
  }, [visible, isEditMode]);

  const fetchTemplates = async () => {
    try {
      const response = await templateService.getTemplates();
      setTemplates(response.data);
    } catch (error) {
      console.error('获取模版列表失败:', error);
    }
  };

  // 当编辑需求变化时，更新表单
  useEffect(() => {
    if (editingRequirement) {
      form.setFieldsValue({
        title: editingRequirement.title,
        type: editingRequirement.type,
        description: editingRequirement.description,
        business_background: editingRequirement.business_background,
        expected_benefit: editingRequirement.expected_benefit,
        implementation_cost: editingRequirement.implementation_cost,
      });
    } else {
      form.resetFields();
      setSelectedTemplate(null);
    }
  }, [editingRequirement, form]);

  // 应用模版
  const handleTemplateChange = (templateId) => {
    if (!templateId) {
      setSelectedTemplate(null);
      return;
    }

    const template = templates.find(t => t.id === templateId);
    if (template && template.fields_config) {
      setSelectedTemplate(template);

      // 应用模版的默认值
      const config = template.fields_config;
      const values = {};

      Object.keys(config).forEach(field => {
        if (config[field].default !== undefined && config[field].default !== '') {
          values[field] = config[field].default;
        }
      });

      form.setFieldsValue(values);
      message.success(`已应用模版：${template.name}`);
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      if (isEditMode) {
        await requirementService.updateRequirement(editingRequirement.id, values);
        message.success('需求更新成功，AI 重新评估已完成！');
      } else {
        await requirementService.createRequirement(values);
        message.success('需求创建成功，AI 评估已完成！');
      }

      form.resetFields();
      setSelectedTemplate(null);
      onSuccess();
      onClose();
    } catch (error) {
      console.error(isEditMode ? '更新失败:' : '创建失败:', error);
      if (error.response) {
        message.error(`${isEditMode ? '更新' : '创建'}失败: ${error.response.data.detail || '未知错误'}`);
      } else if (error.errorFields) {
        message.error('请检查表单填写');
      } else {
        message.error(`${isEditMode ? '更新' : '创建'}失败，请重试`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title={isEditMode ? "编辑需求" : "创建新需求"}
      open={visible}
      onOk={handleSubmit}
      onCancel={onClose}
      confirmLoading={loading}
      width={800}
      okText={isEditMode ? "保存并重新评估" : "创建并评估"}
      cancelText="取消"
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          type: 'feature',
        }}
      >
        {!isEditMode && templates.length > 0 && (
          <Form.Item label="选择模版（可选）">
            <Select
              placeholder="选择一个模版快速填充表单"
              allowClear
              onChange={handleTemplateChange}
            >
              {templates.map(template => (
                <Option key={template.id} value={template.id}>
                  {template.name} {template.is_default && '(默认)'}
                </Option>
              ))}
            </Select>
          </Form.Item>
        )}

        <Form.Item
          label="需求标题"
          name="title"
          rules={[{ required: true, message: '请输入需求标题' }]}
        >
          <Input placeholder="简要描述需求" />
        </Form.Item>

        <Form.Item
          label="需求类型"
          name="type"
          rules={[{ required: true, message: '请选择需求类型' }]}
        >
          <Select>
            <Option value="feature">功能需求</Option>
            <Option value="optimization">优化需求</Option>
            <Option value="bug_fix">Bug 修复</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="需求描述"
          name="description"
          rules={[{ required: true, message: '请输入需求描述' }]}
        >
          <TextArea rows={4} placeholder="详细描述需求内容、功能点、实现方案等" />
        </Form.Item>

        <Form.Item
          label="业务背景"
          name="business_background"
        >
          <TextArea rows={3} placeholder="说明需求的业务背景和原因，为什么要做这个需求" />
        </Form.Item>

        <Form.Item
          label="预期收益"
          name="expected_benefit"
        >
          <TextArea
            rows={3}
            placeholder="描述预期带来的收益，如：提升安全能力、增加营收、提高用户满意度等"
          />
        </Form.Item>

        <Form.Item
          label="实现成本估算"
          name="implementation_cost"
        >
          <TextArea
            rows={2}
            placeholder="描述预计需要的开发工作量，如：2周、3个人月、需要额外采购设备等"
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default RequirementForm;
