import { Input } from '../ui/input';
import { Button } from '../ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from '../ui/form';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const searchFormSchema = z.object({
  verbalName: z.string().optional(),
  verbalContent: z.string().optional(),
  datasetName: z.string().optional(),
  creator: z.string().optional(),
  owner: z.string().optional(),
});

type SearchFormValues = z.infer<typeof searchFormSchema>;

// This is just a skeleton component that we'll implement in the next step
interface SearchFormProps {
  onSearch: (values: SearchFormValues) => void;
}

export const SearchForm = ({ onSearch }: SearchFormProps) => {
  const form = useForm<SearchFormValues>({
    resolver: zodResolver(searchFormSchema),
    defaultValues: {
      verbalName: '',
      verbalContent: '',
      datasetName: '',
      creator: '',
      owner: '',
    },
  });

  const onSubmit = (values: SearchFormValues) => {
    onSearch(values);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="grid grid-cols-3 gap-4">
        <FormField
          control={form.control}
          name="verbalName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>话术名称</FormLabel>
              <FormControl>
                <Input placeholder="请输入话术名称" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="verbalContent"
          render={({ field }) => (
            <FormItem>
              <FormLabel>话术内容</FormLabel>
              <FormControl>
                <Input placeholder="请输入话术内容" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="datasetName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>数据集</FormLabel>
              <FormControl>
                <Input placeholder="请输入数据集" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="creator"
          render={({ field }) => (
            <FormItem>
              <FormLabel>创建人</FormLabel>
              <FormControl>
                <Input placeholder="请输入创建人" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="owner"
          render={({ field }) => (
            <FormItem>
              <FormLabel>负责人</FormLabel>
              <FormControl>
                <Input placeholder="请输入负责人" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <div className="flex items-end">
          <Button type="submit">搜索</Button>
        </div>
      </form>
    </Form>
  );
};
