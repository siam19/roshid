from fastapi import APIRouter, Depends, HTTPException, Header, Request
from typing import Dict
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from utils.uuid import simple_uuid
from utils.exceptions import RoshidError
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import APIRouter, Depends, HTTPException, Header

from routers.stores import get_stores_dal, StoresDAL

class BlockContent(BaseModel):
    pass

class TextContent(BlockContent):
    text: str
    style: Optional[str]

class LinkContent(BlockContent):
    text: str
    url: str
    style: Optional[str]



class Block(BaseModel):
    
    index: int
    type: str
    content: Dict



class Page(BaseModel):
    title: str
    visibility: bool 
    blocks: List[Block]



class PagesDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_page(self, page: Page, store_id: str) -> str:
        page_id = simple_uuid(12)
        page_data = page.model_dump()
        for block in page_data.get("blocks"):
            block["id"] = simple_uuid(4)
        page_data["_id"] = page_id
        page_data["store_id"] = store_id
        page_data["created_at"] = datetime.now()
        
        try:
            await self.collection.insert_one(page_data)
            return page_id
        except Exception as e:
            raise RoshidError(f"Failed to create page: {str(e)}")

    async def update_page(self, page_id: str, page_data: dict) -> bool:
        try:
            result = await self.collection.update_one(
                {"_id": page_id},
                {"$set": {
                    **page_data,
                    "updated_at": datetime.now(datetime.utc)
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            raise RoshidError(f"Failed to update page: {str(e)}")

    async def get_page_content(self, page_id: str) -> dict:
        try:
            page = await self.collection.find_one({"_id": page_id})
            if not page:
                raise HTTPException(status_code=404, detail="Page not found")
            return page
        except Exception as e:
            raise RoshidError(f"Failed to get page: {str(e)}")
        
    async def add_block(self, page_id: str, block: Block) -> bool:
        try:
            page = await self.collection.find_one({"_id": page_id}, {"blocks": 1})
            if not page:
                raise HTTPException(status_code=404, detail="Page not found")

            # Check for duplicate index
            if any(b.get("index") == block.index for b in page.get("blocks", [])):
                raise HTTPException(status_code=400, detail=f"Block index {block.index} is already used")

            new_block = block.model_dump()
            new_block["id"] = simple_uuid(4)
            result = await self.collection.update_one(
                {"_id": page_id},
                {"$push": {"blocks": new_block}}
            )
            return {"success": result.modified_count > 0, "block_id": new_block["id"]}
        except Exception as e:
            raise RoshidError(f"Failed to add block: {str(e)}")

    async def update_block(self, page_id: str, block_id: str, block_data: dict) -> bool:
        try:
            result = await self.collection.update_one(
                {"_id": page_id, "blocks.id": block_id},
                {"$set": {
                    "blocks.$": block_data
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            raise RoshidError(f"Failed to update block: {str(e)}")
        
    async def delete_block(self, page_id: str, block_id: str) -> bool:
        try:
            # Find the page and its blocks
            page = await self.collection.find_one({"_id": page_id}, {"blocks": 1})
            if not page:
                raise HTTPException(status_code=404, detail="Page not found")

            # Remove the block with the specified block_id
            blocks = [block for block in page["blocks"] if block["id"] != block_id]
            if len(blocks) == len(page["blocks"]):
                raise HTTPException(status_code=404, detail="Block not found")

            # Re-index the remaining blocks
            for i, block in enumerate(blocks):
                block["index"] = i

            # Update the page with the new blocks
            result = await self.collection.update_one(
                {"_id": page_id},
                {"$set": {"blocks": blocks}}
            )
            return result.modified_count > 0
        except Exception as e:
            raise RoshidError(f"Failed to delete block: {str(e)}")

router = APIRouter()

def get_pages_dal(request: Request):
    return request.app.pages_dal


@router.post("/page/create")
async def create_page(
    page_data: Page,
    store_id: str = Header(...),
    pages_dal: PagesDAL = Depends(get_pages_dal),
    store_dal: StoresDAL = Depends(get_stores_dal)
):
    
    # check store collection for store_id
    
    store = await store_dal.get_store(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    else:
        page_id = await pages_dal.create_page(page_data, store_id)
        
        await store_dal.add_page(store_id, page_id)
        
        return {"page_id": page_id,
                "store_id": store_id}


@router.get("/page/{page_id}")
async def get_page(
    page_id: str,
    pages_dal: PagesDAL = Depends(get_pages_dal)
):
    try:
        page = await pages_dal.get_page_content(page_id)
        return page
    except RoshidError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/page/blocks/add")
async def add_block(
    page_id: str,
    block_data: Block,
    pages_dal: PagesDAL = Depends(get_pages_dal)
):
    try:
        success = await pages_dal.add_block(page_id, block_data)
        return {"success": success}
    except RoshidError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/page/blocks/update")
async def update_block(
    page_id: str,
    block_id: str,
    block_data: dict,
    pages_dal: PagesDAL = Depends(get_pages_dal)
):
    try:
        success = await pages_dal.update_block(page_id, block_id, block_data)
        return {"success": success}
    except RoshidError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/page/blocks/delete")
async def delete_block(
    page_id: str,
    block_id: str,
    pages_dal: PagesDAL = Depends(get_pages_dal)
):
    try:
        success = await pages_dal.delete_block(page_id, block_id)
        return {"success": success}
    except RoshidError as e:
        raise HTTPException(status_code=500, detail=str(e))