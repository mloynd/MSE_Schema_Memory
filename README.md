# MSE Schema-Aware Memory API

A minimal FastAPI-based backend for the Memory Synthesis Engine (MSE) that supports:
- Dynamic schema storage
- Validated instance creation
- Schema-driven reasoning by external GPT agents

## Features
- Store and list schemas (e.g., for exercises, reports, any domain)
- Create validated instances of schema-based data
- MongoDB-native structure with thread-safe extensibility

## Routes

- `POST /schemas/create` – Create a new schema definition
- `GET /schemas` – List all schemas
- `GET /schemas/{schema_id}` – View one schema
- `POST /instances/create` – Insert a new instance with validation
- `GET /instances/{schema_id}` – List all instances of a schema

## Setup

```bash
git clone https://github.com/your-name/mse-schema-memory.git
cd mse-schema-memory
cp .env.example .env
# Fill in your MongoDB URI
pip install -r requirements.txt
uvicorn main:app --reload
```

## License
MIT
