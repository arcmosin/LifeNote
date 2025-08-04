// src/config.js

export const APP_NAME = "LifeNote";

let API_BASE_URL;

// 开发模式下用默认或环境变量
if (import.meta.env.DEV) {
  API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8040';
} else {
  // 生产模式用运行时注入配置
  API_BASE_URL = window.__APP_CONFIG__?.VITE_API_BASE_URL || 'http://localhost:8040';
}

export { API_BASE_URL };
