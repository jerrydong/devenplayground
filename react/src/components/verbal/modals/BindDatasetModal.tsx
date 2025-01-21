import React, { useEffect, useState } from 'react';
import { Modal, Form, Select, message } from 'antd';
import { api } from '../../../services/api';
import type { DatasetInfo, BatchModifyRequest } from '../../../types/api';

interface BindDatasetModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (payload: BatchModifyRequest) => Promise<void>;
  basePayload: Omit<BatchModifyRequest, 'datasetList'>;
}

export const BindDatasetModal: React.FC<BindDatasetModalProps> = ({
  open,
  onClose,
  onConfirm,
  basePayload,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);

  useEffect(() => {
    if (open) {
      fetchDatasets();
    }
  }, [open]);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const response = await api.getSuggestDatasets();
      if (response.code === 0 && response.data) {
        setDatasets(response.data);
      } else {
        message.error(response.msg || '获取数据集列表失败');
      }
    } catch (error) {
      message.error('获取数据集列表失败');
      console.error('Fetch datasets error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      await onConfirm({
        ...basePayload,
        datasetList: values.datasetList,
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
      title="绑定数据集"
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
      confirmLoading={loading}
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="datasetList"
          label="选择数据集"
          rules={[{ required: true, message: '请选择数据集' }]}
        >
          <Select
            mode="multiple"
            placeholder="请选择数据集"
            loading={loading}
            options={datasets.map(ds => ({
              label: ds.datasetName,
              value: ds.datasetId,
            }))}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};
