/** Main application component */
import { QueryChat } from './components/QueryChat';
import { ResultsPanel } from './components/ResultsPanel';
import { DatasetSelector } from './components/DatasetSelector';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            SpeakInsights
          </h1>
          <p className="text-gray-600 mt-1">
            Prompt-driven data analytics platform
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <DatasetSelector />
        <QueryChat />
        <ResultsPanel />
      </main>
    </div>
  );
}

export default App;

