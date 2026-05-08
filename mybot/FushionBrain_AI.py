import requests
import json
import asyncio
import config

HEADERS = {
    "X-Key" : f"Key {config.API_KEY}",
    "X-Secret" : f"Secret {config.SECRET_KEY}"
}
URL = "https://api-key.fusionbrain.ai/"

async def generate(prompt):
    params = {
        "type": "GENERATE",
        "width": 1024,
        "height": 1024,
        "numImages": 1,
        "generateParams": {"query": prompt}
    }

    files = {
        "model_id" : (None, 4),
        "params" : (None, json.dumps(params), "application/json")
    }

    response = requests.post(URL + 'key/api/v1/text2image/run', headers=HEADERS, files=files)
    print(response)
    data = response.json()
    attempts = 0
    while attempts < 40:
        response = requests.get(URL + 'key/api/v1/text2image/status/' + data['uuid'], headers=HEADERS)
        data = response.json()
        print(data)
        if data['status'] == 'DONE':
            print(data)
            return data['images']
        attempts += 1
        await asyncio.sleep(3)