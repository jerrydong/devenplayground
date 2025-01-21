import { http, HttpResponse } from 'msw';
import Mock from 'mockjs';
import type { 
  VerbalItem, 
  VerbalQueryResponse, 
  SuggestDatasetResponse,
  SuggestOwnerResponse,
  BaseResponse,
  VerbalNameValidResponse,
  AddModifyVerbalRequest,
  DatasetInfo
} from '../types/api';
import {
  verbalItemTemplate,
  datasetTemplate,
  ownerTemplate,
  baseResponseTemplate,
  generateMockList,
  generateMockData
} from './mockTemplates';

export const handlers = [
  // Query verbals
  http.get('/api/verbalQuery', ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get('page')) || 1;
    const pageSize = Number(url.searchParams.get('pageSize')) || 50;
    const verbalName = url.searchParams.get('verbalName');
    const verbalContent = url.searchParams.get('verbalContent');
    const datasetName = url.searchParams.get('datasetName');
    const creator = url.searchParams.get('creator');
    const owner = url.searchParams.get('owner');

    // Generate consistent mock data using a seed
    Mock.Random.seed(123);
    const verbals = generateMockList<VerbalItem>(verbalItemTemplate, 50);
    Mock.Random.seed(); // Reset seed
    
    // Map the verbals to have consistent, searchable names
    const mappedVerbals = verbals.map((verbal, index) => ({
      ...verbal,
      name: `话术${String(index + 1).padStart(3, '0')}`,
      contentList: [{
        id: verbal.contentList[0].id,
        content: `这是第${index + 1}条话术的示例内容，包含了完整的对话场景和回复建议。${
          index % 3 === 0 ? '适用于客服咨询场景。' :
          index % 3 === 1 ? '用于产品介绍和功能说明。' :
          '针对售后服务和问题处理。'
        }`
      }]
    }));
    
    let filteredVerbals = [...mappedVerbals];

    // Apply filters
    if (verbalName) {
      filteredVerbals = filteredVerbals.filter(v => v.name.includes(verbalName));
    }
    if (verbalContent) {
      filteredVerbals = filteredVerbals.filter(v => 
        v.contentList.some(c => c.content.includes(verbalContent))
      );
    }
    if (datasetName) {
      filteredVerbals = filteredVerbals.filter(v => 
        v.datasetList.some(d => d.datasetName.includes(datasetName))
      );
    }
    if (creator) {
      filteredVerbals = filteredVerbals.filter(v => v.creator.includes(creator));
    }
    if (owner) {
      filteredVerbals = filteredVerbals.filter(v => 
        v.ownerList.some(o => o.includes(owner))
      );
    }

    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    
    const response = generateMockData<VerbalQueryResponse>({
      ...baseResponseTemplate,
      data: {
        verbalList: filteredVerbals.slice(start, end),
        total: filteredVerbals.length,
      },
    });
    
    return HttpResponse.json(response);
  }),

  // Get suggested datasets
  http.get('/api/verbalGetSuggestDataset', () => {
    const datasets = generateMockList<DatasetInfo>(datasetTemplate, 4);
    const response = generateMockData<SuggestDatasetResponse>({
      ...baseResponseTemplate,
      data: datasets,
    });
    
    return HttpResponse.json(response);
  }),

  // Get suggested owners
  http.get('/api/verbalGetSuggest', () => {
    const owners = generateMockList<{ misId: string; avatarUrl: string }>(ownerTemplate, 4);
    const response = generateMockData<SuggestOwnerResponse>({
      ...baseResponseTemplate,
      data: owners,
    });
    
    return HttpResponse.json(response);
  }),

  // Batch modify dataset
  http.post('/api/verbalBatchModifyDataset', () => {
    const response = generateMockData<BaseResponse>(baseResponseTemplate);
    return HttpResponse.json(response);
  }),

  // Batch modify owner
  http.post('/api/verbalBatchModifyOwner', () => {
    const response = generateMockData<BaseResponse>(baseResponseTemplate);
    return HttpResponse.json(response);
  }),

  // Import verbal
  http.post('/api/importXcVerbal', () => {
    const response = generateMockData<BaseResponse>(baseResponseTemplate);
    return HttpResponse.json(response);
  }),

  // Add/modify verbal
  http.post('/api/:operation(verbalAdd|verbalModify)', async ({ request }) => {
    try {
      const data = await request.json() as AddModifyVerbalRequest;
      // Validate required fields
      if (!data?.name || !data?.contentList?.length || !data?.ownerList?.length || !data?.datasetList?.length) {
        return HttpResponse.json({
          code: 1,
          msg: '缺少必要字段',
        } as BaseResponse);
      }
      
      const response = generateMockData<BaseResponse>({
        ...baseResponseTemplate,
        code: 0, // Force success for valid requests
      });
      return HttpResponse.json(response);
    } catch (error) {
      return HttpResponse.json({
        code: 1,
        msg: '请求数据格式错误',
      } as BaseResponse);
    }
  }),

  // Check verbal name validity
  http.get('/api/verbalIsNameValid', ({ request }) => {
    try {
      const url = new URL(request.url);
      const verbalName = url.searchParams.get('verbalName');
      
      if (!verbalName) {
        return HttpResponse.json({
          code: 1,
          msg: '话术名称不能为空',
          data: false,
        } as VerbalNameValidResponse);
      }

      // Generate mock validation response
      const response = generateMockData<VerbalNameValidResponse>({
        ...baseResponseTemplate,
        code: 0, // Force success for valid name
        data: Math.random() > 0.2, // 80% chance of name being valid
      });
      return HttpResponse.json(response);
    } catch (error) {
      return HttpResponse.json({
        code: 1,
        msg: '请求参数错误',
        data: false,
      } as VerbalNameValidResponse);
    }
  }),
];
