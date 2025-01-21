import { 
  ImportVerbalRequest,
  AddModifyVerbalRequest,
  VerbalQueryRequest,
  BatchModifyRequest,
  BaseResponse,
  VerbalQueryResponse,
  SuggestDatasetResponse,
  SuggestOwnerResponse,
  VerbalNameValidResponse
} from '../types/api';

const BASE_URL = '/api';

export const api = {
  // Query verbals with pagination
  queryVerbals: async (params: VerbalQueryRequest): Promise<VerbalQueryResponse> => {
    const queryString = new URLSearchParams({
      ...params,
      page: params.page.toString(),
      pageSize: params.pageSize.toString()
    }).toString();
    const response = await fetch(`${BASE_URL}/verbalQuery?${queryString}`);
    return response.json();
  },

  // Add or modify verbal
  addModifyVerbal: async (data: AddModifyVerbalRequest, isEdit: boolean): Promise<BaseResponse> => {
    const endpoint = isEdit ? '/verbalModify' : '/verbalAdd';
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  // Import verbal from learning city
  importVerbal: async (data: ImportVerbalRequest): Promise<BaseResponse> => {
    const response = await fetch(`${BASE_URL}/importXcVerbal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  // Check if verbal name is valid
  checkVerbalName: async (verbalName: string): Promise<VerbalNameValidResponse> => {
    const response = await fetch(`${BASE_URL}/verbalIsNameValid?verbalName=${encodeURIComponent(verbalName)}`);
    return response.json();
  },

  // Get suggested datasets
  getSuggestDatasets: async (): Promise<SuggestDatasetResponse> => {
    const response = await fetch(`${BASE_URL}/verbalGetSuggestDataset`);
    return response.json();
  },

  // Get suggested owners
  getSuggestOwners: async (query: string): Promise<SuggestOwnerResponse> => {
    const response = await fetch(`${BASE_URL}/verbalGetSuggest?q=${encodeURIComponent(query)}`);
    return response.json();
  },

  // Batch modify owners
  batchModifyOwner: async (data: BatchModifyRequest): Promise<BaseResponse> => {
    const response = await fetch(`${BASE_URL}/verbalBatchModifyOwner`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  // Batch modify datasets
  batchModifyDataset: async (data: BatchModifyRequest): Promise<BaseResponse> => {
    const response = await fetch(`${BASE_URL}/verbalBatchModifyDataset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
};
