from typing import Dict, List

import bson

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult, InsertManyResult


class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient(
            'localhost', 27017
        )['image_db']['image_collection']

    async def insert_one(self,
                         document: Dict[str, List[Dict]]
                         ) -> InsertOneResult:
        result = await self.client.insert_one(document)
        return result.inserted_id

    async def find_by_id(self, obj_id: str) -> Dict or None:
        try:
            result = await self.client.find_one(
                {"_id": ObjectId(obj_id)}
            )
        except bson.errors.InvalidId:
            return
        return result


async def setup_db() -> MongoClient:
    mongo_client = MongoClient()
    return mongo_client
