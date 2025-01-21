import * as React from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { useState } from 'react';
import { api } from '../../services/api';

interface ImportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
}

export const ImportDialog = ({
  open,
  onOpenChange,
  onSuccess,
}: ImportDialogProps) => {
  const [link, setLink] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImport = async () => {
    if (!link) return;

    setLoading(true);
    try {
      const response = await api.importVerbal({
        link,
        ownerList: [],
        datasetList: [],
      });

      if (response.code === 0) {
        onSuccess();
        onOpenChange(false);
        setLink('');
      }
    } catch (error) {
      console.error('Failed to import verbal:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>导入学城话术</DialogTitle>
        </DialogHeader>
        <div className="py-4">
          <Input
            placeholder="请输入链接"
            value={link}
            onChange={(e) => setLink(e.target.value)}
          />
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
          >
            取消
          </Button>
          <Button
            onClick={handleImport}
            disabled={!link || loading}
          >
            导入
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
