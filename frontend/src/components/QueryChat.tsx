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
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={
            currentDatasetId
              ? "Ask a question about your data..."
              : "Please select a dataset first"
          }
          disabled={isLoading || !currentDatasetId}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim() || !currentDatasetId}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Query
            </>
          )}
        </button>
      </form>
    </div>
  );
}

