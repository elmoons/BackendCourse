import os
import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_task: BackgroundTasks):
    ImageService().upload_image(file, background_task)
