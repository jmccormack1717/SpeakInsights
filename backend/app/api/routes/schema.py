"""Schema API routes"""
from fastapi import APIRouter, HTTPException
from app.core.database import db_manager


router = APIRouter()


@router.get("/datasets/{user_id}/{dataset_id}/schema")
async def get_schema(user_id: str, dataset_id: str):
    """Get database schema information"""
    try:
        schema_info = await db_manager.get_schema(user_id, dataset_id)
        
        if not schema_info.get("tables"):
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_id}' not found or has no tables"
            )
        
        return schema_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get schema: {str(e)}"
        )

