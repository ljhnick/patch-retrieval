import pyrootutils
pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

import base64
import json
import csv
import numpy as np
import redis
from app.config import Config

config = Config()
redis_client = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=False
)

def load_file_embeddings(file_path, key_prefix='file'):

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        prev = ''
        prev_embeddings = []
        for row in reader:
            file_path = row[1]
            if file_path != prev:
                if prev:
                    # embeddings = np.array(prev_embeddings, dtype=np.float32)
                    key = f'{key_prefix}:{prev}'
                    # redis_client.set(key, base64.b64encode(embeddings.tobytes()).decode('utf-8'))
                    redis_client.set(key, json.dumps(prev_embeddings))
                prev = file_path
                prev_embeddings = []

            embeddings = row[2]
            embeddings = eval(embeddings)
            prev_embeddings.append(embeddings)
        
        embeddings = np.array(prev_embeddings, dtype=np.float32)
        redis_client.set(key, json.dumps(prev_embeddings))

def get_all_data():
    cursor = 0
    all_data = {}

    while True:
        cursor, keys = redis_client.scan(cursor=cursor)

        for key in keys:
            key = str(key, 'utf-8')
            # Fetch the value for each key
            value = redis_client.get(key)
            all_data[key] = value

        # Break the loop when cursor returns to 0
        if cursor == 0:
            break

    return all_data

def preprocess_and_load():
    """
    Preprocess the image and query embeddings, and load them into Redis.
    """
    print("Loading image embeddings...")
    load_file_embeddings('data/file_embeddings.csv', 'file')

    print("Loading query embeddings...")
    # load_embeddings('data/query_embeddings.csv', 'query')

    print("All embeddings loaded into Redis successfully.")

if __name__ == "__main__":
    # all_data = get_all_data()
    # print(all_data)
    preprocess_and_load()