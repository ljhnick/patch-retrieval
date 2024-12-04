import asyncio
from gradio_client import Client

client = Client("AltarAI1/colqwen-embedding-api", hf_token="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")

async def generate_query_embedding(query):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: client.predict(text=query, api_name="/predict")
    )
    # result = client.predict(
    #     text=query,
    #     api_name="/predict"
    # )
    return result["embeddings"][0]