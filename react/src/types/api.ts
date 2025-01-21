// API Response Types
interface BaseResponse {
  code: number;
  msg: string;
}

interface DatasetInfo {
  datasetId: string;
  datasetName: string;
}

interface ContentItem {
  id: number;
  content: string;
}

interface VerbalItem {
  id: number;
  name: string;
  contentList: ContentItem[];
  datasetList: DatasetInfo[];
  creator: string;
  ownerList: string[];
}

interface VerbalQueryResponse extends BaseResponse {
  data: {
    verbalList: VerbalItem[];
    total: number;
  };
}

interface SuggestDatasetResponse extends BaseResponse {
  data: DatasetInfo[];
}

interface SuggestOwnerResponse extends BaseResponse {
  data: {
    misId: string;
    avatarUrl: string;
  }[];
}

interface VerbalNameValidResponse extends BaseResponse {
  data: boolean;
}

// API Request Types
interface ImportVerbalRequest {
  link: string;
  ownerList: string[];
  datasetList: string[];
}

interface AddModifyVerbalRequest {
  id?: number;
  name: string;
  contentList: ContentItem[];
  ownerList: string[];
  datasetList: string[];
}

interface VerbalQueryRequest {
  verbalName?: string;
  verbalContent?: string;
  datasetName?: string;
  creator?: string;
  owner?: string;
  page: number;
  pageSize: number;
}

interface BatchModifyRequest {
  ownerList?: string[];
  datasetList?: string[];
  verbalList?: number[];
  filterVerbalName?: string;
  filterVerbalContent?: string;
  filterCreator?: string;
  filterOwner?: string;
}

export type {
  BaseResponse,
  DatasetInfo,
  ContentItem,
  VerbalItem,
  VerbalQueryResponse,
  SuggestDatasetResponse,
  SuggestOwnerResponse,
  VerbalNameValidResponse,
  ImportVerbalRequest,
  AddModifyVerbalRequest,
  VerbalQueryRequest,
  BatchModifyRequest
};
