/** API client for backend communication */
import axios from 'axios';
import type { QueryRequest, QueryResponse, Dataset } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryApi = {
  /**
   * Execute a natural language query
   */
  async executeQuery(request: QueryRequest): Promise<QueryResponse> {
    const response = await apiClient.post<QueryResponse>('/query', request);
    return response.data;
  },
};

export const datasetApi = {
  /**
   * List all datasets for a user
   */
  async listDatasets(userId: string): Promise<Dataset[]> {
    const response = await apiClient.get<Dataset[]>(`/datasets/${userId}`);
    return response.data;
  },

  /**
   * Create a new dataset
   */
  async createDataset(
    userId: string,
    datasetId: string,
    name: string,
    description?: string
  ): Promise<Dataset> {
    const response = await apiClient.post<Dataset>('/datasets', {
      user_id: userId,
      dataset_id: datasetId,
      name,
      description,
    });
    return response.data;
  },

  /**
   * Delete a dataset
   */
  async deleteDataset(userId: string, datasetId: string): Promise<void> {
    await apiClient.delete(`/datasets/${userId}/${datasetId}`);
  },

  /**
   * Get schema for a dataset
   */
  async getSchema(userId: string, datasetId: string): Promise<any> {
    const response = await apiClient.get(`/datasets/${userId}/${datasetId}/schema`);
    return response.data;
  },

  /**
   * Upload CSV file to a dataset
   */
  async uploadCSV(
    userId: string,
    datasetId: string,
    file: File,
    tableName?: string
  ): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (tableName) {
      formData.append('table_name', tableName);
    }

    const response = await apiClient.post(
      `/datasets/${userId}/${datasetId}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },
};

