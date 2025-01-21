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
export const SearchForm = () => {
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

  return (
    <Form {...form}>
      <form className="flex gap-4 items-end">
        <FormField
          control={form.control}
          name="verbalName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>话术名称</FormLabel>
              <FormControl>
                <Input placeholder="请输入" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        {/* Other form fields will be implemented in the next step */}
        <Button type="submit" className="bg-blue-500">搜索</Button>
      </form>
    </Form>
  );
};
