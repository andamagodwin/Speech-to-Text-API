import requests
import json

url = "http://localhost:5000/transcribe?language=en-US"

try:
    with requests.post(url, stream=True) as r:
        print(f"Connection established. Status code: {r.status_code}")
        for line in r.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data:'):
                    data = json.loads(decoded[5:])
                    print(f"{data.get('type', 'unknown').upper()}: {data.get('transcript', '')}")
except requests.exceptions.ConnectionError as e:
    print(f"Failed to connect to server. Is it running? Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")