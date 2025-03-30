import logging
import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
import tempfile
import zipfile
from fastapi.responses import JSONResponse,FileResponse
from ..services.images import ImagesService
from ..repository.mongodb.images import ImageRepository
from fastapi.background import BackgroundTasks

router = APIRouter(
    prefix='/dataset',
    tags=['dataset'],
    responses={404: {'description': 'Not found'}},
)

# Dependency function for ImageRepository
def get_image_repository() -> ImageRepository:
    return ImageRepository()

# Dependency function for ImagesService
def get_images_service(image_repository: ImageRepository = Depends(get_image_repository)) -> ImagesService:
    return ImagesService(image_repository=image_repository)


@router.put('/images', summary='Upload images', description='Saves images to the dataset')
async def upload_images(
    files: List[UploadFile] = File(...),
    images_service: ImagesService = Depends(get_images_service)
):
    try:
        saved_image_ids = images_service.save_images(files)
        return {"message": f"{len(files)} files uploaded", "image_ids": saved_image_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/images', summary='Download images', description='Downloads info about all images from the dataset')
async def download_images_metadata(
    images_service: ImagesService = Depends(get_images_service)
):
    try:
        # Retrieve all images from the service
        images = images_service.get_all_images()

        # Prepare the response
        response_data = [
            {
                "image_name": image.image_name,
                "metadata": image.metadata
            }
            for image in images
        ]

        return {"count": len(response_data), "images": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/images/download', summary='Download all images', description='Downloads all images as a ZIP file')
async def download_all_images(
    background_tasks: BackgroundTasks,
    images_service: ImagesService = Depends(get_images_service)
    ):
    """
    Endpoint to download all images as a ZIP file.
    """
    try:
        # Retrieve all images from the service
        images = images_service.get_all_images()

        # Create a temporary ZIP file
        temp_zip_path = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name
        with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
            for image in images:
                zipf.writestr(image.image_name, image.image_data)
                
        # Schedule the cleanup of the temporary file    
        background_tasks.add_task(os.remove, temp_zip_path)

        # Return the ZIP file as a response
        return FileResponse(
            temp_zip_path,
            media_type="application/zip",
            filename="images_dataset.zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
