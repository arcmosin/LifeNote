// src/config.js

export const APP_NAME = "LifeNote";

export function getApiBaseUrl() {
    return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8040';
}

