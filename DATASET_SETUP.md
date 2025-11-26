# Demo Dataset Setup (PIMA Diabetes)

This project ships with a **cleaned PIMA diabetes dataset** as the default demo, and also supports uploading additional CSVs via the UI.

## Where the Demo Dataset Lives

On first backend startup, if no database is found for the default user/dataset, the app will:

1. Look for a CSV named `cleaned_diabetes_dataset.csv` in any of these locations:
   - `backend/cleaned_diabetes_dataset.csv`
   - `cleaned_diabetes_dataset.csv` (project root)
   - `backend/data/cleaned_diabetes_dataset.csv`
2. Import it into a SQLite database at:
   ```
   backend/data/default_user/mvp_dataset.db
   ```

In the UI this appears as **“PIMA Diabetes Dataset”** and is selected by default.

## Using Your Own Data Instead (Local Development)

You don’t need to pre-create a SQLite database any more—just:

1. Start backend and frontend.
2. In the app, go to the **Dataset** section.
3. Use the **“Import your own CSV”** card to upload a file.
4. The backend will create `backend/data/{user_id}/{dataset_id}.db` and import your CSV automatically.

For this demo (especially on free Render hosting), datasets up to about **50MB / ~100k rows** are recommended for good responsiveness.

## Notes for Deployment (Render)

- The demo SQLite DB for PIMA diabetes will be placed at `backend/data/default_user/mvp_dataset.db` on the server.
- Render’s filesystem is ephemeral, so for long-lived custom datasets you would normally:
  - Include small demo DBs in the repo **or**
  - Recreate/import data on each deploy via a script **or**
  - Attach a persistent disk (paid feature)

For portfolio/demo purposes, relying on auto-import of the diabetes CSV and ad‑hoc CSV uploads is usually sufficient.
