import os
import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_task: BackgroundTasks):
    # Получаем абсолютный путь до папки
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к текущему файлу
    images_dir = os.path.join(base_dir, "../static/images")

    image_path = os.path.join(images_dir, file.filename)

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    # resize_image.delay(image_path)
    background_task.add_task(resize_image, image_path)
