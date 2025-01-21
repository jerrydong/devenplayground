import Mock from 'mockjs';

// Common response template
export const baseResponseTemplate = {
  'code': '@pick([0, 1])',
  'msg': function() {
    return this.code === 0 ? 'success' : '@sentence(3, 5)';
  }
};

// Dataset template
export const datasetTemplate = {
  'datasetId': '@id',
  'datasetName': '@pick(["客服知识库", "产品介绍", "常见问题", "售后服务"])'
};

// Owner template
export const ownerTemplate = {
  'misId': '@word(5,10)',
  'avatarUrl': '@image("200x200")'
};

// Content item template
export const contentItemTemplate = {
  'id|+1': 1,
  'content': '@paragraph(1, 3)'
};

// Verbal item template
export const verbalItemTemplate = {
  'id|+1': 1,
  'name': '@word(5,10)',
  'contentList|1-3': [contentItemTemplate],
  'datasetList|1-3': [datasetTemplate],
  'creator': '@pick(["zhang.san", "li.si", "wang.wu", "zhao.liu"])',
  'ownerList|1-2': ['@pick(["zhang.san", "li.si", "wang.wu", "zhao.liu"])']
};

// Helper function to generate mock data with proper typing
export function generateMockData<T>(template: Record<string, any>): T {
  return Mock.mock(template) as T;
}

// Helper function to generate mock list with proper typing
export function generateMockList<T>(
  template: Record<string, any>,
  count: number
): T[] {
  return Mock.mock({
    [`list|${count}`]: [template]
  }).list as T[];
}
