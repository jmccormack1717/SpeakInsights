"""Data analysis service: Analyze query result structure"""
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime


class DataAnalysisService:
    """Service for analyzing data structure and statistics"""
    
    @staticmethod
    def infer_column_type(column_name: str, sample_data: List[Any]) -> str:
        """
        Infer column type from sample data
        
        Args:
            column_name: Name of the column
            sample_data: Sample values from the column
            
        Returns:
            Column type: 'numeric', 'categorical', 'datetime', 'text'
        """
        if not sample_data:
            return "text"
        
        # Check for datetime
        datetime_count = 0
        for value in sample_data[:10]:  # Check first 10 values
            if isinstance(value, (datetime, pd.Timestamp)):
                datetime_count += 1
            elif isinstance(value, str):
                # Try to parse as date
                try:
                    pd.to_datetime(value)
                    datetime_count += 1
                except:
                    pass
        
        if datetime_count >= len(sample_data) * 0.8:
            return "datetime"
        
        # Check for numeric
        numeric_count = 0
        for value in sample_data[:10]:
            if isinstance(value, (int, float)) and not pd.isna(value):
                numeric_count += 1
            elif isinstance(value, str):
                try:
                    float(value)
                    numeric_count += 1
                except:
                    pass
        
        if numeric_count >= len(sample_data) * 0.8:
            return "numeric"
        
        # Check cardinality for categorical
        unique_values = len(set(str(v) for v in sample_data if v is not None))
        if unique_values <= 20 and len(sample_data) > unique_values:
            return "categorical"
        
        return "text"
    
    def analyze_structure(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze query result structure
        
        Args:
            results: List of result rows as dictionaries
            
        Returns:
            Data structure analysis
        """
        if not results:
            return {
                "row_count": 0,
                "column_count": 0,
                "columns": {},
                "numeric_columns": [],
                "categorical_columns": [],
                "datetime_columns": [],
                "text_columns": [],
                "has_time_series": False,
                "cardinality": {}
            }
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(results)
        
        analysis = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": {},
            "numeric_columns": [],
            "categorical_columns": [],
            "datetime_columns": [],
            "text_columns": [],
            "has_time_series": False,
            "cardinality": {}
        }
        
        # Analyze each column
        for col in df.columns:
            sample_data = df[col].dropna().head(20).tolist()
            col_type = self.infer_column_type(col, sample_data)
            
            analysis["columns"][col] = {
                "type": col_type,
                # Convert to native bool to avoid numpy.bool_ serialization issues
                "nullable": bool(df[col].isna().any())
            }
            
            # Calculate cardinality
            unique_count = df[col].nunique()
            analysis["cardinality"][col] = unique_count
            
            # Categorize columns
            if col_type == "numeric":
                analysis["numeric_columns"].append(col)
                # Add statistics
                numeric_values = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(numeric_values) > 0:
                    analysis["columns"][col]["statistics"] = {
                        "min": float(numeric_values.min()),
                        "max": float(numeric_values.max()),
                        "mean": float(numeric_values.mean()),
                        "median": float(numeric_values.median())
                    }
            elif col_type == "categorical":
                analysis["categorical_columns"].append(col)
            elif col_type == "datetime":
                analysis["datetime_columns"].append(col)
                # Ensure we store a native Python bool, not numpy.bool_
                analysis["has_time_series"] = True
            else:
                analysis["text_columns"].append(col)
        
        return analysis

