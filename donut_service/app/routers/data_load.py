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
    db = get_db()
    try:
        for file in files:
            db.images.insert_one({
                "filename": file.filename,
                "content_type": file.content_type
                # you could also store the actual image file if needed
            })
        return {"message": f"{len(files)} files uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/labels', summary='Upload json labels', description='Saves labels to the database')
async def upload_labels(files: List[UploadFile] = File(...)):
    db = get_db()
    try:
        for file in files:
            db.labels.insert_one({
                "filename": file.filename,
                "content_type": file.content_type
                # you could also store the actual image file if needed
            })
        return {"message": f"{len(files)} files uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get()
async def get_images_status():
    db = get_db()
    images = list(db.images.find({}, {"_id": 0}))  # exclude Mongo’s _id field
    return {
        "count": len(images),
        "images": images
    }

@router.get()
async def get_labels_status():
    pass