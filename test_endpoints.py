#!/usr/bin/env python
import requests
import json
import os
import time

BASE_URL = "http://localhost:5000"

print("\n" + "="*60)
print("Testing Plant Disease Detection Endpoints")
print("="*60)

# Test 1: Speak Endpoint
print("\n[TEST 1] Testing /speak endpoint...")
data = {"text": "Plant disease detected successfully", "lang": "en"}
try:
    r = requests.post(f"{BASE_URL}/speak", json=data, timeout=10)
    print(f"  Status: {r.status_code}")
    result = r.json()
    print(f"  Response: {result}")
    
    if r.status_code == 200 and 'file' in result:
        file_path = os.path.join("backend/uploads", result['file'])
        time.sleep(0.5)  # Wait for file
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✓ Audio file created: {result['file']} ({size} bytes)")
        else:
            print(f"  ✗ File not found at {file_path}")
    else:
        print(f"  ✗ Failed to generate audio")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: PDF Report Endpoint
print("\n[TEST 2] Testing /report/pdf endpoint...")
report_data = {
    "disease": "Early Blight",
    "confidence": 0.92,
    "severity": "Moderate",
    "affected_area_percent": 25,
    "analysis_method": "File-based Heuristic",
    "recommendation": {
        "treatment": "Apply fungicide",
        "spray_schedule": "Every 7-10 days"
    }
}
try:
    r = requests.post(f"{BASE_URL}/report/pdf", json=report_data, timeout=10)
    print(f"  Status: {r.status_code}")
    result = r.json()
    print(f"  Response: {result}")
    
    if r.status_code == 200 and 'file' in result:
        file_path = os.path.join("backend/uploads", result['file'])
        time.sleep(0.5)  # Wait for file
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✓ Report file created: {result['file']} ({size} bytes)")
        else:
            print(f"  ✗ File not found at {file_path}")
    else:
        print(f"  ✗ Failed to generate report")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: Check uploads folder
print("\n[TEST 3] Checking uploads folder...")
uploads_path = "backend/uploads"
if os.path.exists(uploads_path):
    files = os.listdir(uploads_path)
    print(f"  Files in {uploads_path}:")
    for f in files[:10]:  # Show first 10
        full_path = os.path.join(uploads_path, f)
        size = os.path.getsize(full_path)
        print(f"    - {f} ({size} bytes)")
    if len(files) > 10:
        print(f"    ... and {len(files)-10} more files")
else:
    print(f"  ✗ Uploads folder not found")

print("\n" + "="*60)
print("Test Complete")
print("="*60 + "\n")
