import requests
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

def get_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.ok:
            data = response.json()
            if "numbers" in data:
                return data["numbers"]
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    urls = request.args.getlist('url')
    merged_numbers = []
    start_time = time.time()
    for url in urls:
        numbers = get_numbers(url)
        merged_numbers.extend(numbers)
    merged_numbers = list(set(merged_numbers))
    merged_numbers.sort()
    end_time = time.time()
    response = {
        "numbers": merged_numbers,
        "processing_time": end_time - start_time
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8008)
