from fastapi import APIRouter

from pydantic import BaseModel

from app.db.redis_client import db
from app.utils.similarity import late_interaction
from app.services.vectorize import generate_query_embedding

import time

router = APIRouter()

class Query(BaseModel):
    query_string: str

class QueryEmbeddings(BaseModel):
    embeddings: list


def retrieve_with_embeddings(embedding):
    prev_time = time.time()
    score_table = db.data.copy()

    start_time = time.time()
    for file, file_emb in db.data.items():
        if isinstance(file_emb, str):
            continue
        start = time.time()
        score = late_interaction(data_emb=file_emb, query_emb=embedding)
        end = time.time()
        score_table[file] = score
    end_time = time.time()

    start_sort = time.time()
    sorted_dict = dict(sorted(score_table.items(), key=lambda item: item[1], reverse=True))
    end_sort = time.time()
    # print(f"Time taken for sorting: {end_sort - start_sort}")
    elements = list(sorted_dict.items())
    most_similar = elements[0]
    return {"most_similar": most_similar}

@router.get("/")
async def retrieve_files_with_query(query: Query):
    query_string = query.query_string
    embedding = await generate_query_embedding(query_string)
    result = retrieve_with_embeddings(embedding)
    return result

@router.get("/embedding/")
async def retrieve_files_with_embedding(query_embedding: QueryEmbeddings):
    embedding = query_embedding.embeddings
    result = retrieve_with_embeddings(embedding)
    return result