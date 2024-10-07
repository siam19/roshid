import os
import pytesseract
from groq import Groq
from utils.exceptions import RoshidAPIKeyError
from classes import CustomerConfig
from typing import Annotated
from fastapi import File
from PIL import Image
from io import BytesIO
import json

def get_text(img: Annotated[bytes, File()]):
    image = Image.open(BytesIO(img))
    scanned_text = pytesseract.image_to_string(image)
    return scanned_text

class LLM:
    
    def __init__(self, client="groq") -> None:
        
        
        if client == "groq":
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise RoshidAPIKeyError("LLM / AI service not set up.")
            self.client = Groq(api_key=self.api_key)
    
        else:
            #TODO update for openai and local models later
            raise Exception("Only groq-llama-3.1-8b-instant is supported for now.")
        

        
    def extract_customer_data(self, unstructured_text, customer_config: CustomerConfig,):

        chat_completion = self.client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent data extraction model that outputs extracted data in JSON from unstructured text that is returned from a OCR engine.\n" +
                f"{customer_config.generate_description()}.The JSON object must use the schema: {json.dumps(customer_config.expected_json(), indent=2)}",
            },
            {
                "role": "user",
                "content": f"unstructured text: {unstructured_text}",
            },
        ],
        model="llama-3.1-8b-instant",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"},
    )
        return chat_completion.choices[0].message.content


