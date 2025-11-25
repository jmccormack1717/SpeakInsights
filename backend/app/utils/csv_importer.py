"""CSV import utility for creating tables and inserting data"""
import pandas as pd
from typing import Dict, Any, Optional
from sqlalchemy import text
from pathlib import Path
import io
import asyncio


class CSVImporter:
    """Utility for importing CSV files into SQLite databases"""
    
    @staticmethod
    def sanitize_table_name(name: str) -> str:
        """Sanitize table name for SQLite"""
        # Remove special characters, replace spaces with underscores
        sanitized = "".join(c if c.isalnum() or c == '_' else '_' for c in name)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        # Ensure it starts with a letter or underscore
        if sanitized and not (sanitized[0].isalpha() or sanitized[0] == '_'):
            sanitized = '_' + sanitized
        return sanitized or 'table'
    
    @staticmethod
    def sanitize_column_name(name: str) -> str:
        """Sanitize column name for SQLite"""
        # Similar to table name sanitization
        sanitized = name.strip().replace(' ', '_').replace('-', '_')
        sanitized = "".join(c if c.isalnum() or c == '_' else '_' for c in sanitized)
        sanitized = sanitized.strip('_')
        if sanitized and not (sanitized[0].isalpha() or sanitized[0] == '_'):
            sanitized = '_' + sanitized
        return sanitized or 'column'
    
    @staticmethod
    def infer_sqlite_type(series: pd.Series) -> str:
        """Infer SQLite type from pandas Series"""
        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'DATE'
        
        # Check for numeric types
        if pd.api.types.is_integer_dtype(series):
            return 'INTEGER'
        if pd.api.types.is_float_dtype(series):
            return 'REAL'
        
        # Check if string looks like a date
        if pd.api.types.is_object_dtype(series):
            sample = series.dropna().head(10)
            if len(sample) > 0:
                try:
                    pd.to_datetime(sample, errors='raise')
                    return 'DATE'
                except:
                    pass
        
        # Default to TEXT
        return 'TEXT'
    
    @staticmethod
    async def import_csv(
        engine,
        csv_content: bytes,
        table_name: Optional[str] = None,
        encoding: str = 'utf-8',
        delimiter: str = ','
    ) -> Dict[str, Any]:
        """
        Import CSV file into SQLite database
        
        Args:
            engine: SQLAlchemy async engine
            csv_content: CSV file content as bytes
            table_name: Optional table name (defaults to filename)
            encoding: File encoding
            delimiter: CSV delimiter
            
        Returns:
            Dict with import results
        """
        try:
            # Run pandas operations in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            def read_csv():
                csv_string = csv_content.decode(encoding)
                return pd.read_csv(io.StringIO(csv_string), delimiter=delimiter)
            
            # Read CSV into pandas DataFrame (non-blocking)
            df = await loop.run_in_executor(None, read_csv)
            
            if df.empty:
                raise ValueError("CSV file is empty")
            
            # Sanitize column names
            df.columns = [CSVImporter.sanitize_column_name(col) for col in df.columns]
            
            # Determine table name
            if not table_name:
                table_name = 'imported_data'
            table_name = CSVImporter.sanitize_table_name(table_name)
            
            # Infer column types
            column_defs = []
            for col in df.columns:
                sql_type = CSVImporter.infer_sqlite_type(df[col])
                column_defs.append(f"{col} {sql_type}")
            
            # Create table
            create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(column_defs)}
                )
            """
            
            async with engine.begin() as conn:
                # Drop existing table if it exists (for re-import)
                await conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                
                # Create new table
                await conn.execute(text(create_table_sql))
                
                # Insert data
                # Convert DataFrame to list of dicts for insertion
                rows_inserted = 0
                for _, row in df.iterrows():
                    # Prepare values, handling NaN as NULL
                    values = []
                    placeholders = []
                    for col in df.columns:
                        placeholders.append('?')
                        val = row[col]
                        if pd.isna(val):
                            values.append(None)
                        else:
                            # Convert datetime to string if needed
                            if pd.api.types.is_datetime64_any_dtype(df[col]):
                                values.append(val.strftime('%Y-%m-%d'))
                            else:
                                values.append(val)
                    
                    insert_sql = f"""
                        INSERT INTO {table_name} ({', '.join(df.columns)})
                        VALUES ({', '.join(placeholders)})
                    """
                    await conn.execute(text(insert_sql), tuple(values))
                    rows_inserted += 1
                
                return {
                    "success": True,
                    "table_name": table_name,
                    "rows_imported": rows_inserted,
                    "columns": list(df.columns),
                    "column_count": len(df.columns)
                }
        
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or invalid")
        except Exception as e:
            raise Exception(f"Failed to import CSV: {str(e)}")

