import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { API_BASE_URL, DEFAULT_HEADERS, STORAGE_KEYS } from '../config';

class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;

  private constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: DEFAULT_HEADERS,
      withCredentials: true,
    });

    this.setupInterceptors();
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error: AxiosError) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;
        
        // If the error status is 401 and we haven't tried to refresh the token yet
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
            if (refreshToken) {
              const response = await this.refreshToken(refreshToken);
              const { access_token, refresh_token } = response.data;
              
              localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
              if (refresh_token) {
                localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh_token);
              }
              
              // Update the authorization header
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
              
              // Retry the original request
              return this.api(originalRequest);
            }
          } catch (error) {
            // If refresh token fails, clear auth data and redirect to login
            this.clearAuthData();
            window.location.href = '/login';
            return Promise.reject(error);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Auth methods
  public async login(credentials: { email: string; password: string }): Promise<any> {
    const response = await this.api.post('/auth/login', credentials);
    this.setAuthData(response.data);
    return response.data;
  }

  public async register(userData: { email: string; password: string; full_name: string }): Promise<any> {
    const response = await this.api.post('/auth/register', userData);
    return response.data;
  }

  public async refreshToken(refreshToken: string): Promise<any> {
    const response = await this.api.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  }

  public async getCurrentUser(): Promise<any> {
    const response = await this.api.get('/users/me');
    return response.data;
  }

  // Agent methods
  public async getAgents(): Promise<any> {
    const response = await this.api.get('/agents');
    return response.data;
  }

  public async getAgentById(id: string): Promise<any> {
    const response = await this.api.get(`/agents/${id}`);
    return response.data;
  }

  public async createAgent(agentData: any): Promise<any> {
    const response = await this.api.post('/agents', agentData);
    return response.data;
  }

  public async updateAgent(id: string, agentData: any): Promise<any> {
    const response = await this.api.put(`/agents/${id}`, agentData);
    return response.data;
  }

  public async deleteAgent(id: string): Promise<void> {
    await this.api.delete(`/agents/${id}`);
  }

  // Social account methods
  public async getSocialAccounts(): Promise<any> {
    const response = await this.api.get('/social/accounts');
    return response.data;
  }

  public async connectSocialAccount(platform: string, data: any): Promise<any> {
    const response = await this.api.post(`/social/accounts/connect/${platform}`, data);
    return response.data;
  }

  // Vector store methods
  public async getVectorCollections(): Promise<any> {
    const response = await this.api.get('/vector/collections');
    return response.data;
  }

  public async searchVectors(collectionId: string, query: string, k: number = 5): Promise<any> {
    const response = await this.api.post(`/vector/collections/${collectionId}/search`, {
      query,
      k,
    });
    return response.data;
  }

  // Helper methods
  private setAuthData(authData: { access_token: string; refresh_token: string; user: any }): void {
    const { access_token, refresh_token, user } = authData;
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh_token);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
  }

  public clearAuthData(): void {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  }

  public isAuthenticated(): boolean {
    return !!localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  }

  // Utility method for making requests
  public async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.api.request<T>(config);
    return response.data;
  }
}

export const apiService = ApiService.getInstance();
