# Quick Start Guide

Get up and running in 5 minutes!

## 1. Backend Setup (2 minutes)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp env.example .env
```

**Edit `.env` and add your OpenAI API key:**
```
OPENAI_API_KEY=sk-your-key-here
```

**Start the server:**
```bash
uvicorn app.main:app --reload
```

✅ Backend running at `http://localhost:8000`

## 2. Frontend Setup (2 minutes)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## 3. Create Sample Data (1 minute)

**Option A: Upload CSV (Easiest)**
1. In the UI, click "New Dataset" → name it "sales_data"
2. Click "Upload CSV" on the dataset card
3. Upload `backend/data/sample_sales.csv` (or any CSV file)
4. Done! ✅

**Option B: Use the script**
```bash
cd backend
python scripts/create_sample_data.py
```

**Option C: Manual SQLite**
```bash
sqlite3 data/default_user/sales_data.db
```

Then run:
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT,
    product TEXT,
    amount REAL,
    quarter TEXT,
    date DATE
);

INSERT INTO sales VALUES
    (1, 'North', 'Product A', 50000, 'Q4', '2024-10-01'),
    (2, 'South', 'Product A', 45000, 'Q4', '2024-10-15'),
    (3, 'East', 'Product B', 60000, 'Q4', '2024-11-01'),
    (4, 'West', 'Product B', 55000, 'Q4', '2024-11-15');
```

## 4. Try It Out!

1. Open `http://localhost:5173`
2. Create or select a dataset
3. Ask a question: **"Show me sales by region"**
4. See the magic! 🎉

## Example Queries

- "Show me total sales by region"
- "What are the top products by revenue?"
- "Compare sales across quarters"
- "Show me sales trends over time"

## Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.11+)
- Check virtual environment is activated
- Verify `.env` file exists with API key

**Frontend won't start?**
- Check Node version: `node --version` (need 18+)
- Try deleting `node_modules` and running `npm install` again

**No results?**
- Make sure you have data in your database
- Check backend logs for errors
- Verify dataset is selected in the UI

## Next Steps

- Add your own data
- Experiment with different queries
- Check out the API docs at `http://localhost:8000/docs`

