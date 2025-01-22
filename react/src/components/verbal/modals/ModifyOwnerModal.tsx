import React, { useState } from 'react';
import { Modal, Select, message } from 'antd';
import type { BatchModifyRequest } from '../../../types/api';
import { api } from '../../../services/api';

interface ModifyOwnerModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (payload: BatchModifyRequest) => Promise<void>;
  basePayload: BatchModifyRequest;
}

export const ModifyOwnerModal: React.FC<ModifyOwnerModalProps> = ({
  open,
  onClose,
  onConfirm,
  basePayload,
}) => {
  const [loading, setLoading] = useState(false);
  const [owners, setOwners] = useState<{ misId: string; avatarUrl: string }[]>([]);
  const [selectedOwners, setSelectedOwners] = useState<string[]>([]);
  const [_searchValue, setSearchValue] = useState('');

  const fetchOwners = async (query: string) => {
    try {
      const response = await api.getSuggestOwners(query);
      if (response.code === 0) {
        setOwners(response.data);
      }
    } catch (error) {
      console.error('Fetch owners error:', error);
      message.error('获取负责人列表失败');
    }
  };

  const handleSearch = (value: string) => {
    setSearchValue(value);
    if (value) {
      fetchOwners(value);
    } else {
      setOwners([]);
    }
  };

  const handleConfirm = async () => {
    if (selectedOwners.length === 0) {
      message.warning('请选择负责人');
      return;
    }

    try {
      setLoading(true);
      await onConfirm({
        ...basePayload,
        ownerList: selectedOwners,
      });
      onClose();
    } catch (error) {
      console.error('Modify owner error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="修改负责人"
      open={open}
      onCancel={onClose}
      onOk={handleConfirm}
      confirmLoading={loading}
    >
      <Select
        mode="multiple"
        style={{ width: '100%' }}
        placeholder="请输入关键字搜索负责人"
        value={selectedOwners}
        onChange={setSelectedOwners}
        onSearch={handleSearch}
        options={owners.map(owner => ({
          label: owner.misId,
          value: owner.misId,
        }))}
        showSearch
        filterOption={false}
      />
    </Modal>
  );
};
