from pydantic import BaseModel, ValidationError
from typing import Literal, Optional
import json

from app.roshid.exceptions import RoshidAttributeError


class Attribute(BaseModel):
    '''Attributes are entities that will be extracted from the text sent to the LLM. Datatypes and Descriptions are there to help the LLM perform better.'''
    attribute_name: str
    datatype: Literal['string', 'number', 'boolean']  # Restrict to specific values
    description: Optional[str] = None  # Description is optional



class CustomerConfig:
    def __init__(self) -> None:
        self.attributes: set[Attribute] = []
        self.attributes.append(Attribute(attribute_name="Name", datatype="string", description="Name of the customer"))
        self.attributes.append(Attribute(attribute_name="Address", datatype="string", description="The delivery address mentioned by the customer"))
        self.attributes.append(Attribute(attribute_name="Phone", datatype="string", description="Phone number mentioned by the customer in the format: '01X XXXX XXXX'"))

    def generate_description(self) -> str:
        attribute_descriptions = [
            f"{attr.attribute_name} ({attr.datatype}): {attr.description or 'No description provided'}"
            for attr in self.attributes
        ]
        return f"Extract {', '.join(attribute_descriptions)} from the text:"
    
    def add_attribute(self, name:str, datatype: str, description: str):
        '''
        attribute_name: str = Name of the attribute (e.g 'Email', 'Secondary Contact')\n\n
        datatype: str ='string', 'number' or 'boolean'\n\n
        description: str = Description of the attribute for the LLM to accurately locate and extract the attribute
        '''
        try:
            if name.lower() in [attr.attribute_name.lower() for attr in self.attributes]: # checks if the attribute name already exists
                raise RoshidAttributeError("Attribute name already exists. Choose a different name.")
            else:
                self.attributes.append(Attribute(attribute_name=name, datatype=datatype, description=description))

        except ValidationError as e:
            print("Something went wrong when creating Attrbute.")
            print(e)

    def expected_json(self) -> str:
        """
        Returns a JSON schema that defines the structure of the expected output from the LLM.
        """
        schema = {"reciepient_info": {}}

        for attr in self.attributes:
            schema["reciepient_info"][attr.attribute_name] = ""

        return json.dumps(schema)