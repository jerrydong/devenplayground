import React, { useState, useEffect } from 'react';
import { Modal, Select, message } from 'antd';
import type { BatchModifyRequest, DatasetInfo } from '../../../types/api';
import { api } from '../../../services/api';

interface BindDatasetModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (payload: BatchModifyRequest) => Promise<void>;
  basePayload: BatchModifyRequest;
}

export const BindDatasetModal: React.FC<BindDatasetModalProps> = ({
  open,
  onClose,
  onConfirm,
  basePayload,
}) => {
  const [loading, setLoading] = useState(false);
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
  const [selectedDatasets, setSelectedDatasets] = useState<string[]>([]);

  useEffect(() => {
    if (open) {
      fetchDatasets();
    }
  }, [open]);

  const fetchDatasets = async () => {
    try {
      const response = await api.getSuggestDatasets();
      if (response.code === 0) {
        setDatasets(response.data);
      }
    } catch (error) {
      console.error('Fetch datasets error:', error);
      message.error('获取数据集列表失败');
    }
  };

  const handleConfirm = async () => {
    if (selectedDatasets.length === 0) {
      message.warning('请选择数据集');
      return;
    }

    try {
      setLoading(true);
      await onConfirm({
        ...basePayload,
        datasetList: selectedDatasets,
      });
      onClose();
    } catch (error) {
      console.error('Bind dataset error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="绑定数据集"
      open={open}
      onCancel={onClose}
      onOk={handleConfirm}
      confirmLoading={loading}
    >
      <Select
        mode="multiple"
        style={{ width: '100%' }}
        placeholder="请选择数据集"
        onChange={setSelectedDatasets}
        options={datasets.map(dataset => ({
          label: dataset.datasetName,
          value: dataset.datasetId,
        }))}
      />
    </Modal>
  );
};
