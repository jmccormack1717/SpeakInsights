# Setup Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- OpenAI API key

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   ```bash
   # Copy the example env file
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_key_here
   ```

6. **Create data directory:**
   ```bash
   mkdir -p data
   ```

7. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Creating / Using Datasets

1. **Start both backend and frontend servers**

2. **Built-in PIMA diabetes dataset (recommended starting point)**  
   - On first backend startup, a cleaned diabetes CSV (`cleaned_diabetes_dataset.csv`) is imported into `backend/data/default_user/mvp_dataset.db`.
   - In the UI, this appears as **“PIMA Diabetes Dataset”** and is selected by default.

3. **Import your own CSV via the UI (no-code)**  
   - In the **Dataset** section, use the **“Import your own CSV”** card.  
   - Choose a CSV from your machine; the app will:
     - Create a new SQLite DB for that dataset: `backend/data/{user_id}/{dataset_id}.db`
     - Import the CSV into a table and make it available to the playbooks.
   - On the free Render tier and typical dev machines, CSVs up to roughly **50MB / ~100k rows** tend to perform best for this demo.

4. **Query your data:**
   - Select the dataset you want (PIMA or your custom CSV).  
   - Ask questions like:
     - "Describe this dataset."
     - "Which features are most related to the outcome?"
     - "How does glucose relate to the diabetes outcome?"

## Example Queries

- "Describe the dataset to me like I’m new to it."
- "Which features are most strongly correlated with the outcome?"
- "Show the distribution of BMI."
- "Compare patients with diabetes vs without across key metrics."

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure virtual environment is activated
- **Database errors**: Ensure data directory exists and is writable
- **OpenAI API errors**: Check your API key in `.env` file

### Frontend Issues

- **Connection errors**: Ensure backend is running on port 8000
- **Build errors**: Try deleting `node_modules` and reinstalling
- **Port conflicts**: Change port in `vite.config.ts`

## Next Steps

- Add more datasets
- Experiment with different query types
- Customize visualizations
- Harden authentication & authorization (rate limits, roles, etc.)

