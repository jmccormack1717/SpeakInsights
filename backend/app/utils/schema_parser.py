"""Schema parsing and context building utilities"""
from typing import Dict, Any, List


def build_schema_context(schema_info: Dict[str, Any]) -> str:
    """
    Build a human-readable schema context for LLM prompts
    
    Args:
        schema_info: Schema information from database
        
    Returns:
        Formatted schema context string
    """
    context_parts = []
    
    for table in schema_info.get("tables", []):
        table_name = table["name"]
        columns = table.get("columns", [])
        sample_rows = table.get("sample_rows", [])
        
        context_parts.append(f"\nTable: {table_name}")
        context_parts.append("Columns:")
        
        for col in columns:
            col_type = col.get("type", "unknown")
            nullable = "NULL" if col.get("nullable") else "NOT NULL"
            context_parts.append(f"  - {col['name']} ({col_type}) {nullable}")
        
        if sample_rows:
            context_parts.append("\nSample data (first 3 rows):")
            for i, row in enumerate(sample_rows[:3], 1):
                context_parts.append(f"  Row {i}: {row}")
    
    return "\n".join(context_parts)


def get_table_names(schema_info: Dict[str, Any]) -> List[str]:
    """Extract list of table names from schema"""
    return [table["name"] for table in schema_info.get("tables", [])]

