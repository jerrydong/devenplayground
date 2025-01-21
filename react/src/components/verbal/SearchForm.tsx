import React from 'react';
import { Form, Input, Button } from 'antd';
import type { VerbalQueryRequest } from '../../types/api';

export const SearchForm = () => {
  const [form] = Form.useForm<VerbalQueryRequest>();

  const onFinish = (values: VerbalQueryRequest) => {
    // Will implement in the next step
    console.log('Search form values:', values);
  };

  return (
    <Form form={form} onFinish={onFinish} layout="inline">
      <Form.Item name="verbalName" label="话术名称">
        <Input placeholder="请输入" />
      </Form.Item>
      <Form.Item name="verbalContent" label="话术内容">
        <Input placeholder="请输入" />
      </Form.Item>
      <Form.Item name="datasetName" label="数据集">
        <Input placeholder="请输入" />
      </Form.Item>
      <Form.Item name="creator" label="创建人">
        <Input placeholder="请输入" />
      </Form.Item>
      <Form.Item name="owner" label="负责人">
        <Input placeholder="请输入" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          搜索
        </Button>
      </Form.Item>
    </Form>
  );
};
