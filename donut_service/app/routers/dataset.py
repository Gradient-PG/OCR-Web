import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Body
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse,FileResponse
from typing import List
import tempfile
import zipfile
from ..services.image import ImageService
from ..repository.mongodb.image import ImageRepository
from ..model.label import LabelRequest
from ..services.label import LabelService
from ..repository.mongodb.label import LabelRepository

router = APIRouter(
    prefix='/dataset',
    tags=['dataset'],
    responses={404: {'description': 'Not found'}},
)

# Dependency function for ImageRepository
def get_image_repository() -> ImageRepository:
    return ImageRepository()

# Dependency function for ImageService
def get_image_service(image_repository: ImageRepository = Depends(get_image_repository)) -> ImageRepository:
    return ImageService(image_repository=image_repository)

def get_label_repository() -> LabelRepository:
    return LabelRepository()

def get_label_service(label_repository: LabelRepository = Depends(get_label_repository)) -> LabelService:
    return LabelService(label_repository=label_repository)



@router.put('/images', summary='Upload images', description='Saves images to the dataset')
async def upload_images(
    files: List[UploadFile] = File(...),
    image_service: ImageService = Depends(get_image_service)
):
    try:
        saved_image_ids = image_service.save_images(files)
        return {"message": f"{len(files)} files uploaded", "image_ids": saved_image_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/images', summary='Download images', description='Downloads info about all images from the dataset')
async def download_image_metadata(
    image_service: ImageService = Depends(get_image_service)
):
    try:
        # Retrieve all images from the service
        images = image_service.get_all_images()

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
    image_service: ImageService = Depends(get_image_service)
    ):
    """
    Endpoint to download all images as a ZIP file.
    """
    try:
        # Retrieve all images from the service
        images = image_service.get_all_images()

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
    
@router.put('/label', summary='Upload labels', description='Uploads labels for the images')
async def upload_label(
    request: LabelRequest = Body(...),
    label_service: LabelService = Depends(get_label_service)
):
    """
    Endpoint to upload labels for the images.
    """
    try:
        # Convert the request object to a LabelEntity
        label_entity = label_service.create_label_entity(request)

        # Save the label using the service
        label_service.save_label(label_entity)

        return {"message": "Label uploaded successfully", "image_code": label_entity.image_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put('/labels', summary='Upload multiple labels', description='Uploads multiple labels for the images')
async def upload_labels(
    requests: List[LabelRequest] = Body(...),
    label_service: LabelService = Depends(get_label_service)
):
    """
    Endpoint to upload multiple labels for the images.
    """
    try:
        # Convert each request object to a LabelEntity and save it
        for request in requests:
            label_entity = label_service.create_label_entity(request)
            label_service.save_label(label_entity)

        return {"message": f"{len(requests)} labels uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/labels', summary='Download labels', description='Downloads all labels from the dataset')
async def download_labels(
    label_service: LabelService = Depends(get_label_service)
):
    """
    Endpoint to download all labels from the dataset.
    """
    try:
        # Retrieve all labels from the service
        labels = label_service.get_labels()
        
        return {"count": len(labels), "labels": labels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
