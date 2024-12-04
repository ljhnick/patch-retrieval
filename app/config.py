import os
import dotenv

class Config:
    def __init__(self):
        
        self.REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        self.REDIS_PORT = os.getenv('REDIS_PORT', 6379)