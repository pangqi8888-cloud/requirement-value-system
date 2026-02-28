import React, { useState } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import { requirementService } from '../services/api';

const { TextArea } = Input;
const { Option } = Select;

const RequirementForm = ({ visible, onClose, onSuccess }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      await requirementService.createRequirement(values);

      message.success('需求创建成功，AI 评估已完成！');
      form.resetFields();
      onSuccess();
      onClose();
    } catch (error) {
      console.error('创建失败:', error);
      if (error.response) {
        message.error(`创建失败: ${error.response.data.detail || '未知错误'}`);
      } else if (error.errorFields) {
        message.error('请检查表单填写');
      } else {
        message.error('创建失败，请重试');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="创建新需求"
      open={visible}
      onOk={handleSubmit}
      onCancel={onClose}
      confirmLoading={loading}
      width={800}
      okText="创建并评估"
      cancelText="取消"
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          type: 'feature',
        }}
      >
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
