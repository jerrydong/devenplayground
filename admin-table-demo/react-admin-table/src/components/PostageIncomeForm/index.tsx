'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form } from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { ConfigurationModule } from './ConfigurationModule';
import { DisplayLogicModule } from './DisplayLogicModule';
import { EffectiveDimensionsModule } from './EffectiveDimensionsModule';
import { PostageIncomeFormData, formSchema } from './types';

interface PostageIncomeFormProps {
  onSubmit: (data: PostageIncomeFormData) => void;
  initialData?: PostageIncomeFormData;
}

export function PostageIncomeForm({ onSubmit, initialData }: PostageIncomeFormProps) {
  const form = useForm<PostageIncomeFormData>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData,
  });

  const handleSubmit = form.handleSubmit((data) => {
    onSubmit(data);
  });

  return (
    <Form {...form}>
      <form onSubmit={handleSubmit} className="space-y-6">
        <ConfigurationModule />
        <DisplayLogicModule />
        <EffectiveDimensionsModule />
        <div className="flex justify-end space-x-4">
          <Button type="submit">提交</Button>
        </div>
      </form>
    </Form>
  );
}
