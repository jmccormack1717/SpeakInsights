# Hardcoded Dataset Setup for MVP

## Where to Put Your Dataset

Place your SQLite database file at:

```
backend/data/default_user/mvp_dataset.db
```

## Steps to Add Your Dataset

### Option 1: Create from CSV (Recommended)

1. **Place your CSV file** at: `backend/data/your_data.csv`

2. **Run the import script** (create this script):
   ```bash
   cd backend
   python scripts/import_mvp_dataset.py
   ```

3. **Or manually import using SQLite:**
   ```bash
   sqlite3 data/default_user/mvp_dataset.db
   ```
   Then create tables and import your data.

### Option 2: Copy Existing Database

1. **Create the directory** (if it doesn't exist):
   ```bash
   mkdir -p backend/data/default_user
   ```

2. **Copy your database file** to:
   ```
   backend/data/default_user/mvp_dataset.db
   ```

### Option 3: Use SQLite GUI Tool

1. Open `backend/data/default_user/mvp_dataset.db` in DB Browser for SQLite
2. Import your CSV or create tables manually
3. Save the database

## Important Notes

- **File name must be**: `mvp_dataset.db`
- **Location must be**: `backend/data/default_user/`
- **User ID**: `default_user` (hardcoded in frontend)
- **Dataset ID**: `mvp_dataset` (hardcoded in frontend)

## After Adding Your Dataset

1. The dataset will automatically be selected when the app loads
2. Users can immediately start querying it
3. No need to create/upload - it's already there!

## For Deployment

On Render, the database file will be in the same location:
- `backend/data/default_user/mvp_dataset.db`

**Note**: Render's filesystem is ephemeral, so you'll need to:
- Either include the database file in your git repo (if small)
- Or recreate it on each deploy using a script
- Or use Render Disk for persistence (paid feature)

