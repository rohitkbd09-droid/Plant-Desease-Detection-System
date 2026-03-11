import argparse
import json
from pathlib import Path
import cv2
import numpy as np
import joblib


def extract_features(image_path, target_size=(64, 64)):
    """Extract color histogram features from image."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        img = cv2.resize(img, target_size)
        hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        return hist.flatten()
    except Exception:
        return None


def load_metadata(model_path):
    p = Path(model_path)
    meta_file = p.with_suffix('.json')
    if meta_file.exists():
        with open(meta_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def predict(model_path, img_path):
    model = joblib.load(model_path)
    meta = load_metadata(model_path)
    class_map = meta.get('class_indices', {})

    feat = extract_features(img_path)
    if feat is None:
        return {'error': 'Failed to extract features from image'}
    feat = np.expand_dims(feat, axis=0)
    idx = model.predict(feat)[0]
    conf = float(model.predict_proba(feat)[0].max())
    label = class_map.get(str(idx), str(idx))
    return {'label': label, 'confidence': conf}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True, help='Path to saved model (.h5)')
    p.add_argument('--image', required=True, help='Path to image file')
    args = p.parse_args()
    res = predict(args.model, args.image)
    print(json.dumps(res, indent=2))
