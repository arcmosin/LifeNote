import './assets/main.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia';

import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import * as config from '@/utils/config'; // 导入所有配置
import eventBus from 'vue3-eventbus'


const pinia = createPinia();
const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// API挂载到全局属性（在组件内可通过 `this.$config` 访问）
app.config.globalProperties.$config = config;

app.use(eventBus)
app.use(ElementPlus);
app.use(pinia);

app.mount('#app')
