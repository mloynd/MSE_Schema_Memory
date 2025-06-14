# main.py – MSE Schema-Aware Memory API

from fastapi import FastAPI, Request
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import os, uuid

app = FastAPI()

# --- MongoDB Setup ---
client = MongoClient(os.getenv("MONGO_URI"))
db = client["MSE"]
schemas = db["schemas"]
instances = db["instances"]

# --- Models ---
class SchemaField(BaseModel):
    name: str
    type: str
    required: bool = False
    enum: Optional[List[str]] = None
    item_type: Optional[str] = None  # for lists

class SchemaDefinition(BaseModel):
    schema_id: str
    description: str
    domain: str
    version: str = "1.0.0"
    fields: List[SchemaField]
    created_by: str
    tags: List[str]

class InstanceData(BaseModel):
    schema_id: str
    data: dict
    created_by: str

# --- Routes ---
@app.post("/schemas/create")
async def create_schema(request: Request):
    body = await request.json()
    schema = SchemaDefinition(**body)
    schemas.insert_one(schema.dict())
    return {"status": "schema_created", "schema_id": schema.schema_id}

@app.get("/schemas")
async def list_schemas():
    return list(schemas.find({}, {"_id": 0}))

@app.get("/schemas/{schema_id}")
async def get_schema(schema_id: str):
    schema = schemas.find_one({"schema_id": schema_id}, {"_id": 0})
    if not schema:
        return {"error": "schema not found"}
    return schema

@app.post("/instances/create")
async def create_instance(request: Request):
    body = await request.json()
    instance = InstanceData(**body)
    schema = schemas.find_one({"schema_id": instance.schema_id})
    if not schema:
        return {"error": "schema not found"}

    # Validate fields
    missing = []
    for field in schema["fields"]:
        if field.get("required") and field["name"] not in instance.data:
            missing.append(field["name"])
    if missing:
        return {"error": "missing required fields", "fields": missing}

    # Save instance
    instance_id = str(uuid.uuid4())
    instances.insert_one({
        "instance_id": instance_id,
        "schema_id": instance.schema_id,
        "data": instance.data,
        "created_by": instance.created_by
    })
    return {"status": "instance_created", "instance_id": instance_id}

@app.get("/instances/{schema_id}")
async def list_instances(schema_id: str):
    return list(instances.find({"schema_id": schema_id}, {"_id": 0}))
