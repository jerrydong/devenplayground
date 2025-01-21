import { http } from 'msw';

// Mock city data with a good variety of cities
const cityData = [
  { id: 1, name: 'New York' },
  { id: 2, name: 'London' },
  { id: 3, name: 'Tokyo' },
  { id: 4, name: 'Paris' },
  { id: 5, name: 'Shanghai' },
  { id: 6, name: 'Dubai' },
  { id: 7, name: 'Singapore' },
  { id: 8, name: 'Hong Kong' },
  { id: 9, name: 'Sydney' },
  { id: 10, name: 'Mumbai' },
  { id: 11, name: 'Berlin' },
  { id: 12, name: 'Toronto' },
  { id: 13, name: 'Seoul' },
  { id: 14, name: 'Moscow' },
  { id: 15, name: 'Madrid' },
];

export const handlers = [
  http.get('/api/cities', ({ request, params }) => {
    const url = new URL(request.url);
    const searchTerm = url.searchParams.get('search')?.toLowerCase() || '';
    const pageParam = Number(url.searchParams.get('page') || '1');
    const pageSizeParam = Number(url.searchParams.get('pageSize') || '5');

    // Filter cities by searchTerm (fuzzy)
    const filtered = cityData.filter(city => 
      city.name.toLowerCase().includes(searchTerm)
    );

    // Implement pagination
    const startIndex = (pageParam - 1) * pageSizeParam;
    const pageData = filtered.slice(startIndex, startIndex + pageSizeParam);

    return Response.json({
      data: pageData,
      total: filtered.length,
      currentPage: pageParam,
      pageSize: pageSizeParam
    });
  })
];

export const mockCityData = cityData;
