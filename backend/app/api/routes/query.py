"""Query API routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.query_service import QueryService
from app.services.data_analysis_service import DataAnalysisService
from app.services.viz_service import VisualizationService
from app.services.analysis_service import AnalysisService
from app.core.database import db_manager


router = APIRouter()

query_service = QueryService()
data_analysis_service = DataAnalysisService()
viz_service = VisualizationService()
analysis_service = AnalysisService()


class QueryRequest(BaseModel):
    """Query request model"""
    user_id: str
    dataset_id: str
    query: str


class QueryResponse(BaseModel):
    """Query response model"""
    sql: str
    results: List[Dict[str, Any]]
    visualization: Dict[str, Any]
    analysis: Dict[str, Any]
    data_structure: Dict[str, Any]


@router.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """
    Execute a natural language query
    
    Flow:
    1. Get schema context
    2. Generate SQL from natural language
    3. Execute SQL query
    4. Analyze data structure
    5. Select visualization
    6. Generate textual analysis
    """
    try:
        # Step 1: Get schema
        schema_info = await db_manager.get_schema(
            request.user_id,
            request.dataset_id
        )
        
        if not schema_info.get("tables"):
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{request.dataset_id}' not found or has no tables"
            )
        
        # Step 2: Generate SQL
        sql_result = await query_service.generate_sql(
            request.query,
            schema_info
        )
        sql = sql_result["sql"]
        intent = sql_result["intent"]
        
        # Step 3: Execute query
        results = await db_manager.execute_query(
            request.user_id,
            request.dataset_id,
            sql
        )
        
        # Step 4: Analyze data structure
        data_structure = data_analysis_service.analyze_structure(results)
        
        # Step 5: Select visualization
        chart_config = viz_service.select_chart_type(intent, data_structure)
        formatted_data = viz_service.format_data_for_chart(results, chart_config)
        
        visualization = {
            "type": chart_config.get("type"),
            "data": formatted_data,
            "config": chart_config.get("config", {}),
            "metadata": {
                "x_axis": chart_config.get("x_axis"),
                "y_axis": chart_config.get("y_axis"),
                "labels": chart_config.get("labels"),
                "values": chart_config.get("values")
            }
        }
        
        # Step 6: Generate analysis
        textual_analysis = await analysis_service.generate_insights(
            request.query,
            results,
            sql,
            data_structure
        )
        
        return QueryResponse(
            sql=sql,
            results=results,
            visualization=visualization,
            analysis=textual_analysis,
            data_structure=data_structure
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

