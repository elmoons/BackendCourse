import os
import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, background_task: BackgroundTasks):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "../static/images")

        image_path = os.path.join(images_dir, file.filename)

        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # resize_image.delay(image_path)
        background_task.add_task(resize_image, image_path)
