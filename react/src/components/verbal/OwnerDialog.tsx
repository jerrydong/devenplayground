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
import { Input } from '../ui/input';
import { useState, useEffect } from 'react';
import { api } from '../../services/api';

interface OwnerDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedIds: number[];
  onConfirm: (ownerIds: string[]) => void;
  crossPageSelected?: boolean;
  filters?: {
    verbalName?: string;
    verbalContent?: string;
    creator?: string;
    owner?: string;
  };
}

interface SuggestOwner {
  misId: string;
  avatarUrl: string;
}

export const OwnerDialog = ({
  open,
  onOpenChange,
  selectedIds,
  onConfirm,
  crossPageSelected,
  filters,
}: OwnerDialogProps) => {
  const [owners, setOwners] = useState<SuggestOwner[]>([]);
  const [selectedOwners, setSelectedOwners] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchOwners = async () => {
      if (!searchQuery) return;
      setLoading(true);
      try {
        const response = await api.getSuggestOwners(searchQuery);
        if (response.code === 0 && response.data) {
          setOwners(response.data);
        }
      } catch (error) {
        console.error('Failed to fetch owners:', error);
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(fetchOwners, 300);
    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  const handleConfirm = async () => {
    if (selectedOwners.length === 0) return;

    try {
      const response = await api.batchModifyOwner(
        crossPageSelected
          ? {
              ownerList: selectedOwners,
              filterVerbalName: filters?.verbalName,
              filterVerbalContent: filters?.verbalContent,
              filterCreator: filters?.creator,
              filterOwner: filters?.owner,
            }
          : {
              ownerList: selectedOwners,
              verbalList: selectedIds,
            }
      );

      if (response.code === 0) {
        onConfirm(selectedOwners);
        onOpenChange(false);
      }
    } catch (error) {
      console.error('Failed to modify owners:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>修改负责人</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <Input
            placeholder="搜索负责人"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Select
            value={selectedOwners[0]}
            onValueChange={(value) => setSelectedOwners([value])}
          >
            <SelectTrigger>
              <SelectValue placeholder="请选择负责人" />
            </SelectTrigger>
            <SelectContent>
              {owners.map((owner) => (
                <SelectItem key={owner.misId} value={owner.misId}>
                  {owner.misId}
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
            disabled={selectedOwners.length === 0 || loading}
          >
            确认
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
