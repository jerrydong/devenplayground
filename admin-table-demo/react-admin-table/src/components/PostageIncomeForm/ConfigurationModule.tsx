'use client';

import { useFormContext } from 'react-hook-form';
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Tooltip, TooltipContent } from '@/components/ui/tooltip';
import { InfoIcon } from 'lucide-react';
import {
  FULFILLMENT_NODES,
  MANAGEMENT_LINES,
  PRICING_PLANS,
  PostageIncomeFormData,
} from './types';

export function ConfigurationModule() {
  const { control, watch } = useFormContext<PostageIncomeFormData>();
  const managementLine = watch('configuration.managementLine');
  const showPricingPlan = ['happy_running', 'happy_running_far', 'local_core'].includes(managementLine || '');

  return (
    <Card>
      <CardHeader>
        <CardTitle>配置信息</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Strategy Name */}
        <FormField
          control={control}
          name="configuration.strategyName"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="flex items-center space-x-2">
                <span>邮资收入展示策略名称</span>
                <Tooltip>
                  <InfoIcon className="h-4 w-4 text-zinc-500" />
                  <TooltipContent>此名称仅在后台做配置管理使用、不会在骑手端展示</TooltipContent>
                </Tooltip>
              </FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Fulfillment Nodes */}
        <FormField
          control={control}
          name="configuration.fulfillmentNodes"
          render={() => (
            <FormItem>
              <FormLabel>展示的履约节点选项</FormLabel>
              <div className="grid grid-cols-2 gap-4">
                {FULFILLMENT_NODES.map((node) => (
                  <FormField
                    key={node.value}
                    control={control}
                    name="configuration.fulfillmentNodes"
                    render={({ field }) => (
                      <FormItem className="flex items-center space-x-2">
                        <FormControl>
                          <Checkbox
                            checked={field.value?.includes(node.value)}
                            onCheckedChange={(checked) => {
                              const value = field.value || [];
                              if (checked) {
                                field.onChange([...value, node.value]);
                              } else {
                                field.onChange(value.filter((v) => v !== node.value));
                              }
                            }}
                          />
                        </FormControl>
                        <FormLabel className="font-normal">{node.label}</FormLabel>
                      </FormItem>
                    )}
                  />
                ))}
              </div>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Management Line */}
        <FormField
          control={control}
          name="configuration.managementLine"
          render={({ field }) => (
            <FormItem>
              <FormLabel>展示的运力管理线选项</FormLabel>
              <FormControl>
                <RadioGroup
                  onValueChange={field.onChange}
                  value={field.value}
                  className="grid grid-cols-2 gap-4"
                >
                  {MANAGEMENT_LINES.map((line) => (
                    <FormItem key={line.value} className="flex items-center space-x-2">
                      <FormControl>
                        <RadioGroupItem value={line.value} />
                      </FormControl>
                      <FormLabel className="font-normal">{line.label}</FormLabel>
                    </FormItem>
                  ))}
                </RadioGroup>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Pricing Plan - Conditional */}
        {showPricingPlan && (
          <FormField
            control={control}
            name="configuration.pricingPlan"
            render={({ field }) => (
              <FormItem>
                <FormLabel>定价方案</FormLabel>
                <FormControl>
                  <RadioGroup
                    onValueChange={field.onChange}
                    value={field.value}
                    className="grid grid-cols-2 gap-4"
                  >
                    {PRICING_PLANS.map((plan) => (
                      <FormItem key={plan.value} className="flex items-center space-x-2">
                        <FormControl>
                          <RadioGroupItem value={plan.value} />
                        </FormControl>
                        <FormLabel className="font-normal">{plan.label}</FormLabel>
                      </FormItem>
                    ))}
                  </RadioGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}
      </CardContent>
    </Card>
  );
}
