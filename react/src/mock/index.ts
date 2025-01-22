import Mock from 'mockjs';
import type { VerbalQueryResponse, SuggestDatasetResponse, SuggestOwnerResponse, BaseResponse } from '../types/api';

const Random = Mock.Random;

// Override fetch to handle mock API requests
const originalFetch = window.fetch;
window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof input === 'string' ? input : input instanceof URL ? input.href : new URL(input.url).href;
  console.log('Mock intercepting fetch:', { url, init });

  // Helper function to create mock response
  const createMockResponse = (data: any) => {
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  };

  // verbalQuery endpoint
  if (url.match(/\/api\/verbalQuery/)) {
    const params = new URLSearchParams(url.split('?')[1]);
    const page = parseInt(params.get('page') || '1');
    const pageSize = parseInt(params.get('pageSize') || '50');

    const response: VerbalQueryResponse = {
      code: 0,
      msg: 'success',
      data: {
        verbalList: Array(pageSize).fill(null).map((_, index) => ({
          id: (page - 1) * pageSize + index + 1,
          name: Random.word(5, 10),
          contentList: [{ id: Random.natural(), content: Random.sentence(10, 20) }],
          datasetList: Array(Random.natural(1, 3)).fill(null).map(() => ({
            datasetId: Random.guid(),
            datasetName: Random.word(3, 8)
          })),
          creator: Random.name(),
          ownerList: Array(Random.natural(1, 2)).fill(null).map(() => Random.name())
        })),
        total: 200
      }
    };
    return createMockResponse(response);
  }
  // verbalGetSuggestDataset endpoint
  if (url.match(/\/api\/verbalGetSuggestDataset/)) {
    const response: SuggestDatasetResponse = {
      code: 0,
      msg: 'success',
      data: Array(Random.natural(5, 10)).fill(null).map(() => ({
        datasetId: Random.guid(),
        datasetName: Random.word(3, 8)
      }))
    };
    return createMockResponse(response);
  }

  // verbalGetSuggest endpoint
  if (url.match(/\/api\/verbalGetSuggest/)) {
    const response: SuggestOwnerResponse = {
      code: 0,
      msg: 'success',
      data: Array(Random.natural(3, 8)).fill(null).map(() => ({
        misId: Random.guid(),
        avatarUrl: Random.image('100x100')
      }))
    };
    return createMockResponse(response);
  }

  // verbalIsNameValid endpoint
  if (url.match(/\/api\/verbalIsNameValid/)) {
    return createMockResponse({
      code: 0,
      msg: 'success',
      data: true
    });
  }

  // POST endpoints with success response
  if (
    url.match(/\/api\/verbalAdd/) ||
    url.match(/\/api\/verbalModify/) ||
    url.match(/\/api\/importXcVerbal/) ||
    url.match(/\/api\/verbalBatchModifyOwner/) ||
    url.match(/\/api\/verbalBatchModifyDataset/)
  ) {
    const successResponse: BaseResponse = {
      code: 0,
      msg: 'success'
    };
    return createMockResponse(successResponse);
  }

  // If no mock matches, pass through to original fetch
  return originalFetch(input, init);
};
