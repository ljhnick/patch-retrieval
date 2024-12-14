import redis
from app.config import Config

# Get configuration (e.g., Redis host and port)
config = Config()

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=False  # Set to False for binary data like embeddings
)

def get_all_data(client):
    cursor = 0
    all_data = {}

    while True:
        cursor, keys = client.scan(cursor=cursor)
        for key in keys:
            key = str(key, 'utf-8')
            value = redis_client.get(key)
            all_data[key] = value
        if cursor == 0:
            break
    return all_data

class DB:
    def __init__(self) -> None:
        self.client = redis_client
        self.data = self.load_all_data()

    def set_data(self, key, value):
        redis_client.set(key, value)
    
    def get_data(self, key):
        return redis_client.get(key)

    def delete_key(self, key):
        redis_client.delete(key)
    
    def key_exists(self, key):
        return redis_client.exists(key) > 0
    
    def set_data_with_expiry(self, key, value, ttl):
        redis_client.setex(key, ttl, value)

    def scan_keys(self, pattern):
        cursor = 0
        keys = []
        while True:
            cursor, batch_keys = redis_client.scan(cursor=cursor, match=pattern)
            keys.extend(batch_keys)
            if cursor == 0:
                break
        return keys
    
    def load_all_data(self):
        raw = get_all_data(self.client)
        for key, emb_string in raw.items():
            raw[key] = eval(emb_string)
        return raw
    
    def flush_database(self):
        redis_client.flushdb()

    

db = DB()