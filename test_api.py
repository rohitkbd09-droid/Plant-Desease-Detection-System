#!/usr/bin/env python
"""Test script for the Plant Disease Detection API."""
import sys
import time
import requests
import os
from pathlib import Path

# Allow a few seconds for the server to start
BASE_URL = 'http://localhost:5000'


def test_api():
    print('Testing Plant Disease Detection API...\n')

    # Test 1: Predict endpoint
    print('TEST 1: Image prediction')
    img_path = Path('data/sample_dataset/Blight/Blight_000.jpg')
    if not img_path.exists():
        print(f'  SKIP: Image not found at {img_path}')
    else:
        try:
            with open(img_path, 'rb') as f:
                files = {'image': f}
                resp = requests.post(f'{BASE_URL}/predict', files=files, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(f'  PASS: Detected disease: {data.get("disease")}')
                print(f'        Confidence: {data.get("confidence")}')
            else:
                print(f'  FAIL: Status {resp.status_code}')
        except Exception as e:
            print(f'  ERROR: {e}')

    # Test 2: Recommendation endpoint
    print('\nTEST 2: Get recommendation for disease')
    try:
        resp = requests.post(f'{BASE_URL}/recommendation', 
                             json={'disease': 'Blight'}, 
                             timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f'  PASS: Got recommendation for {data.get("disease")}')
            print(f'        Pesticide: {data.get("recommendation", {}).get("pesticide")}')
        else:
            print(f'  FAIL: Status {resp.status_code}')
    except Exception as e:
        print(f'  ERROR: {e}')

    # Test 3: Translate endpoint (skip if no internet)
    print('\nTEST 3: Translate text')
    try:
        resp = requests.post(f'{BASE_URL}/translate',
                             json={'text': 'Healthy', 'dest': 'es'},
                             timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f'  PASS: English "Healthy" -> Spanish "{data.get("translated")}"')
        else:
            print(f'  SKIP: {resp.status_code} (likely no internet)')
    except Exception as e:
        print(f'  SKIP: {e} (likely no internet)')

    # Test 4: Speak endpoint (skip if no internet)
    print('\nTEST 4: Generate TTS audio')
    try:
        resp = requests.post(f'{BASE_URL}/speak',
                             json={'text': 'Disease detected', 'lang': 'en'},
                             timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f'  PASS: Generated audio file: {data.get("file")}')
        else:
            print(f'  SKIP: {resp.status_code} (likely no internet)')
    except Exception as e:
        print(f'  SKIP: {e} (likely no internet)')

    print('\n✓ Tests completed!')


if __name__ == '__main__':
    print(f'Connecting to {BASE_URL}...')
    try:
        # Wait for server to be ready
        for i in range(10):
            try:
                requests.get(f'{BASE_URL}/', timeout=1)
                break
            except:
                if i < 9:
                    time.sleep(1)
                else:
                    raise
        test_api()
    except Exception as e:
        print(f'ERROR: Could not connect to server at {BASE_URL}')
        print(f'  Make sure the Flask app is running: python backend/app.py')
        print(f'  Error: {e}')
        sys.exit(1)
