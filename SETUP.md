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

## Creating Your First Dataset

1. **Start both backend and frontend servers**

2. **In the frontend:**
   - Click "New Dataset" to create a dataset
   - Give it a name (e.g., "sales_data")

3. **Add data to your dataset:**
   
   **Option A: Upload CSV (Recommended)**
   - Click "Upload CSV" button on your dataset card
   - Select a CSV file from your computer
   - The system will automatically create a table and import the data
   - Sample CSV available at: `backend/data/sample_sales.csv`
   
   **Option B: Manual SQL (Advanced)**
   
   The dataset will be created at: `backend/data/{user_id}/{dataset_id}.db`
   
   You can use any SQLite tool to add tables and data:
   
   ```bash
   # Using sqlite3 command line
   sqlite3 backend/data/default_user/sales_data.db
   
   # Create a sample table
   CREATE TABLE sales (
       id INTEGER PRIMARY KEY,
       region TEXT,
       product TEXT,
       amount REAL,
       quarter TEXT,
       date DATE
   );
   
   # Insert sample data
   INSERT INTO sales (region, product, amount, quarter, date) VALUES
       ('North', 'Product A', 50000, 'Q4', '2024-10-01'),
       ('South', 'Product A', 45000, 'Q4', '2024-10-15'),
       ('East', 'Product B', 60000, 'Q4', '2024-11-01'),
       ('West', 'Product B', 55000, 'Q4', '2024-11-15');
   ```

4. **Query your data:**
   - Select your dataset in the frontend
   - Type a query like: "Show me sales by region for Q4"
   - See the results with visualization and analysis!

## Example Queries

- "Show me total sales by region"
- "What are the top 5 products by revenue?"
- "Show me sales trends over time"
- "Compare sales across different regions"
- "What is the average sales amount?"

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
- Add authentication (Phase 2)

