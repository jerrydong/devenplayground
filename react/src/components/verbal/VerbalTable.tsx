import * as React from 'react';
import { useState, useEffect, useImperativeHandle } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table';
import { Button } from '../ui/button';
import { Checkbox } from '../ui/checkbox';
import { api } from '../../services/api';
import type { VerbalItem, VerbalQueryRequest } from '../../types/api';
import { DatasetDialog } from './DatasetDialog';
import { OwnerDialog } from './OwnerDialog';
import { ImportDialog } from './ImportDialog';
import { VerbalDialog } from './VerbalDialog';

// This is just a skeleton component that we'll implement in the next step
export interface VerbalTableRef {
  fetchVerbals: (params?: Partial<VerbalQueryRequest>) => Promise<void>;
}

export const VerbalTable = React.forwardRef<VerbalTableRef>((_, ref) => {
  const [selectedRows, setSelectedRows] = useState<number[]>([]);
  const [crossPageSelected, setCrossPageSelected] = useState(false);

  const [verbals, setVerbals] = useState<VerbalItem[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 50;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchVerbals = async (params?: Partial<VerbalQueryRequest>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.queryVerbals({
        page: currentPage,
        pageSize,
        ...params,
      });
      if (response.code === 0) {
        setVerbals(response.data.verbalList);
        setTotal(response.data.total);
      } else {
        setError(response.msg);
      }
    } catch (error) {
      console.error('Failed to fetch verbals:', error);
      setError('获取数据失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  useImperativeHandle(ref, () => ({
    fetchVerbals,
  }));

  useEffect(() => {
    fetchVerbals();
  }, [currentPage]);

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedRows(verbals.map(verbal => verbal.id));
    } else {
      setSelectedRows([]);
    }
  };

  const handleSelectRow = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedRows([...selectedRows, id]);
    } else {
      setSelectedRows(selectedRows.filter(rowId => rowId !== id));
    }
  };

  const handleCrossPageSelect = (checked: boolean) => {
    setCrossPageSelected(checked);
    if (checked) {
      setSelectedRows(verbals.map(verbal => verbal.id));
    } else {
      setSelectedRows([]);
    }
  };

  const [datasetDialogOpen, setDatasetDialogOpen] = useState(false);
  const [ownerDialogOpen, setOwnerDialogOpen] = useState(false);
  const [importDialogOpen, setImportDialogOpen] = useState(false);
  const [verbalDialogOpen, setVerbalDialogOpen] = useState(false);
  const [editingVerbal, setEditingVerbal] = useState<VerbalItem | null>(null);

  const handleDatasetConfirm = async (datasetIds: string[]) => {
    await api.batchModifyDataset({
      datasetList: datasetIds,
      verbalList: selectedRows,
    });
    fetchVerbals();
  };

  const handleOwnerConfirm = async (ownerIds: string[]) => {
    await api.batchModifyOwner({
      ownerList: ownerIds,
      verbalList: selectedRows,
    });
    fetchVerbals();
  };

  const handleImportSuccess = () => {
    fetchVerbals();
  };

  const handleVerbalSuccess = () => {
    fetchVerbals();
    setEditingVerbal(null);
  };

  return (
    <div className="w-full space-y-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Checkbox
            checked={crossPageSelected}
            onCheckedChange={handleCrossPageSelect}
          />
          <span>跨页全选</span>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            disabled={selectedRows.length === 0}
            onClick={() => setDatasetDialogOpen(true)}
          >
            绑定数据集
          </Button>
          <Button
            variant="outline"
            disabled={selectedRows.length === 0}
            onClick={() => setOwnerDialogOpen(true)}
          >
            修改负责人
          </Button>
          <Button
            variant="outline"
            onClick={() => setImportDialogOpen(true)}
          >
            导入学城话术
          </Button>
          <Button
            variant="outline"
            onClick={() => {
              setEditingVerbal(null);
              setVerbalDialogOpen(true);
            }}
          >
            新增话术
          </Button>
        </div>
      </div>

      <DatasetDialog
        open={datasetDialogOpen}
        onOpenChange={setDatasetDialogOpen}
        selectedIds={selectedRows}
        onConfirm={handleDatasetConfirm}
      />

      <OwnerDialog
        open={ownerDialogOpen}
        onOpenChange={setOwnerDialogOpen}
        selectedIds={selectedRows}
        onConfirm={handleOwnerConfirm}
      />

      <ImportDialog
        open={importDialogOpen}
        onOpenChange={setImportDialogOpen}
        onSuccess={handleImportSuccess}
      />

      <VerbalDialog
        open={verbalDialogOpen}
        onOpenChange={setVerbalDialogOpen}
        onSuccess={handleVerbalSuccess}
        type={editingVerbal ? 'edit' : 'add'}
        initialData={editingVerbal || undefined}
      />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50px]">
              <Checkbox
                checked={selectedRows.length === verbals.length && verbals.length > 0}
                onCheckedChange={handleSelectAll}
              />
            </TableHead>
            <TableHead>话术名称</TableHead>
            <TableHead>话术内容</TableHead>
            <TableHead>数据集</TableHead>
            <TableHead>创建人</TableHead>
            <TableHead>负责人</TableHead>
            <TableHead className="w-[100px]">操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {verbals.map((verbal) => (
            <TableRow key={verbal.id}>
              <TableCell>
                <Checkbox
                  checked={selectedRows.includes(verbal.id)}
                  onCheckedChange={(checked) => handleSelectRow(verbal.id, checked as boolean)}
                />
              </TableCell>
              <TableCell>{verbal.name}</TableCell>
              <TableCell>{verbal.contentList.map(c => c.content).join(', ')}</TableCell>
              <TableCell>{verbal.datasetList.map(d => d.datasetName).join(', ')}</TableCell>
              <TableCell>{verbal.creator}</TableCell>
              <TableCell>{verbal.ownerList.join(', ')}</TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  onClick={() => {
                    setEditingVerbal(verbal);
                    setVerbalDialogOpen(true);
                  }}
                >
                  编辑
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {error && (
        <div className="text-red-500 mt-4 text-center">{error}</div>
      )}
      {loading && (
        <div className="text-center mt-4">加载中...</div>
      )}
      <div className="flex justify-between items-center mt-4">
        <div>
          总共 {total} 条记录
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1 || loading}
          >
            上一页
          </Button>
          <span className="py-2">
            第 {currentPage} 页
          </span>
          <Button
            variant="outline"
            onClick={() => setCurrentPage(p => p + 1)}
            disabled={verbals.length < pageSize || loading}
          >
            下一页
          </Button>
        </div>
      </div>
    </div>
  );
});
