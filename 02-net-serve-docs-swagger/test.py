import requests
import json

# Test the API endpoint
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "messages": [
            {
                "role": "user",
                "content": "What colour is the sky?"
            }
        ],
        "stream": False
    }
)

# Parse and display the response
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)