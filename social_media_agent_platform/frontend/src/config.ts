// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Auth endpoints
export const AUTH_ENDPOINTS = {
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  REFRESH: '/auth/refresh',
  ME: '/auth/me',
};

// Agent endpoints
export const AGENT_ENDPOINTS = {
  AGENTS: '/agents',
  AGENT_BY_ID: (id: string) => `/agents/${id}`,
  AGENT_EXECUTE: (id: string) => `/agents/${id}/execute`,
};

// Social endpoints
export const SOCIAL_ENDPOINTS = {
  ACCOUNTS: '/social/accounts',
  ACCOUNT_BY_ID: (id: string) => `/social/accounts/${id}`,
  POSTS: '/social/posts',
  POST_BY_ID: (id: string) => `/social/posts/${id}`,
};

// Vector store endpoints
export const VECTOR_STORE_ENDPOINTS = {
  COLLECTIONS: '/vector/collections',
  COLLECTION_BY_ID: (id: string) => `/vector/collections/${id}`,
  VECTORS: (collectionId: string) => `/vector/collections/${collectionId}/vectors`,
  VECTOR_BY_ID: (collectionId: string, vectorId: string) => 
    `/vector/collections/${collectionId}/vectors/${vectorId}`,
  SEARCH: (collectionId: string) => `/vector/collections/${collectionId}/search`,
  DOCUMENTS: (collectionId: string) => `/vector/collections/${collectionId}/documents`,
  DOCUMENT_BY_ID: (collectionId: string, documentId: string) => 
    `/vector/collections/${collectionId}/documents/${documentId}`,
};

// Default request headers
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  Accept: 'application/json',
};

// Local storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
};
