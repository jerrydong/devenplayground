import { setupWorker } from 'msw/browser';
import { handlers } from '../services/mockCityApi';

export const worker = setupWorker(...handlers);
