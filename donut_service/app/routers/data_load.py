import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse
from ..services.images import ImagesService
from ..db.mongo import get_db

router = APIRouter(
    prefix='/dataset',
    tags=['dataset'],
    responses={404: {'description': 'Not found'}},
)

imagesService = ImagesService()


@router.put('/images', summary='Upload images', description='Saves images to the database')
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        saved_id = imagesService.save_images(files)
        return JSONResponse(content=saved_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.put('/labels', summary='Upload json labels', description='Saves labels to the database')
async def upload_labels(files: List[UploadFile] = File(...)):
    pass

@router.get()
async def get_images_status():
    pass

@router.get()
async def get_labels_status():
    pass