import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse
from ..services.images import ImagesService

router = APIRouter(
    prefix='/dataset',
    tags=['dataset'],
    responses={404: {'description': 'Not found'}},
)

imagesService = ImagesService()

@router.post('/images', summary='Upload images', description='Saves images to the database')
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        result = imagesService.save_images(files)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
