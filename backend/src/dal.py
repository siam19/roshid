from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from pydantic import BaseModel, ConfigDict
from typing import List, AsyncGenerator,Optional

from utils.uuid import simple_uuid

from classes import Product, ProductVariant

class ProductResponse(Product):
    product_id: Optional[str] 
    


#DAL stands for Data Access Layer. The DAL is responsible for handling all interactions with the database.

# class ToDoDAL:
#   def __init__(self, todo_collection: AsyncIOMotorCollection):
#       self._todo_collection = todo_collection

#   async def list_todo_lists(self, session=None):
#       async for doc in self._todo_collection.find(
#           {},
#           projection={
#               "name": 1,
#               "item_count": {"$size": "$items"},
#           },
#           sort={"name": 1},
#           session=session,
#       ):
#           yield ListSummary.from_doc(doc)

#   async def create_todo_list(self, name: str, session=None) -> str:
#       response = await self._todo_collection.insert_one(
#           {"name": name, "items": []},
#           session=session,
#       )
#       return str(response.inserted_id)

#   async def get_todo_list(self, id: str | ObjectId, session=None) -> ToDoList:
#       doc = await self._todo_collection.find_one(
#           {"_id": ObjectId(id)},
#           session=session,
#       )
#       return ToDoList.from_doc(doc)

#   async def delete_todo_list(self, id: str | ObjectId, session=None) -> bool:
#       response = await self._todo_collection.delete_one(
#           {"_id": ObjectId(id)},
#           session=session,
#       )
#       return response.deleted_count == 1

#   async def create_item(
#       self,
#       id: str | ObjectId,
#       label: str,
#       session=None,
#   ) -> ToDoList | None:
#       result = await self._todo_collection.find_one_and_update(
#           {"_id": ObjectId(id)},
#           {
#               "$push": {
#                   "items": {
#                       "id": uuid4().hex,
#                       "label": label,
#                       "checked": False,
#                   }
#               }
#           },
#           session=session,
#           return_document=ReturnDocument.AFTER,
#       )
#       if result:
#           return ToDoList.from_doc(result)

#   async def set_checked_state(
#       self,
#       doc_id: str | ObjectId,
#       item_id: str,
#       checked_state: bool,
#       session=None,
#   ) -> ToDoList | None:
#       result = await self._todo_collection.find_one_and_update(
#           {"_id": ObjectId(doc_id), "items.id": item_id},
#           {"$set": {"items.$.checked": checked_state}},
#           session=session,
#           return_document=ReturnDocument.AFTER,
#       )
#       if result:
#           return ToDoList.from_doc(result)

#   async def delete_item(
#       self,
#       doc_id: str | ObjectId,
#       item_id: str,
#       session=None,
#   ) -> ToDoList | None:
#       result = await self._todo_collection.find_one_and_update(
#           {"_id": ObjectId(doc_id)},
#           {"$pull": {"items": {"id": item_id}}},
#           session=session,
#           return_document=ReturnDocument.AFTER,
#       )
#       if result:
#           return ToDoList.from_doc(result)
class ProductDAL:
    '''
    Acts as a Data Access Layer for the Product collection.
    Attach the ProductDAL to the app instance as app.product_dal.
    '''
    def __init__(self, product_collection: AsyncIOMotorCollection):
       self._product_collection = product_collection
    

    async def list_products(self, session=None)-> AsyncGenerator:
        #yields a generator that returns Product instances.
        # `use [i async for i in app.product_dal.list_products()]

        async for doc in self._product_collection.find({}, session=session):
            yield Product.from_doc(doc)

    async def get_product(self, id: str | ObjectId, session=None) -> Product:
        doc = await self._product_collection.find_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return Product.from_doc(doc)
    
    async def create_product(self, product: Product, session=None) -> str:
        #product.product_id = simple_uuid(4)
        response = await self._product_collection.insert_one(
            product.model_dump(),
            session=session,
        )
        return {"inserted_id": str(response.inserted_id)}
    
    async def delete_product(self, id: str | ObjectId, session=None) -> bool:
        response = await self._product_collection.delete_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return response.deleted_count == 1
    
    
    