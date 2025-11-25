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
      <div className="w-full max-w-4xl mx-auto mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-800">Error: {error}</p>
      </div>
    );
  }

  if (!currentResponse) {
    return null;
  }

  return (
    <div className="w-full max-w-4xl mx-auto mt-6 space-y-6">
      {/* SQL Query Toggle */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg">
        <button
          onClick={() => setShowSql(!showSql)}
          className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 rounded-lg"
        >
          <div className="flex items-center gap-2">
            <Code className="w-5 h-5" />
            <span className="font-medium">Generated SQL Query</span>
          </div>
          {showSql ? (
            <ChevronUp className="w-5 h-5" />
          ) : (
            <ChevronDown className="w-5 h-5" />
          )}
        </button>
        {showSql && (
          <div className="px-4 pb-4">
            <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-sm">
              {currentResponse.sql}
            </pre>
          </div>
        )}
      </div>

      {/* Visualization */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <ChartRenderer config={currentResponse.visualization} />
      </div>

      {/* Textual Analysis */}
      <AnalysisPanel analysis={currentResponse.analysis} />

      {/* Raw Data Toggle */}
      {currentResponse.results.length > 0 && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg">
          <button
            onClick={() => setShowRawData(!showRawData)}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 rounded-lg"
          >
            <span className="font-medium">
              Raw Data ({currentResponse.results.length} rows)
            </span>
            {showRawData ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </button>
          {showRawData && (
            <div className="px-4 pb-4">
              <div className="overflow-x-auto">
                <table className="min-w-full border-collapse border border-gray-300 text-sm">
                  <thead>
                    <tr className="bg-gray-100">
                      {Object.keys(currentResponse.results[0]).map((col) => (
                        <th key={col} className="border border-gray-300 px-3 py-2 text-left">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {currentResponse.results.slice(0, 50).map((row, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        {Object.keys(row).map((col) => (
                          <td key={col} className="border border-gray-300 px-3 py-2">
                            {row[col]?.toString() || ''}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {currentResponse.results.length > 50 && (
                  <p className="mt-2 text-sm text-gray-500">
                    Showing first 50 of {currentResponse.results.length} rows
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

