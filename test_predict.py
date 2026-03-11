#!/usr/bin/env python
"""
Minimal test of predict endpoint with actual image file
"""
import requests
import os
import time

BASE_URL = "http://localhost:5000"

# Wait for server
time.sleep(2)

# Find an image to upload
test_image = None
for img in ['backend/uploads/tomato_leaf.jpg', 'data/sample_dataset/Healthy/1.jpg']:
    if os.path.exists(img):
        test_image = img
        break

if not test_image:
    print("No test image found!")
    exit(1)

print(f"\nTesting /predict with: {test_image}")
print(f"File exists: {os.path.exists(test_image)}")
print(f"File size: {os.path.getsize(test_image)} bytes")

# Test the endpoint
try:
    with open(test_image, 'rb') as f:
        files = {'image': f}
        r = requests.post(f"{BASE_URL}/predict", files=files, timeout=10)
        print(f"\nStatus: {r.status_code}")
        print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"\nError: {e}")
