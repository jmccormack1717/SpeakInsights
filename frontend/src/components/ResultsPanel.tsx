/** Results panel showing visualization and analysis */
import { useQueryStore } from '../stores/queryStore';
import { ChartRenderer } from './ChartRenderer';
import { AnalysisPanel } from './AnalysisPanel';
import { ChevronDown, ChevronUp, Code } from 'lucide-react';
import { useState } from 'react';

export function ResultsPanel() {
  const { currentResponse, error } = useQueryStore();
  const [showSql, setShowSql] = useState(false);
  const [showRawData, setShowRawData] = useState(false);

  if (error) {
    return (
      <div className="w-full mt-6 p-5 bg-red-50 border-l-4 border-red-500 rounded-lg shadow-sm">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <svg className="w-5 h-5 text-red-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-red-800 mb-1">Query Error</h3>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!currentResponse) {
    return (
      <div className="w-full mt-8 text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-100 mb-4">
          <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p className="text-gray-500 text-lg">Ask a question to see results</p>
        <p className="text-gray-400 text-sm mt-2">Your query will generate a visualization and analysis</p>
      </div>
    );
  }

  return (
    <div className="w-full mt-6 space-y-5">
      {/* Visualization - Prominent */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200/60 p-6 sm:p-8">
        <ChartRenderer config={currentResponse.visualization} />
      </div>

      {/* Textual Analysis */}
      <AnalysisPanel analysis={currentResponse.analysis} />

      {/* SQL Query Toggle */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200/60 overflow-hidden">
        <button
          onClick={() => setShowSql(!showSql)}
          className="w-full px-5 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <Code className="w-5 h-5 text-gray-500" />
            <span className="font-medium text-gray-700">View Generated SQL</span>
          </div>
          {showSql ? (
            <ChevronUp className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-400" />
          )}
        </button>
        {showSql && (
          <div className="px-5 pb-5 border-t border-gray-100">
            <pre className="mt-4 bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm font-mono leading-relaxed">
              {currentResponse.sql}
            </pre>
          </div>
        )}
      </div>

      {/* Raw Data Toggle */}
      {currentResponse.results.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200/60 overflow-hidden">
          <button
            onClick={() => setShowRawData(!showRawData)}
            className="w-full px-5 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <span className="font-medium text-gray-700">
              Raw Data <span className="text-gray-500 font-normal">({currentResponse.results.length} rows)</span>
            </span>
            {showRawData ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </button>
          {showRawData && (
            <div className="px-5 pb-5 border-t border-gray-100">
              <div className="mt-4 overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      {Object.keys(currentResponse.results[0]).map((col) => (
                        <th key={col} className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {currentResponse.results.slice(0, 50).map((row, idx) => (
                      <tr key={idx} className="hover:bg-gray-50 transition-colors">
                        {Object.keys(row).map((col) => (
                          <td key={col} className="px-4 py-3 text-gray-900 whitespace-nowrap">
                            {row[col]?.toString() || ''}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {currentResponse.results.length > 50 && (
                  <div className="bg-gray-50 px-4 py-3 text-sm text-gray-500 text-center border-t border-gray-200">
                    Showing first 50 of {currentResponse.results.length} rows
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

