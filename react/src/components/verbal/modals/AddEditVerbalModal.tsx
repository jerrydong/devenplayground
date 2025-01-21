import React, { useEffect, useState } from 'react';
import { Modal, Form, Input, Select, Button, Space, message } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { debounce } from 'lodash';
import { api } from '../../../services/api';
import type { AddModifyVerbalRequest, DatasetInfo, ContentItem } from '../../../types/api';

interface AddEditVerbalModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  type: 'add' | 'edit';
  initialValues?: AddModifyVerbalRequest;
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
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
  const [owners, setOwners] = useState<{ misId: string; avatarUrl: string }[]>([]);

  useEffect(() => {
    if (open) {
      fetchDatasets();
      if (initialValues) {
        form.setFieldsValue(initialValues);
      }
    }
  }, [open, initialValues, form]);

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
      const response = await api.addModifyVerbal(values, type === 'edit');
      if (response.code === 0) {
        message.success(type === 'edit' ? '修改成功' : '新增成功');
        form.resetFields();
        onSuccess();
        onClose();
      } else {
        message.error(response.msg || (type === 'edit' ? '修改失败' : '新增失败'));
      }
    } catch (error) {
      console.error('Submit error:', error);
      message.error('提交失败，请检查输入');
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
      title={type === 'edit' ? '编辑话术' : '新增话术'}
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
      confirmLoading={loading}
      width={600}
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="name"
          label="话术名称"
          rules={[{ required: true, message: '请输入话术名称' }]}
        >
          <Input 
            placeholder="请输入话术名称" 
            disabled={type === 'edit'}
          />
        </Form.Item>
        
        <Form.List name="contentList">
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                  <Form.Item
                    {...restField}
                    name={[name, 'content']}
                    rules={[{ required: true, message: '请输入话术内容' }]}
                  >
                    <Input placeholder="请输入话术内容" />
                  </Form.Item>
                  {fields.length > 1 && (
                    <MinusCircleOutlined onClick={() => remove(name)} />
                  )}
                </Space>
              ))}
              <Form.Item>
                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                  添加话术内容
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>

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
