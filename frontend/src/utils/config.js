// src/config.js

export const APP_NAME = "LifeNote";

export function getApiBaseUrl() {
  if (import.meta.env.DEV) {
    return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8040';
  } else {
    return window.__APP_CONFIG__?.VITE_API_BASE_URL || 'http://localhost:8040';
  }
}

