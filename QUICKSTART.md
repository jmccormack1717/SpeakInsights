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

## 3. Demo Dataset (PIMA Diabetes)

For the current demo, the backend will automatically import a **cleaned PIMA diabetes dataset**
if it doesn't find a database for the default user.

Place a CSV file named `cleaned_diabetes_dataset.csv` in one of these locations (if it’s not already there):

- `backend/cleaned_diabetes_dataset.csv`
- `cleaned_diabetes_dataset.csv` (project root)
- `backend/data/cleaned_diabetes_dataset.csv`

Then start the backend. On first run, it will create `backend/data/default_user/mvp_dataset.db`
and import the CSV into it.

## 4. Try It Out! (Built-in + Your Own CSV)

1. Open `http://localhost:5173`
2. Use the **PIMA diabetes dataset** (default) or upload your own CSV (see Dataset card)
3. Ask a question, e.g.: **"Describe the dataset"** or **"Which features are most related to the outcome?"**
4. See the magic! 🎉

## Example Queries

- "Describe this dataset to me."
- "Which features are most strongly related to the outcome?"
- "How does glucose relate to the diabetes outcome?"
- "Show the distribution of BMI."

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

