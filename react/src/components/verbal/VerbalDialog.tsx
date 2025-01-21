import * as React from 'react';
import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from '../ui/form';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { api } from '../../services/api';
import type { AddModifyVerbalRequest, VerbalItem } from '../../types/api';

interface VerbalDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
  type: 'add' | 'edit';
  initialData?: VerbalItem;
}

const verbalSchema = z.object({
  name: z.string().min(1, '请输入话术名称'),
  content: z.string().min(1, '请输入话术内容'),
  ownerList: z.array(z.string()).min(1, '请选择负责人'),
  datasetList: z.array(z.string()).min(1, '请选择数据集'),
});

type VerbalFormValues = z.infer<typeof verbalSchema>;

export const VerbalDialog = ({
  open,
  onOpenChange,
  onSuccess,
  type,
  initialData,
}: VerbalDialogProps) => {
  const [loading, setLoading] = useState(false);

  const form = useForm<VerbalFormValues>({
    resolver: zodResolver(verbalSchema),
    defaultValues: {
      name: initialData?.name || '',
      content: initialData?.contentList[0]?.content || '',
      ownerList: initialData?.ownerList || [],
      datasetList: initialData?.datasetList.map((d: { datasetId: string }) => d.datasetId) || [],
    },
  });

  const onSubmit = async (values: VerbalFormValues) => {
    setLoading(true);
    try {
      const data: AddModifyVerbalRequest = {
        name: values.name,
        contentList: [{ id: 0, content: values.content }],
        ownerList: values.ownerList,
        datasetList: values.datasetList,
      };

      if (type === 'edit' && initialData) {
        data.id = initialData.id;
      }

      const response = await api.addModifyVerbal(data, type === 'edit');

      if (response.code === 0) {
        onSuccess();
        onOpenChange(false);
        form.reset();
      }
    } catch (error) {
      console.error('Failed to save verbal:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{type === 'add' ? '新增话术' : '编辑话术'}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>话术名称</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="请输入话术名称"
                      {...field}
                      disabled={type === 'edit'}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="content"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>话术内容</FormLabel>
                  <FormControl>
                    <Input placeholder="请输入话术内容" {...field} />
                  </FormControl>
                </FormItem>
              )}
            />
            {/* Owner and dataset selection will be added here */}
          </form>
        </Form>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
          >
            取消
          </Button>
          <Button
            onClick={form.handleSubmit(onSubmit)}
            disabled={loading}
          >
            确认
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
