import argparse
import requests

import os
from io import BytesIO
import time

import numpy as np
import pandas as pd
import json
import psutil

from PIL import Image
import matplotlib.pyplot as plt

def measure_cpu_usage(func, *args, **kwargs):

    # Start CPU usage monitoring
    start_cpu_percent = psutil.cpu_percent(interval=None)
    start_time = time.time()

    # Execute the function
    result = func(*args, **kwargs)

    # Stop CPU usage monitoring
    end_time = time.time()
    end_cpu_percent = psutil.cpu_percent(interval=None)

    cpu_usage = end_cpu_percent - start_cpu_percent
    execution_time = end_time - start_time

    return {
        "result": result,
        "cpu_usage_percent": cpu_usage,
        "execution_time_seconds": execution_time
    }


def read_embeddings(embedding_file):
    try:
        embeddings = pd.read_csv(embedding_file, header=None)
        embeddings_list = embeddings.values.tolist()
    except FileNotFoundError:
        print(f"File not found: {embedding_file}")
        return None

    # clean the embeddings
    hash_map = {}
    for emb_list in embeddings_list:
        query_text = emb_list[0]
        embedding = eval(emb_list[1])
        dim = np.array(embedding).ndim
        if query_text not in hash_map:
            if dim == 1:
                hash_map[query_text] = [embedding]
            elif dim == 2:
                hash_map[query_text] = list(embedding)
        else:
            hash_map[query_text].append(embedding)
        
    return hash_map

def show_image(image_path):
    try:
        if image_path.startswith("https"):
            response = requests.get(image_path)
            image = Image.open(BytesIO(response.content))
        else:
            data_folder = os.getenv("DATA_FOLDER", "data")
            image_path = os.path.join(data_folder, image_path)
            image = Image.open(image_path)
        plt.imshow(image)
        plt.axis("off")
        plt.show()
    except FileNotFoundError:
        print(f"File not found: {image_path}")

def parse_result_and_show(response):
    most_similar = response["most_similar"][0]
    filepath = most_similar.split("file:")[1]
    show_image(filepath)

def query_with_text(base_url, query, endpoint="/query/"):
    url = f"{base_url}{endpoint}"

    payload = {
        "query_string": query
    }
    try:
        response = requests.get(
            url=url,
            headers={"Content-Type": "application/json"},
            json=payload
            )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while accessing API: {e}")
        return None

def query_with_embedding(base_url, embedding, endpoint="/query/embedding/"):
    url = f"{base_url}{endpoint}"

    payload = {
        "embeddings": embedding
    }
    try:
        response = requests.get(
            url=url,
            headers={"Content-Type": "application/json"},
            json=payload
            )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while accessing API: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Test API query endpoint.")
    parser.add_argument("--base-url", type=str, default="http://localhost:8000")
    parser.add_argument("--query", type=str)
    parser.add_argument( "--embedding_file", type=str)
    parser.add_argument("--num", type=int)

    args = parser.parse_args()

    start_time = time.time()
    if args.embedding_file:
        base_url = args.base_url
        embeddings = read_embeddings(args.embedding_file)
        for idx, (query, embedding) in enumerate(embeddings.items()):
            if args.num or args.num == 0:
                if idx != args.num:
                    continue
            print(query)
            response = query_with_embedding(args.base_url, embedding)

            metrics = measure_cpu_usage(query_with_embedding, args.base_url, embedding)
            response = metrics["result"]
            cpu_usage = metrics["cpu_usage_percent"]
            print(f"CPU usage: {cpu_usage}")
    else:
        response = query_with_text(args.base_url, args.query)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")
    parse_result_and_show(response)

if __name__ == "__main__":
    main()
