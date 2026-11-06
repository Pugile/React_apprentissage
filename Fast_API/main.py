from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReturnDocument
import jwt
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

app = FastAPI()
security = HTTPBearer()
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["React"]
users_collection = db["User"]
class UserSchema(BaseModel):
    username: str
    roles: List[str]

async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
  token = credentials.credentials
  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return payload
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expiré")
  except jwt.PyJWTError:
    raise HTTPException(status_code=401, detail="Token invalide")

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
async def sync_user(
    user: UserSchema,
    current_token_payload: dict = Depends(verify_jwt),
):
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