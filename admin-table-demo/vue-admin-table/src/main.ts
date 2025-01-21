import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'

async function prepare() {
  console.log('Starting prepare function...');
  if (import.meta.env.DEV || window.location.hostname.includes('devinapps.com')) {
    console.log('Environment check passed, initializing MSW...');
    try {
      const { worker } = await import('./mocks/browser').catch(e => {
        console.error('Failed to import MSW browser:', e);
        throw e;
      });
      console.log('MSW worker imported successfully');
      
      await worker.start({
        onUnhandledRequest: 'bypass',
      }).catch(e => {
        console.error('Failed to start MSW worker:', e);
        throw e;
      });
      console.log('MSW worker started successfully');
      
      // Test MSW by making a request
      try {
        const response = await fetch('/api/cities?page=1&pageSize=5');
        const data = await response.json();
        console.log('Test request successful:', data);
      } catch (e) {
        console.error('Test request failed:', e);
      }
    } catch (error) {
      console.error('MSW initialization failed:', error);
      throw error; // Re-throw to see the error in the console
    }
  } else {
    console.log('Environment check failed, skipping MSW');
  }
}

// Wait for MSW to initialize before mounting the app
await prepare();
console.log('Mounting Vue app...');

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')
console.log('Vue app mounted');
