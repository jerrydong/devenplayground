import { http, HttpResponse } from 'msw';
import type { 
  VerbalItem, 
  VerbalQueryResponse, 
  SuggestDatasetResponse,
  SuggestOwnerResponse,
  BaseResponse 
} from '../types/api';

// Mock data
const mockDatasets = [
  { datasetId: 'dataset1', datasetName: '客服知识库' },
  { datasetId: 'dataset2', datasetName: '产品介绍' },
  { datasetId: 'dataset3', datasetName: '常见问题' },
  { datasetId: 'dataset4', datasetName: '售后服务' },
];

const mockOwners = [
  { misId: 'zhang.san', avatarUrl: '' },
  { misId: 'li.si', avatarUrl: '' },
  { misId: 'wang.wu', avatarUrl: '' },
  { misId: 'zhao.liu', avatarUrl: '' },
];

const mockVerbals: VerbalItem[] = Array.from({ length: 50 }, (_, index) => {
  const datasetCount = Math.floor(Math.random() * 3) + 1; // 1-3 datasets
  const ownerCount = Math.floor(Math.random() * 2) + 1; // 1-2 owners
  
  return {
    id: index + 1,
    name: `话术${String(index + 1).padStart(3, '0')}`,
    contentList: [
      { 
        id: index + 1, 
        content: `这是第${index + 1}条话术的示例内容，包含了完整的对话场景和回复建议。${
          index % 3 === 0 ? '适用于客服咨询场景。' : 
          index % 3 === 1 ? '用于产品介绍和功能说明。' : 
          '针对售后服务和问题处理。'
        }`
      }
    ],
    datasetList: mockDatasets
      .slice(0, datasetCount)
      .map(ds => ({ ...ds })),
    creator: mockOwners[index % mockOwners.length].misId,
    ownerList: mockOwners
      .slice(0, ownerCount)
      .map(owner => owner.misId),
  };
});

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
