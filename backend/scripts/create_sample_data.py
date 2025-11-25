"""Script to create sample data for testing"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import db_manager
from sqlalchemy import text


async def create_sample_database():
    """Create a sample sales database with data"""
    user_id = "default_user"
    dataset_id = "sales_data"
    
    # Create database
    await db_manager.create_database(user_id, dataset_id)
    engine = await db_manager.get_engine(user_id, dataset_id)
    
    async with engine.begin() as conn:
        # Create sales table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                quarter TEXT NOT NULL,
                date DATE NOT NULL,
                salesperson TEXT
            )
        """))
        
        # Insert sample data
        sample_data = [
            ('North', 'Product A', 50000, 'Q4', '2024-10-01', 'Alice'),
            ('North', 'Product B', 45000, 'Q4', '2024-10-15', 'Alice'),
            ('South', 'Product A', 42000, 'Q4', '2024-10-05', 'Bob'),
            ('South', 'Product C', 38000, 'Q4', '2024-10-20', 'Bob'),
            ('East', 'Product B', 60000, 'Q4', '2024-11-01', 'Charlie'),
            ('East', 'Product A', 55000, 'Q4', '2024-11-10', 'Charlie'),
            ('West', 'Product C', 48000, 'Q4', '2024-11-05', 'Diana'),
            ('West', 'Product B', 52000, 'Q4', '2024-11-15', 'Diana'),
            ('North', 'Product A', 47000, 'Q3', '2024-07-10', 'Alice'),
            ('South', 'Product A', 40000, 'Q3', '2024-08-15', 'Bob'),
            ('East', 'Product B', 58000, 'Q3', '2024-09-01', 'Charlie'),
            ('West', 'Product C', 45000, 'Q3', '2024-09-20', 'Diana'),
        ]
        
        for data in sample_data:
            await conn.execute(text("""
                INSERT INTO sales (region, product, amount, quarter, date, salesperson)
                VALUES (?, ?, ?, ?, ?, ?)
            """), data)
        
        print(f"✅ Created sample database: {dataset_id}")
        print(f"   Location: {db_manager.get_database_path(user_id, dataset_id)}")
        print(f"   Inserted {len(sample_data)} rows")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_sample_database())

