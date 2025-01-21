import React from 'react';
import { Form, Input, Button, Select } from 'antd';
import type { FormInstance } from 'antd/es/form';

interface SearchFormProps {
  onSearch: (values: any) => void;
  onReset: () => void;
  onCitySearch?: (value: string) => void;
  onLoadMore?: () => void;
  cityOptions: Array<{ id: number; name: string; }>;
  form: FormInstance;
  loading?: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({
  onSearch,
  onReset,
  onCitySearch,
  onLoadMore,
  cityOptions,
  form,
  loading
}) => {
  const handleReset = () => {
    form.resetFields();
    onReset();
  };

  return (
    <Form
      form={form}
      layout="inline"
      onFinish={onSearch}
      className="mb-4 p-4 bg-white rounded-lg shadow"
    >
      <Form.Item name="name" label="Name">
        <Input placeholder="Search by name" allowClear />
      </Form.Item>
      <Form.Item name="age" label="Age">
        <Input placeholder="Search by age" type="number" allowClear />
      </Form.Item>
      <Form.Item name="address" label="Address">
        <Input placeholder="Search by address" allowClear />
      </Form.Item>
      <Form.Item name="city" label="City">
        <Select
          placeholder="Select city"
          style={{ width: 200 }}
          showSearch
          allowClear
          loading={loading}
          filterOption={false}
          onSearch={onCitySearch}
          options={cityOptions.map(city => ({
            value: city.name,
            label: city.name,
          }))}
          notFoundContent={loading ? 'Loading...' : null}
          onPopupScroll={(e) => {
            const target = e.target as HTMLDivElement;
            if (
              !loading &&
              target.scrollTop + target.offsetHeight === target.scrollHeight
            ) {
              onLoadMore?.();
            }
          }}
        />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Search
        </Button>
      </Form.Item>
      <Form.Item>
        <Button onClick={handleReset}>Reset</Button>
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
