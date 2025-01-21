import * as React from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import { Button } from '../ui/button';
import { useState, useEffect } from 'react';
import { api } from '../../services/api';
import type { DatasetInfo } from '../../types/api';

interface DatasetDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedIds: number[];
  onConfirm: (datasetIds: string[]) => void;
  crossPageSelected?: boolean;
  filters?: {
    verbalName?: string;
    verbalContent?: string;
    creator?: string;
    owner?: string;
  };
}

export const DatasetDialog = ({
  open,
  onOpenChange,
  selectedIds,
  onConfirm,
  crossPageSelected,
  filters,
}: DatasetDialogProps) => {
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
  const [selectedDatasets, setSelectedDatasets] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchDatasets = async () => {
      setLoading(true);
      try {
        const response = await api.getSuggestDatasets();
        if (response.code === 0 && response.data) {
          setDatasets(response.data);
        }
      } catch (error) {
        console.error('Failed to fetch datasets:', error);
      } finally {
        setLoading(false);
      }
    };

    if (open) {
      fetchDatasets();
    }
  }, [open]);

  const handleConfirm = async () => {
    if (selectedDatasets.length === 0) return;

    try {
      const response = await api.batchModifyDataset(
        crossPageSelected
          ? {
              datasetList: selectedDatasets,
              filterVerbalName: filters?.verbalName,
              filterVerbalContent: filters?.verbalContent,
              filterCreator: filters?.creator,
              filterOwner: filters?.owner,
            }
          : {
              datasetList: selectedDatasets,
              verbalList: selectedIds,
            }
      );

      if (response.code === 0) {
        onConfirm(selectedDatasets);
        onOpenChange(false);
      }
    } catch (error) {
      console.error('Failed to modify datasets:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>绑定数据集</DialogTitle>
        </DialogHeader>
        <div className="py-4">
          <Select
            value={selectedDatasets[0]}
            onValueChange={(value) => setSelectedDatasets([value])}
          >
            <SelectTrigger>
              <SelectValue placeholder="请选择数据集" />
            </SelectTrigger>
            <SelectContent>
              {datasets.map((dataset) => (
                <SelectItem key={dataset.datasetId} value={dataset.datasetId}>
                  {dataset.datasetName}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
          >
            取消
          </Button>
          <Button
            onClick={handleConfirm}
            disabled={selectedDatasets.length === 0 || loading}
          >
            确认
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
