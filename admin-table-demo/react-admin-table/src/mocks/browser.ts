import { setupWorker } from 'msw/browser';
import { handlers } from '../services/mockCityApi';

// Configure worker with more detailed options
export const worker = setupWorker(...handlers);

// Add custom configuration for debugging
worker.events.on('request:match', ({ request }) => {
  console.log('MSW matched request:', request.method, request.url);
});

worker.events.on('response:mocked', ({ request, response }) => {
  console.log('MSW mocked response:', request.method, request.url, response.status);
});

worker.events.on('request:unhandled', ({ request }) => {
  console.warn('MSW unhandled request:', request.method, request.url);
});
