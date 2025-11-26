/** Zustand store for query state management */
import { create } from 'zustand';
import type { QueryResponse, Dataset } from '../types';

interface QueryState {
  // Current query state
  isLoading: boolean;
  error: string | null;
  currentResponse: QueryResponse | null;
  
  // Dataset management
  currentUserId: string;
  currentDatasetId: string | null;
  datasets: Dataset[];
  presetQuestion: string | null;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setResponse: (response: QueryResponse | null) => void;
  setUserId: (userId: string) => void;
  setDatasetId: (datasetId: string | null) => void;
  setDatasets: (datasets: Dataset[]) => void;
  setPresetQuestion: (question: string | null) => void;
  reset: () => void;
}

const initialState = {
  isLoading: false,
  error: null,
  currentResponse: null,
  currentUserId: 'default_user',
  currentDatasetId: null,
  datasets: [],
  presetQuestion: null,
};

export const useQueryStore = create<QueryState>((set) => ({
  ...initialState,
  
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  setResponse: (response) => set({ currentResponse: response }),
  setUserId: (userId) => set({ currentUserId: userId }),
  setDatasetId: (datasetId) => set({ currentDatasetId: datasetId }),
  setDatasets: (datasets) => set({ datasets }),
  setPresetQuestion: (presetQuestion) => set({ presetQuestion }),
  reset: () => set(initialState),
}));

