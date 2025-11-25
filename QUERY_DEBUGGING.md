# Query Debugging & Success Path

## What I've Fixed

### 1. **Fallback Query System**
- If LLM generates invalid SQL → automatically tries a simple `SELECT * FROM table LIMIT 10`
- If SQL execution fails → automatically tries the fallback query
- This ensures you'll get SOME response even if the LLM makes mistakes

### 2. **Better SQL Validation**
- Rejects PostgreSQL-specific syntax (`FROM (VALUES ...)`)
- Validates SQL before execution
- Provides clear error messages

### 3. **Improved Error Handling**
- Each step has try/catch with fallbacks
- Detailed logging at each failure point
- CORS headers always included (even on errors)

### 4. **SQLite-Specific Guidance**
- LLM prompt explicitly mentions SQLite limitations
- Examples of correct vs incorrect syntax
- Special handling for schema/column queries

## What Should Work Now

### Simple Queries (Most Likely to Work):
1. **"Show me the data"** → `SELECT * FROM diabetes LIMIT 10`
2. **"How many rows?"** → `SELECT COUNT(*) FROM diabetes`
3. **"What's the average glucose?"** → `SELECT AVG(Glucose) FROM diabetes`
4. **"Show me the first 5 rows"** → `SELECT * FROM diabetes LIMIT 5`

### Medium Complexity (Should Work):
- **"What's the distribution of outcomes?"** → `SELECT Outcome, COUNT(*) FROM diabetes GROUP BY Outcome`
- **"Show me glucose by outcome"** → `SELECT Outcome, AVG(Glucose) FROM diabetes GROUP BY Outcome`

### Complex Queries (May Need Retry):
- Schema queries ("what features do we have?") - now uses PRAGMA
- Multi-column aggregations
- Complex WHERE clauses

## Testing Strategy

### Step 1: Test the Simplest Query
Try: **"show me 10 rows"** or **"show me the data"**

This should work because:
- Simple `SELECT * FROM diabetes LIMIT 10`
- No complex logic
- Fallback will catch it if LLM fails

### Step 2: Check Backend Logs
On Render, check your backend logs. You should see:
- `CORS allowed origins: [...]`
- `MVP dataset found at ...` or import messages
- SQL queries being generated
- Any errors with full stack traces

### Step 3: Verify Database Exists
The logs will show if the database file exists. If not, the startup script should import it automatically if `diabetes.csv` is in the repo.

## If Queries Still Fail

### Check These in Order:

1. **Database File Exists?**
   - Look for: `MVP dataset found at ...` in logs
   - If not: Check if `diabetes.csv` is in the repo

2. **CORS Working?**
   - Check browser console - should NOT see CORS errors
   - Backend logs should show CORS origins

3. **LLM API Working?**
   - Check if `OPENAI_API_KEY` is set correctly
   - Check if model name is correct (`gpt-5-nano-2025-08-07` or whatever you're using)

4. **SQL Generation?**
   - Logs will show the generated SQL
   - If invalid, fallback should kick in

5. **SQL Execution?**
   - Logs will show execution errors
   - Fallback query should work if table exists

## Expected Behavior

### Success Case:
1. User asks: "show me the data"
2. LLM generates: `SELECT * FROM diabetes LIMIT 10`
3. SQL executes successfully
4. Results returned with visualization and analysis
5. ✅ User sees data!

### Fallback Case:
1. User asks: "what features do we have?"
2. LLM generates invalid SQL: `SELECT feature FROM (VALUES ...)`
3. Validation catches it
4. Fallback generates: `SELECT * FROM diabetes LIMIT 10`
5. ✅ User sees data (even if not exactly what they asked for)

### Failure Case (Should Be Rare):
1. Database doesn't exist → 404 error (clear message)
2. LLM API fails → 500 error (check API key)
3. Table doesn't exist → 404 error (check import)

## Next Steps

1. **Deploy these changes**
2. **Test with simplest query first**: "show me 10 rows"
3. **Check logs** to see what's happening
4. **Gradually try more complex queries**

The fallback system ensures you'll get SOME response even if the LLM struggles. This should get you your first successful query!

