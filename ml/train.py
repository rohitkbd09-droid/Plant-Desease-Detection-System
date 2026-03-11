import os
import json
import argparse
from pathlib import Path
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
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


def train(data_dir, epochs=10, batch_size=32, output='backend/model.pkl'):
    """Train using scikit-learn RandomForest on color histogram features."""
    data_path = Path(data_dir)
    X, y, class_names = [], [], []
    class_map = {}

    for idx, class_dir in enumerate(sorted(data_path.iterdir())):
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        class_names.append(class_name)
        class_map[idx] = class_name
        for img_file in list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png')) + list(class_dir.glob('*.jpeg')):
            feat = extract_features(str(img_file))
            if feat is not None:
                X.append(feat)
                y.append(idx)

    if len(X) == 0:
        print('No images found in', data_dir)
        return

    X = np.array(X)
    y = np.array(y)

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'Training on {len(X)} images, {len(class_names)} classes')
    model = RandomForestClassifier(n_estimators=50, max_depth=20, n_jobs=-1)
    model.fit(X, y)

    joblib.dump(model, str(out_path))
    print('Model saved to', out_path)

    meta = {'class_indices': class_map, 'class_names': class_names}
    meta_file = out_path.with_suffix('.json')
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print('Metadata saved to', meta_file)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data_dir', required=True)
    p.add_argument('--epochs', type=int, default=10)
    args = p.parse_args()
    train(args.data_dir, epochs=args.epochs)
