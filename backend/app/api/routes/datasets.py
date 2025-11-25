"""Dataset management API routes"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import db_manager
from app.utils.csv_importer import CSVImporter


router = APIRouter()


class DatasetCreate(BaseModel):
    """Dataset creation model"""
    user_id: str
    dataset_id: str
    name: str
    description: Optional[str] = None


class DatasetResponse(BaseModel):
    """Dataset response model"""
    user_id: str
    dataset_id: str
    name: str
    description: Optional[str] = None
    created: bool


@router.post("/datasets", response_model=DatasetResponse)
async def create_dataset(dataset: DatasetCreate):
    """Create a new dataset (database)"""
    try:
        await db_manager.create_database(
            dataset.user_id,
            dataset.dataset_id
        )
        
        return DatasetResponse(
            user_id=dataset.user_id,
            dataset_id=dataset.dataset_id,
            name=dataset.name,
            description=dataset.description,
            created=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create dataset: {str(e)}"
        )


@router.get("/datasets/{user_id}")
async def list_datasets(user_id: str):
    """List all datasets for a user"""
    # In Phase 1, we'll just return a simple list
    # In Phase 2, this would query a metadata database
    import os
    from pathlib import Path
    
    user_dir = Path(db_manager.data_path) / user_id
    if not user_dir.exists():
        return []
    
    datasets = []
    for db_file in user_dir.glob("*.db"):
        datasets.append({
            "dataset_id": db_file.stem,
            "name": db_file.stem,
            "created_at": db_file.stat().st_mtime
        })
    
    return datasets


@router.post("/datasets/{user_id}/{dataset_id}/upload")
async def upload_csv(
    user_id: str,
    dataset_id: str,
    file: UploadFile = File(...),
    table_name: Optional[str] = Form(None)
):
    """
    Upload CSV file to a dataset
    
    Creates or replaces a table in the dataset with the CSV data
    """
    try:
        # Ensure dataset exists
        await db_manager.create_database(user_id, dataset_id)
        engine = await db_manager.get_engine(user_id, dataset_id)
        
        # Read file content
        contents = await file.read()
        
        # Import CSV
        result = await CSVImporter.import_csv(
            engine,
            contents,
            table_name=table_name or file.filename.replace('.csv', '').replace('.CSV', ''),
            encoding='utf-8'
        )
        
        return {
            "success": True,
            "message": f"Successfully imported {result['rows_imported']} rows",
            **result
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload CSV: {str(e)}"
        )


@router.delete("/datasets/{user_id}/{dataset_id}")
async def delete_dataset(user_id: str, dataset_id: str):
    """Delete a dataset"""
    try:
        db_path = db_manager.get_database_path(user_id, dataset_id)
        if db_path.exists():
            db_path.unlink()
            return {"deleted": True, "message": f"Dataset '{dataset_id}' deleted"}
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_id}' not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete dataset: {str(e)}"
        )

