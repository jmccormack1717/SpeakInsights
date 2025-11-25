/** Dataset selector component - MVP: Hardcoded single dataset */
import { useEffect } from 'react';
import { Database, CheckCircle2 } from 'lucide-react';
import { useQueryStore } from '../stores/queryStore';

// Hardcoded dataset for MVP
const HARDCODED_DATASET = {
  dataset_id: 'mvp_dataset',
  name: 'Diabetes Dataset',
};

export function DatasetSelector() {
  const {
    currentDatasetId,
    setDatasetId,
  } = useQueryStore();

  useEffect(() => {
    // Auto-select the hardcoded dataset
    if (!currentDatasetId || currentDatasetId !== HARDCODED_DATASET.dataset_id) {
      setDatasetId(HARDCODED_DATASET.dataset_id);
    }
  }, [currentDatasetId, setDatasetId]);

  return (
    <div className="w-full">
      <div className="flex items-center gap-2 mb-3">
        <Database className="w-5 h-5 text-indigo-600" />
        <h2 className="text-lg font-semibold text-gray-800">Active Dataset</h2>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200/60 p-5 hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-lg flex items-center justify-center shadow-sm">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 text-lg">{HARDCODED_DATASET.name}</h3>
              <p className="text-sm text-gray-500 mt-0.5">Ready to query</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 text-sm font-medium rounded-full border border-green-200">
            <CheckCircle2 className="w-4 h-4" />
            <span>Active</span>
          </div>
        </div>
      </div>
    </div>
  );
}

