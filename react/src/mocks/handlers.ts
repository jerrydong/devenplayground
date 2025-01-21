import { http, HttpResponse } from 'msw';
import type { 
  VerbalItem, 
  VerbalQueryResponse, 
  SuggestDatasetResponse,
  SuggestOwnerResponse,
  BaseResponse 
} from '../types/api';

// Mock data
const mockVerbals: VerbalItem[] = Array.from({ length: 100 }, (_, index) => ({
  id: index + 1,
  name: `话术${index + 1}`,
  contentList: [{ id: index + 1, content: `示例内容 ${index + 1}` }],
  datasetList: [{ datasetId: 'dataset1', datasetName: '数据集1' }],
  creator: 'creator1',
  ownerList: ['owner1'],
}));

const mockDatasets = [
  { datasetId: 'dataset1', datasetName: '数据集1' },
  { datasetId: 'dataset2', datasetName: '数据集2' },
];

const mockOwners = [
  { misId: 'owner1', avatarUrl: '' },
  { misId: 'owner2', avatarUrl: '' },
];

export const handlers = [
  // Query verbals
  http.get('/api/verbalQuery', ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get('page')) || 1;
    const pageSize = Number(url.searchParams.get('pageSize')) || 50;
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    
    const response: VerbalQueryResponse = {
      code: 0,
      msg: 'success',
      data: {
        verbalList: mockVerbals.slice(start, end),
        total: mockVerbals.length,
      },
    };
    
    return HttpResponse.json(response);
  }),

  // Get suggested datasets
  http.get('/api/verbalGetSuggestDataset', () => {
    const response: SuggestDatasetResponse = {
      code: 0,
      msg: 'success',
      data: mockDatasets,
    };
    
    return HttpResponse.json(response);
  }),

  // Get suggested owners
  http.get('/api/verbalGetSuggest', () => {
    const response: SuggestOwnerResponse = {
      code: 0,
      msg: 'success',
      data: mockOwners,
    };
    
    return HttpResponse.json(response);
  }),

  // Batch modify dataset
  http.post('/api/verbalBatchModifyDataset', () => {
    const response: BaseResponse = {
      code: 0,
      msg: 'success',
    };
    
    return HttpResponse.json(response);
  }),

  // Batch modify owner
  http.post('/api/verbalBatchModifyOwner', () => {
    const response: BaseResponse = {
      code: 0,
      msg: 'success',
    };
    
    return HttpResponse.json(response);
  }),

  // Import verbal
  http.post('/api/importXcVerbal', () => {
    const response: BaseResponse = {
      code: 0,
      msg: 'success',
    };
    
    return HttpResponse.json(response);
  }),

  // Add/modify verbal
  http.post('/api/:operation(verbalAdd|verbalModify)', () => {
    const response: BaseResponse = {
      code: 0,
      msg: 'success',
    };
    
    return HttpResponse.json(response);
  }),
];
