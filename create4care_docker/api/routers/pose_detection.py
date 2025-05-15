import os
import tempfile
import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import cv2

from utils.pose_decection import PoseDetector

router = APIRouter()
detector = PoseDetector()

class PostureRequest(BaseModel):
    image_base64: str

class PostureResponse(BaseModel):
    issues: Optional[List[str]] = None
    landmark_image: Optional[str] = None

@router.post("/detect_posture", response_model=PostureResponse)
async def detect_posture(req: PostureRequest):
    # 1. Decode base64 image
    try:
        header, encoded = req.image_base64.split(",", 1)
        img_data = base64.b64decode(encoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image format")

    # 2. Write to a temporary file for PoseDetector
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(img_data)
        tmp_path = tmp.name

    # 3. Run posture evaluation
    try:
        result = detector.evaluate_image(tmp_path)
    finally:
        os.unlink(tmp_path)

    # 4a. Return issues if found
    if "issues" in result:
        return PostureResponse(issues=result["issues"])

    # 4b. No issues: encode overlay and save via image_utils
    success, buffer = cv2.imencode(".png", result["landmark_image"])
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode landmark image")

    b64_img = base64.b64encode(buffer).decode("utf-8")
    data_url = f"data:image/png;base64,{b64_img}"

    return PostureResponse(landmark_image=data_url)
