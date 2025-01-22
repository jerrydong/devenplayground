import React, { useState } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import type { VerbalItem, DatasetInfo } from '../../../types/api';
import { api } from '../../../services/api';

interface AddEditVerbalModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  type: 'add' | 'edit';
  initialValues?: VerbalItem;
}

export const AddEditVerbalModal: React.FC<AddEditVerbalModalProps> = ({
  open,
  onClose,
  onSuccess,
  type,
  initialValues,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      const payload = {
        ...values,
        id: initialValues?.id,
        contentList: [{ id: Date.now(), content: values.content }],
        ownerList: values.ownerList?.split(',').map((item: string) => item.trim()) || [],
        datasetList: values.datasetList?.split(',').map((item: string) => item.trim()) || [],
      };

      await api.addModifyVerbal(payload, type === 'edit');
      message.success(`${type === 'add' ? '新增' : '修改'}话术成功`);
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Submit error:', error);
      message.error(`${type === 'add' ? '新增' : '修改'}话术失败`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title={type === 'add' ? '新增话术' : '编辑话术'}
      open={open}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose}>
          取消
        </Button>,
        <Button key="submit" type="primary" loading={loading} onClick={handleSubmit}>
          确定
        </Button>,
      ]}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          name: initialValues?.name || '',
          content: initialValues?.contentList?.[0]?.content || '',
          ownerList: initialValues?.ownerList?.join(', ') || '',
          datasetList: initialValues?.datasetList?.map((ds: DatasetInfo) => ds.datasetId).join(', ') || '',
        }}
      >
        <Form.Item
          name="name"
          label="话术名称"
          rules={[{ required: true, message: '请输入话术名称' }]}
        >
          <Input disabled={type === 'edit'} placeholder="请输入话术名称" />
        </Form.Item>
        <Form.Item
          name="content"
          label="话术内容"
          rules={[{ required: true, message: '请输入话术内容' }]}
        >
          <Input.TextArea rows={4} placeholder="请输入话术内容" />
        </Form.Item>
        <Form.Item
          name="ownerList"
          label="负责人"
          rules={[{ required: true, message: '请输入负责人' }]}
        >
          <Input placeholder="请输入负责人，多个用逗号分隔" />
        </Form.Item>
        <Form.Item
          name="datasetList"
          label="数据集"
          rules={[{ required: true, message: '请输入数据集' }]}
        >
          <Input placeholder="请输入数据集，多个用逗号分隔" />
        </Form.Item>
      </Form>
    </Modal>
  );
};
