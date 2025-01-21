import React, { useState } from 'react';
import { Modal, Form, Select, message } from 'antd';
import { debounce } from 'lodash';
import { api } from '../../../services/api';
import type { BatchModifyRequest } from '../../../types/api';

interface ModifyOwnerModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (payload: BatchModifyRequest) => Promise<void>;
  basePayload: Omit<BatchModifyRequest, 'ownerList'>;
}

export const ModifyOwnerModal: React.FC<ModifyOwnerModalProps> = ({
  open,
  onClose,
  onConfirm,
  basePayload,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [owners, setOwners] = useState<{ misId: string; avatarUrl: string }[]>([]);

  const fetchOwners = async (query: string) => {
    try {
      setLoading(true);
      const response = await api.getSuggestOwners(query);
      if (response.code === 0 && response.data) {
        setOwners(response.data);
      } else {
        message.error(response.msg || '获取负责人列表失败');
      }
    } catch (error) {
      message.error('获取负责人列表失败');
      console.error('Fetch owners error:', error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedFetchOwners = debounce(fetchOwners, 300);

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      await onConfirm({
        ...basePayload,
        ownerList: values.ownerList,
      });
      form.resetFields();
      onClose();
    } catch (error) {
      console.error('Submit error:', error);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="修改负责人"
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
      confirmLoading={loading}
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="ownerList"
          label="选择负责人"
          rules={[{ required: true, message: '请选择负责人' }]}
        >
          <Select
            mode="multiple"
            placeholder="请选择负责人"
            loading={loading}
            onSearch={debouncedFetchOwners}
            showSearch
            filterOption={false}
            options={owners.map(owner => ({
              label: owner.misId,
              value: owner.misId,
            }))}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};
