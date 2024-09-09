from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.roshid.llm import LLM
from app.roshid.classes import CustomerConfig
from PIL import Image
import pytesseract

import io

# from app.roshid.ocr import 

router = APIRouter()

@router.post("/upload/")
async def upload(file: UploadFile = File(...)):
    customer = CustomerConfig()

    try:
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
        scanned_text = pytesseract.image_to_string(img)
        llm = LLM("groq")
        return f"{llm.extract(scanned_text, customer_config=customer)}"
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)