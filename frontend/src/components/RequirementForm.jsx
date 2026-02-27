import React, { useState } from 'react';
import { Modal, Form, Input, Select, InputNumber, message } from 'antd';
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
          urgency_level: 3,
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
          <TextArea rows={4} placeholder="详细描述需求内容" />
        </Form.Item>

        <Form.Item
          label="业务背景"
          name="business_background"
        >
          <TextArea rows={3} placeholder="说明需求的业务背景和原因" />
        </Form.Item>

        <Form.Item
          label="目标用户"
          name="target_users"
        >
          <Input placeholder="例如：企业用户、个人用户、管理员等" />
        </Form.Item>

        <Form.Item
          label="预期收益"
          name="expected_benefit"
        >
          <TextArea
            rows={3}
            placeholder="描述预期带来的收益，如：提升转化率、增加营收、提高用户满意度等"
          />
        </Form.Item>

        <Form.Item
          label="影响用户数"
          name="affected_user_count"
        >
          <InputNumber
            min={0}
            style={{ width: '100%' }}
            placeholder="预计影响的用户数量"
          />
        </Form.Item>

        <Form.Item
          label="实现成本估算"
          name="implementation_cost"
        >
          <Select placeholder="选择实现成本">
            <Option value="低">低（1-3 人天）</Option>
            <Option value="中">中（3-10 人天）</Option>
            <Option value="高">高（10+ 人天）</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="紧急程度"
          name="urgency_level"
        >
          <Select>
            <Option value={1}>1 - 不紧急</Option>
            <Option value={2}>2 - 较低</Option>
            <Option value={3}>3 - 一般</Option>
            <Option value={4}>4 - 较高</Option>
            <Option value={5}>5 - 非常紧急</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="竞品对比信息"
          name="competitor_info"
        >
          <TextArea
            rows={3}
            placeholder="描述竞品的相关功能情况，如：竞品已有此功能、我们领先、我们落后等"
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default RequirementForm;
