import React from 'react';
import { Layout } from 'antd';
import { SearchForm } from '../../components/verbal/SearchForm';
import { VerbalTable } from '../../components/verbal/VerbalTable';

const { Content } = Layout;

const VerbalPage = () => {
  return (
    <Layout className="min-h-screen">
      <Content className="p-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <SearchForm />
          <div className="mt-6">
            <VerbalTable />
          </div>
        </div>
      </Content>
    </Layout>
  );
};

export default VerbalPage;
