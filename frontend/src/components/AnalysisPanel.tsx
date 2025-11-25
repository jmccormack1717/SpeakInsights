/** Panel displaying textual analysis and insights */
import type { TextualAnalysis } from '../types';
import { Lightbulb, TrendingUp, AlertCircle } from 'lucide-react';

export function AnalysisPanel({ analysis }: { analysis: TextualAnalysis }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold flex items-center gap-2">
        <Lightbulb className="w-6 h-6 text-yellow-500" />
        Analysis & Insights
      </h2>

      {/* Executive Summary */}
      {analysis.summary && (
        <div>
          <h3 className="text-lg font-semibold mb-2">Summary</h3>
          <p className="text-gray-700 leading-relaxed">{analysis.summary}</p>
        </div>
      )}

      {/* Key Findings */}
      {analysis.key_findings && analysis.key_findings.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            Key Findings
          </h3>
          <ul className="space-y-2">
            {analysis.key_findings.map((finding, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-blue-500 mt-1">•</span>
                <span className="text-gray-700">{finding}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Patterns */}
      {analysis.patterns && analysis.patterns.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-3">Notable Patterns</h3>
          <ul className="space-y-2">
            {analysis.patterns.map((pattern, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-purple-500 mt-1">•</span>
                <span className="text-gray-700">{pattern}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {analysis.recommendations && analysis.recommendations.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-green-500" />
            Recommendations
          </h3>
          <ul className="space-y-2">
            {analysis.recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span className="text-gray-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

