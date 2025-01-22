import React from 'react';
import { Form, Input, Button } from 'antd';
import type { VerbalQueryRequest } from '../../types/api';

interface SearchFormProps {
  onSearch: (values: VerbalQueryRequest) => Promise<void>;
  loading?: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, loading }) => {
  const [form] = Form.useForm<VerbalQueryRequest>();

  const handleReset = () => {
    form.resetFields();
    onSearch({ page: 1, pageSize: 50 });
  };

  return (
    <Form 
      form={form} 
      onFinish={onSearch} 
      layout="inline"
      className="gap-4 flex-wrap"
    >
      <Form.Item name="verbalName" label="话术名称">
        <Input placeholder="请输入" allowClear />
      </Form.Item>
      <Form.Item name="verbalContent" label="话术内容">
        <Input placeholder="请输入" allowClear />
      </Form.Item>
      <Form.Item name="datasetName" label="数据集">
        <Input placeholder="请输入" allowClear />
      </Form.Item>
      <Form.Item name="creator" label="创建人">
        <Input placeholder="请输入" allowClear />
      </Form.Item>
      <Form.Item name="owner" label="负责人">
        <Input placeholder="请输入" allowClear />
      </Form.Item>
      <Form.Item className="flex-none">
        <Button type="primary" htmlType="submit" loading={loading}>
          搜索
        </Button>
        <Button className="ml-2" onClick={handleReset}>
          重置
        </Button>
      </Form.Item>
    </Form>
  );
};
