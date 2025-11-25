/** Main query chat interface */
import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { useQueryStore } from '../stores/queryStore';
import { queryApi } from '../services/api';
import type { QueryRequest } from '../types';

export function QueryChat() {
  const [query, setQuery] = useState('');
  const { 
    isLoading, 
    setLoading, 
    setError, 
    setResponse,
    currentUserId,
    currentDatasetId 
  } = useQueryStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim() || !currentDatasetId) {
      setError('Please enter a query and select a dataset');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const request: QueryRequest = {
        user_id: currentUserId,
        dataset_id: currentDatasetId,
        query: query.trim(),
      };

      const response = await queryApi.executeQuery(request);
      setResponse(response);
      setQuery(''); // Clear input after successful query
    } catch (error: any) {
      setError(error.response?.data?.detail || error.message || 'Query failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <div className="mb-3">
        <label className="text-sm font-medium text-gray-700">Ask a Question</label>
      </div>
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={
              currentDatasetId
                ? "e.g., What's the average glucose level? Show me the distribution of outcomes..."
                : "Please select a dataset first"
            }
            disabled={isLoading || !currentDatasetId}
            className="w-full px-5 py-4 pr-12 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-50 disabled:cursor-not-allowed text-gray-900 placeholder:text-gray-400 shadow-sm transition-all"
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !query.trim() || !currentDatasetId}
          className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-xl hover:from-indigo-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium shadow-md hover:shadow-lg transition-all min-w-[120px]"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span className="hidden sm:inline">Processing</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Query</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}

