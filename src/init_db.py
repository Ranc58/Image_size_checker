import bson

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult, InsertManyResult


class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient('localhost', 27017)['image_db']['image_collection']

    async def insert_one(self, document: dict) -> InsertOneResult:
        result = await self.client.insert_one(document)
        return result.inserted_id

    async def insert_many(self, data) -> InsertManyResult:
        result = await self.client.insert_many(data)
        return result.inserted_ids

    async def find_by_id(self, id):
        try:
            result = await self.client.find_one({"_id": ObjectId(id)})
        except bson.errors.InvalidId:
            return
        return result


async def setup_db() -> MongoClient:
    mongo_client = MongoClient()
    return mongo_client
