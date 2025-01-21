import React, { useState, useEffect } from 'react';
import { debounce } from '../utils/debounce';
import { Table, Button, Popconfirm, message, Form } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { ColumnType } from 'antd/es/table';
import type { Key } from 'antd/es/table/interface';
import SearchForm from './SearchForm';

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
  city?: string;
}

// Mock data
const initialData: DataType[] = [
  { key: '1', name: 'John Brown', age: 32, address: 'New York No. 1 Lake Park', city: 'New York' },
  { key: '2', name: 'Jim Green', age: 42, address: 'London No. 1 Lake Park', city: 'London' },
  { key: '3', name: 'Joe Black', age: 32, address: 'Sydney No. 1 Lake Park', city: 'Sydney' },
  { key: '4', name: 'Jim Red', age: 32, address: 'London No. 2 Lake Park', city: 'London' },
];

type DataIndex = keyof DataType;

const DataTable: React.FC = () => {
  const [data, setData] = useState<DataType[]>(initialData);
  const [cityOptions, setCityOptions] = useState<Array<{ id: number; name: string }>>([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState<{
    name?: string;
    age?: number;
    address?: string;
    city?: string;
  }>({});
  const [form] = Form.useForm();

  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [hasMore, setHasMore] = useState(true);
  const pageSize = 10;

  const fetchCities = async (page: number, search: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/cities?page=${page}&pageSize=${pageSize}&search=${search}`);
      const result = await response.json();
      if (page === 1) {
        setCityOptions(result.data);
      } else {
        setCityOptions(prev => [...prev, ...result.data]);
      }
      setCurrentPage(page);
      setHasMore(result.data.length === pageSize);
    } catch (error) {
      message.error('Failed to fetch city options');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCities(1, '');
  }, []);

  // Update form values when searchParams changes
  useEffect(() => {
    form.setFieldsValue(searchParams);
  }, [searchParams, form]);

  const handleCitySearch = debounce((value: string) => {
    setSearchTerm(value);
    setCityOptions([]);
    setCurrentPage(1);
    setHasMore(true);
    fetchCities(1, value);
  }, 300);

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      fetchCities(currentPage + 1, searchTerm);
    }
  };

  const handleDelete = (key: string) => {
    const newData = data.filter(item => item.key !== key);
    setData(newData);
    message.success('Record deleted successfully');
  };

  const getColumnSearchProps = (dataIndex: DataIndex): ColumnType<DataType> => ({
    onFilter: (value: boolean | Key, record: DataType) =>
      record[dataIndex]?.toString().toLowerCase().includes(String(value).toLowerCase()) ?? false,
  });

  const columns: ColumnsType<DataType> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      ...getColumnSearchProps('name'),
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      ...getColumnSearchProps('age'),
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
      ...getColumnSearchProps('address'),
    },
    {
      title: 'City',
      dataIndex: 'city',
      key: 'city',
      ...getColumnSearchProps('city'),
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Popconfirm
          title="Are you sure you want to delete this record?"
          onConfirm={() => handleDelete(record.key)}
          okText="Yes"
          cancelText="No"
        >
          <Button 
            type="link" 
            danger 
            icon={<DeleteOutlined />}
          >
            Delete
          </Button>
        </Popconfirm>
      ),
    },
  ];

  const handleFormSearch = (values: any) => {
    setSearchParams(values);
    setLoading(true);
    
    try {
      const filteredData = initialData.filter(item => {
        const nameMatch = !values.name || item.name.toLowerCase().includes(values.name.toLowerCase());
        const ageMatch = !values.age || item.age === Number(values.age);
        const addressMatch = !values.address || item.address.toLowerCase().includes(values.address.toLowerCase());
        const cityMatch = !values.city || item.city === values.city;
        
        return nameMatch && ageMatch && addressMatch && cityMatch;
      });
      
      if (filteredData.length === 0) {
        message.info('No records found matching the search criteria');
      }
      
      setData(filteredData);
    } catch (error) {
      message.error('An error occurred while searching');
    } finally {
      setLoading(false);
    }
  };

  const handleFormReset = () => {
    setSearchParams({});
    setData(initialData);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-4">Data Table</h1>
      <SearchForm
        onSearch={handleFormSearch}
        onReset={handleFormReset}
        onCitySearch={handleCitySearch}
        onLoadMore={handleLoadMore}
        cityOptions={cityOptions}
        form={form}
        loading={loading}
      />
      <Table 
        columns={columns} 
        dataSource={data}
        loading={loading}
        pagination={{
          defaultPageSize: 5,
          showSizeChanger: true,
          showQuickJumper: true,
          total: data.length,
          showTotal: (total) => `Total ${total} items`,
        }}
      />
    </div>
  );
};

export default DataTable;
