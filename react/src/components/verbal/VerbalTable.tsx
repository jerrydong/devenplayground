import { useState } from 'react';
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table';

// This is just a skeleton component that we'll implement in the next step
export const VerbalTable = () => {
  const [selectedRows, setSelectedRows] = useState<number[]>([]);
  const [crossPageSelected, setCrossPageSelected] = useState(false);

  return (
    <div className="w-full">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>选择</TableHead>
            <TableHead>话术名称</TableHead>
            <TableHead>话术内容</TableHead>
            <TableHead>数据集</TableHead>
            <TableHead>创建人</TableHead>
            <TableHead>负责人</TableHead>
            <TableHead>操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {/* Table implementation will go here */}
        </TableBody>
      </Table>
    </div>
  );
};
