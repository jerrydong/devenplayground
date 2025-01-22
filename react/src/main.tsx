import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Initialize mock before rendering
import './mock'
console.log('Mock API initialized')

// Add debug logging for API calls
const originalFetch = window.fetch;
window.fetch = async (...args) => {
  const [url, config] = args;
  console.log('Fetch request:', {
    url,
    method: config?.method || 'GET',
    headers: config?.headers,
    body: config?.body
  });
  
  try {
    const response = await originalFetch(...args);
    const clonedResponse = response.clone();
    const responseData = await clonedResponse.text();
    console.log('Fetch response:', {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries()),
      data: responseData
    });
    return response;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
