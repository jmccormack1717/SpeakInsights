"""Script to import CSV into the hardcoded MVP dataset"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import db_manager
from app.utils.csv_importer import CSVImporter
from sqlalchemy import text


async def import_mvp_dataset(csv_path: str, table_name: str = None):
    """
    Import a CSV file into the MVP dataset
    
    Args:
        csv_path: Path to CSV file
        table_name: Optional table name (defaults to filename)
    """
    user_id = "default_user"
    dataset_id = "mvp_dataset"
    
    # Create database if it doesn't exist
    await db_manager.create_database(user_id, dataset_id)
    engine = await db_manager.get_engine(user_id, dataset_id)
    
    # Read CSV file
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return
    
    with open(csv_file, 'rb') as f:
        csv_content = f.read()
    
    # Import CSV
    try:
        result = await CSVImporter.import_csv(
            engine,
            csv_content,
            table_name=table_name or csv_file.stem,
            encoding='utf-8'
        )
        
        print(f"✅ Successfully imported dataset!")
        print(f"   Table: {result['table_name']}")
        print(f"   Rows: {result['rows_imported']}")
        print(f"   Columns: {result['column_count']}")
        print(f"   Location: {db_manager.get_database_path(user_id, dataset_id)}")
    except Exception as e:
        print(f"❌ Error importing CSV: {e}")
    
    await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_mvp_dataset.py <path_to_csv> [table_name]")
        print("\nExample:")
        print("  python import_mvp_dataset.py ../data/diamonds.csv")
        print("  python import_mvp_dataset.py ../data/sales.csv sales_data")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    table_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    asyncio.run(import_mvp_dataset(csv_path, table_name))

