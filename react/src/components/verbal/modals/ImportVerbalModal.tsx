import React, { useState } from 'react';
import { Modal, Form, Input, message } from 'antd';
import type { ImportVerbalRequest } from '../../../types/api';
import { api } from '../../../services/api';

interface ImportVerbalModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const ImportVerbalModal: React.FC<ImportVerbalModalProps> = ({
  open,
  onClose,
  onSuccess,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      const payload: ImportVerbalRequest = {
        link: values.link,
        ownerList: values.ownerList.split(',').map((item: string) => item.trim()),
        datasetList: values.datasetList.split(',').map((item: string) => item.trim()),
      };

      await api.importVerbal(payload);
      message.success('导入话术成功');
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Import error:', error);
      message.error('导入话术失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="导入学城话术"
      open={open}
      onCancel={onClose}
      onOk={handleSubmit}
      confirmLoading={loading}
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="link"
          label="学城链接"
          rules={[{ required: true, message: '请输入学城链接' }]}
        >
          <Input placeholder="请输入学城链接" />
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
