from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List

app = FastAPI()
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["React"]
users_collection = db["User"]
class UserSchema(BaseModel):
    username: str
    roles: List[str]

@app.post("/users", status_code=201)
async def create_user(user: UserSchema):
    user_dict = user.model_dump()
    result = await users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "username": user.username}

@app.get("/users/{username}")
async def get_user(username: str):
    user_doc = await users_collection.find_one({"username": username})
    if not user_doc:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc

@app.post("/api/users/sync")
async def sync_user(user: UserSyncSchema):
    now = datetime.now(timezone.utc)
    user_doc = await users_collection.find_one_and_update(
        {"username": user.username},
        {
            "$set": {
                "roles": user.roles,
                "last_login": now
            },
            "$setOnInsert": {
                "created_at": now
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    if not user_doc:
        raise HTTPException(status_code=500, detail="Erreur lors de la synchronisation de l'utilisateur")
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc