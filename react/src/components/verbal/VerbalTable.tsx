import React, { useState } from 'react';
import { Table, Button, Space } from 'antd';
import type { VerbalItem, VerbalQueryRequest } from '../../types/api';
import type { TablePaginationConfig } from 'antd/es/table';

interface VerbalTableProps {
  loading?: boolean;
  data: VerbalItem[];
  total: number;
  currentPage: number;
  onPageChange: (page: number) => void;
  onSearch: (values: VerbalQueryRequest) => Promise<void>;
}

export const VerbalTable: React.FC<VerbalTableProps> = ({
  loading,
  data,
  total,
  currentPage,
  onPageChange,
  onSearch,
}) => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [crossPageSelected, setCrossPageSelected] = useState(false);

  const columns = [
    {
      title: '话术名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '话术内容',
      dataIndex: 'contentList',
      key: 'content',
      render: (contentList: { content: string }[]) => contentList[0]?.content || '-',
    },
    {
      title: '数据集',
      dataIndex: 'datasetList',
      key: 'dataset',
      render: (datasetList: { datasetName: string }[]) => 
        datasetList.map(ds => ds.datasetName).join(', ') || '-',
    },
    {
      title: '创建人',
      dataIndex: 'creator',
      key: 'creator',
    },
    {
      title: '负责人',
      dataIndex: 'ownerList',
      key: 'owner',
      render: (ownerList: string[]) => ownerList.join(', ') || '-',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: VerbalItem) => (
        <Space size="middle">
          <Button type="link" onClick={() => console.log('Edit:', record)}>
            编辑
          </Button>
        </Space>
      ),
    },
  ];

  const rowSelection = {
    selectedRowKeys,
    onChange: (newSelectedRowKeys: React.Key[]) => {
      setSelectedRowKeys(newSelectedRowKeys);
    },
  };

  const pagination: TablePaginationConfig = {
    current: currentPage,
    total,
    pageSize: 50,
    showSizeChanger: false,
    onChange: (page) => {
      onPageChange(page);
      onSearch({ page, pageSize: 50 });
    },
  };

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <Button
          type="primary"
          onClick={() => setCrossPageSelected(!crossPageSelected)}
          className="mr-2"
        >
          {crossPageSelected ? '取消跨页全选' : '跨页全选'}
        </Button>
        <Space>
          <Button
            disabled={selectedRowKeys.length === 0}
            onClick={() => console.log('Bind dataset')}
          >
            绑定数据集
          </Button>
          <Button
            disabled={selectedRowKeys.length === 0}
            onClick={() => console.log('Modify owner')}
          >
            修改负责人
          </Button>
          <Button onClick={() => console.log('Import verbal')}>
            导入学城话术
          </Button>
          <Button onClick={() => console.log('Add verbal')}>
            新增话术
          </Button>
        </Space>
      </div>
      <Table
        rowSelection={rowSelection}
        columns={columns}
        dataSource={data}
        loading={loading}
        rowKey="id"
        pagination={pagination}
      />
    </div>
  );
};
