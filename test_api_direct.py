#!/usr/bin/env python
"""Direct test of the Flask app without requests library."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app

# Test using Flask test client
client = app.test_client()

print('Testing Plant Disease Detection API (Direct)\n')

# Test 1: Frontend route
print('TEST 1: Frontend index route')
try:
    resp = client.get('/')
    if resp.status_code == 200:
        print(f'  PASS: Status {resp.status_code}')
    else:
        print(f'  FAIL: Status {resp.status_code}')
except Exception as e:
    print(f'  ERROR: {e}')

# Test 2: Recommendation endpoint
print('\nTEST 2: Get recommendation for disease')
try:
    resp = client.post('/recommendation', json={'disease': 'Blight'})
    if resp.status_code == 200:
        data = resp.get_json()
        print(f'  PASS: Got recommendation for {data.get("disease")}')
        print(f'        Pesticide: {data.get("recommendation", {}).get("pesticide")}')
    else:
        print(f'  FAIL: Status {resp.status_code}')
except Exception as e:
    print(f'  ERROR: {e}')

# Test 3: Predict endpoint (with sample image)
print('\nTEST 3: Image prediction')
from pathlib import Path
img_path = Path('data/sample_dataset/Blight/Blight_000.jpg')
if not img_path.exists():
    print(f'  SKIP: Image not found at {img_path}')
else:
    try:
        with open(img_path, 'rb') as f:
            resp = client.post('/predict', data={'image': (f, 'test.jpg')})
        if resp.status_code == 200:
            data = resp.get_json()
            print(f'  PASS: Detected disease: {data.get("disease")}')
            print(f'        Confidence: {data.get("confidence")}')
        else:
            print(f'  FAIL: Status {resp.status_code}: {resp.get_json()}')
    except Exception as e:
        print(f'  ERROR: {e}')

# Test 4: Translate endpoint
print('\nTEST 4: Translate (may skip if no internet)')
try:
    resp = client.post('/translate', json={'text': 'Healthy', 'dest': 'es'})
    if resp.status_code == 200:
        data = resp.get_json()
        print(f'  PASS: Translated: {data.get("translated")}')
    elif resp.status_code == 503:
        print(f'  SKIP: {resp.get_json().get("error")}')
    else:
        print(f'  FAIL: Status {resp.status_code}')
except Exception as e:
    print(f'  SKIP: {e}')

print('\n✓ Tests completed!')
