import React, { useEffect, useState } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import { debounce } from 'lodash';
import { api } from '../../../services/api';
import type { DatasetInfo } from '../../../types/api';

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
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
  const [owners, setOwners] = useState<{ misId: string; avatarUrl: string }[]>([]);

  useEffect(() => {
    if (open) {
      fetchDatasets();
    }
  }, [open]);

  const fetchDatasets = async () => {
    try {
      const response = await api.getSuggestDatasets();
      if (response.code === 0 && response.data) {
        setDatasets(response.data);
      } else {
        message.error(response.msg || '获取数据集列表失败');
      }
    } catch (error) {
      message.error('获取数据集列表失败');
      console.error('Fetch datasets error:', error);
    }
  };

  const fetchOwners = async (query: string) => {
    try {
      const response = await api.getSuggestOwners(query);
      if (response.code === 0 && response.data) {
        setOwners(response.data);
      } else {
        message.error(response.msg || '获取负责人列表失败');
      }
    } catch (error) {
      message.error('获取负责人列表失败');
      console.error('Fetch owners error:', error);
    }
  };

  const debouncedFetchOwners = debounce(fetchOwners, 300);

  const handleOk = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      const response = await api.importVerbal(values);
      if (response.code === 0) {
        message.success('导入成功');
        form.resetFields();
        onSuccess();
        onClose();
      } else {
        message.error(response.msg || '导入失败');
      }
    } catch (error) {
      console.error('Submit error:', error);
      message.error('导入失败，请检查输入');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="导入学城话术"
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
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
          label="选择负责人"
          rules={[{ required: true, message: '请选择负责人' }]}
        >
          <Select
            mode="multiple"
            placeholder="请选择负责人"
            onSearch={debouncedFetchOwners}
            showSearch
            filterOption={false}
            options={owners.map(owner => ({
              label: owner.misId,
              value: owner.misId,
            }))}
          />
        </Form.Item>
        <Form.Item
          name="datasetList"
          label="选择数据集"
          rules={[{ required: true, message: '请选择数据集' }]}
        >
          <Select
            mode="multiple"
            placeholder="请选择数据集"
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
