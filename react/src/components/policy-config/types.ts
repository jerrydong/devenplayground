export type ContentType = 'desensitized' | 'structured' | 'waybillSenderAddress' | 'waybillSenderName' | 'none';

export type DisplayMode = 'all' | 'gray';

export type VersionLogic = 'gt' | 'lt' | 'eq' | 'gte' | 'lte';

export type PlatformType = 'android' | 'ios';

export type SuffixType = 'phone' | 'riderId' | 'meiTuanId';

export interface CitySelection {
  type: string;
  city: string;
}

export interface VersionConfig {
  platform: PlatformType;
  logic: VersionLogic;
  versions: string[];
}

export interface PolicyConfigFormData {
  // Before Order
  beforeOrderMainTitle: ContentType;
  beforeOrderSubTitle: ContentType;
  
  // Waiting for Pickup
  waitingPickupMainTitle: ContentType;
  waitingPickupSubTitle: ContentType;
  
  // Waiting for Delivery
  waitingDeliveryMainTitle: ContentType;
  waitingDeliverySubTitle: ContentType;
  
  // Effective Range
  displayMode: DisplayMode;
  citySelections: CitySelection[];
  selectedCities: string[];
  
  // System Version
  versionMode: DisplayMode;
  versionConfigs: VersionConfig[];
  
  // Suffix Restriction
  suffixMode: DisplayMode;
  suffixType: SuffixType;
  selectedDigits: number[];
}
