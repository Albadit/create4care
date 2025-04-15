import os
import base64
from datetime import datetime
from fastapi import HTTPException, Request
from core.config import IMAGE_DIR, IMAGES_URL

ALLOWED_MIME = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif"}

def save_image(image_base64: str, patient_id: int, request: Request) -> str:
    try:
        header, encoded = image_base64.split(",", 1)
        mime = header.split(";")[0].split(":")[1]
        ext = ALLOWED_MIME[mime]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image format")

    try:
        image_data = base64.b64decode(encoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Decoding error")

    file_name = f"{patient_id}{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file_path = os.path.join(IMAGE_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(image_data)

    return f"{request.base_url}{IMAGES_URL}/{file_name}"
