import pyrootutils
pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

import uvicorn

from fastapi import FastAPI
from app.api import query

app = FastAPI(
    title="Embedding Comparison/Retrieval Service",
    version="1.0.0"
)

app.include_router(query.router, prefix="/query", tags=["Query"])

@app.get("/")
def read_root():
    return {"message": "Running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)