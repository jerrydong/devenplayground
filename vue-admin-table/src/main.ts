import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'

function prepare() {
  console.log('Starting prepare function...');
  if (import.meta.env.DEV || window.location.hostname.includes('devinapps.com')) {
    console.log('Environment check passed, initializing MSW...');
    return import('./mocks/browser')
      .then(({ worker }) => {
        console.log('MSW worker imported successfully');
        return worker.start({
          onUnhandledRequest: 'bypass',
        });
      })
      .then(() => {
        console.log('MSW worker started successfully');
        return fetch('/api/cities?page=1&pageSize=5');
      })
      .then(response => response.json())
      .then(data => {
        console.log('Test request successful:', data);
      })
      .catch(error => {
        console.error('MSW initialization failed:', error);
      });
  }
  console.log('Environment check failed, skipping MSW');
  return Promise.resolve();
}

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(Antd);

// Initialize MSW before mounting the app
prepare().then(() => {
  console.log('Mounting Vue app...');
  app.mount('#app');
  console.log('Vue app mounted');
});
