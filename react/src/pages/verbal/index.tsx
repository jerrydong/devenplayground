import React, { useState } from 'react';
import { Layout, message } from 'antd';
import { SearchForm } from '../../components/verbal/SearchForm';
import { VerbalTable } from '../../components/verbal/VerbalTable';
import { api } from '../../services/api';
import type { VerbalItem, VerbalQueryRequest, BatchModifyRequest } from '../../types/api';

const { Content } = Layout;

const VerbalPage = () => {
  const [loading, setLoading] = useState(false);
  const [verbals, setVerbals] = useState<VerbalItem[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchValues, setSearchValues] = useState<Partial<VerbalQueryRequest>>({});
  const pageSize = 50;

  const handleSearch = async (values: Partial<VerbalQueryRequest>) => {
    try {
      setLoading(true);
      setSearchValues(values);
      const response = await api.queryVerbals({
        ...values,
        page: currentPage,
        pageSize,
      } as VerbalQueryRequest);
      if (response.code === 0) {
        setVerbals(response.data.verbalList);
        setTotal(response.data.total);
      } else {
        message.error(response.msg || '查询失败');
      }
    } catch (error) {
      message.error('查询失败，请稍后重试');
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout className="min-h-screen">
      <Content className="p-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <SearchForm onSearch={handleSearch} loading={loading} />
          <div className="mt-6">
            <VerbalTable 
              loading={loading}
              data={verbals}
              total={total}
              currentPage={currentPage}
              onPageChange={setCurrentPage}
              onSearch={handleSearch}
              searchValues={searchValues}
              onBatchModifyDataset={async (payload) => {
                try {
                  await api.batchModifyDataset(payload);
                  message.success('批量修改数据集成功');
                  handleSearch(searchValues);
                } catch (error) {
                  message.error('批量修改数据集失败');
                }
              }}
              onBatchModifyOwner={async (payload) => {
                try {
                  await api.batchModifyOwner(payload);
                  message.success('批量修改负责人成功');
                  handleSearch(searchValues);
                } catch (error) {
                  message.error('批量修改负责人失败');
                }
              }}
            />
          </div>
        </div>
      </Content>
    </Layout>
  );
};

export default VerbalPage;
