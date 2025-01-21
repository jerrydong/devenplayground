import { z } from 'zod';

// Validation schemas
export const configurationSchema = z.object({
  strategyName: z.string().min(1, '请输入策略名称'),
  fulfillmentNodes: z.array(z.string()).min(1, '请至少选择一个履约节点'),
  managementLine: z.string().min(1, '请选择运力管理线'),
  pricingPlan: z.string().optional(),
});

export const displayLogicSchema = z.object({
  normalPackage: z.object({
    totalIncome: z.boolean(),
    subIncome: z.boolean(),
  }),
  buttonPackage: z.object({
    totalIncome: z.boolean(),
    subIncome: z.boolean(),
  }),
  combinedOrder: z.object({
    totalIncome: z.boolean(),
    subIncome: z.boolean(),
  }),
});

export const effectiveDimensionsSchema = z.object({
  appVersion: z.object({
    isGrayscale: z.boolean(),
    cities: z.array(z.object({
      type: z.string(),
      city: z.string(),
    })).optional(),
  }),
  cityRange: z.object({
    isGrayscale: z.boolean(),
    systems: z.array(z.string()),
    comparison: z.string(),
    versions: z.array(z.string()),
  }),
  riderNumber: z.object({
    isGrayscale: z.boolean(),
    restrictionType: z.string(),
    numbers: z.array(z.number()),
  }),
  displayRole: z.string(),
});

export const formSchema = z.object({
  configuration: configurationSchema,
  displayLogic: displayLogicSchema,
  effectiveDimensions: effectiveDimensionsSchema,
});

// Types derived from schemas
export type ConfigurationData = z.infer<typeof configurationSchema>;
export type DisplayLogicData = z.infer<typeof displayLogicSchema>;
export type EffectiveDimensionsData = z.infer<typeof effectiveDimensionsSchema>;
export type PostageIncomeFormData = z.infer<typeof formSchema>;

// Constants
export const FULFILLMENT_NODES = [
  { label: '接单前', value: 'before_accept' },
  { label: '待到店', value: 'waiting_arrival' },
  { label: '待取货', value: 'waiting_pickup' },
  { label: '待送达', value: 'waiting_delivery' },
] as const;

export const MANAGEMENT_LINES = [
  { label: '自营', value: 'self_operated' },
  { label: '加盟', value: 'franchise' },
  { label: '众包', value: 'crowdsourcing' },
  { label: '乐跑', value: 'happy_running' },
  { label: '乐跑远计划', value: 'happy_running_far' },
  { label: '驻跑', value: 'stationed_running' },
  { label: '畅跑', value: 'free_running' },
  { label: '周计划', value: 'weekly_plan' },
  { label: '企客加盟', value: 'enterprise_franchise' },
  { label: '企客驻跑', value: 'enterprise_stationed' },
  { label: '跑腿同城核心', value: 'local_core' },
  { label: '跑腿同城荣耀', value: 'local_glory' },
  { label: '城代', value: 'city_agent' },
  { label: '校园', value: 'campus' },
] as const;

export const PRICING_PLANS = [
  { label: '2.0人工定价', value: 'manual_2_0' },
  { label: '3.0算法定价', value: 'algorithm_3_0' },
] as const;

export const SYSTEM_TYPES = [
  { label: 'Android', value: 'android' },
  { label: 'iOS', value: 'ios' },
] as const;

export const COMPARISON_TYPES = [
  { label: '大于等于', value: 'gte' },
  { label: '等于', value: 'eq' },
  { label: '小于等于', value: 'lte' },
  { label: '大于', value: 'gt' },
  { label: '小于', value: 'lt' },
] as const;

export const RESTRICTION_TYPES = [
  { label: '手机尾号', value: 'phone' },
  { label: '骑手ID', value: 'rider_id' },
  { label: '美团ID', value: 'meituan_id' },
] as const;

export const DISPLAY_ROLES = [
  { label: '全部', value: 'all' },
  { label: '骑手', value: 'rider' },
  { label: '站长', value: 'station_master' },
] as const;
