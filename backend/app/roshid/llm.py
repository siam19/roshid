from typing import List, Optional
import json
from pydantic import BaseModel
from groq import Groq

from .ocr import get_text
from .classes import CustomerConfig


class LLM:
    GROQ_API_KEY="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"
    #TODO Create an environtment variable you lazy fuck

    def __init__(self, client="groq") -> None:
        if client == "groq":
            self.client = Groq(api_key=LLM.GROQ_API_KEY)
        else:
            #TODO update for openai and local models later
            raise Exception("Only groq-llama-3.1-8b-instant is supported for now.")
        

        
    def extract(self, unstructured_text, customer_config:CustomerConfig):

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





if __name__ == "__main__":
    cust1 = CustomerConfig()
    cust1.add_attribute("Email", "string", "The email of the user")
    cust1.add_attribute("is_purni", "boolean", "Checks if the users name is Purnima or anythis starting with the letter 'P'")
    cust1.add_attribute("is_roy", "boolean", "Checks if the users name is roy")
    cust1.add_attribute("product_count", "number", "Number of products ordered")
    cust1.add_attribute("notes", "string", "If the customer mentions any note about the delivery, otherwise keep it empty.")


    llm = LLM("groq")
    out = llm.extract(get_text("/home/bastok/projects/roshid/0.0/ss6.jpg"), customer_config=cust1)
    print(out)