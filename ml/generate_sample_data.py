import os
import numpy as np
import cv2
from pathlib import Path


def generate_sample_images(output_dir='data/sample_dataset', samples_per_class=30):
    """Generate synthetic plant leaf images for testing."""
    output_path = Path(output_dir)
    classes = ['Healthy', 'Blight', 'Rust', 'Powdery_Mildew']

    for class_name in classes:
        class_dir = output_path / class_name
        class_dir.mkdir(parents=True, exist_ok=True)

        for i in range(samples_per_class):
            # Create synthetic leaf image
            img = np.zeros((256, 256, 3), dtype=np.uint8)

            if class_name == 'Healthy':
                # Green leaf
                img[:, :] = [50, 150, 50]
                cv2.circle(img, (128, 128), 80, (80, 200, 80), -1)
            elif class_name == 'Blight':
                # Green with brown spots
                img[:, :] = [100, 150, 80]
                cv2.circle(img, (128, 128), 80, (100, 120, 60), -1)
                for _ in range(5):
                    x, y = np.random.randint(60, 200, 2)
                    cv2.circle(img, (x, y), np.random.randint(10, 25), (40, 50, 30), -1)
            elif class_name == 'Rust':
                # Green with orange-red spots
                img[:, :] = [100, 150, 80]
                cv2.circle(img, (128, 128), 80, (100, 120, 60), -1)
                for _ in range(8):
                    x, y = np.random.randint(60, 200, 2)
                    cv2.circle(img, (x, y), np.random.randint(5, 15), (20, 100, 200), -1)
            else:  # Powdery_Mildew
                # Green with white powder
                img[:, :] = [100, 150, 80]
                cv2.circle(img, (128, 128), 80, (100, 120, 60), -1)
                for _ in range(20):
                    x, y = np.random.randint(60, 200, 2)
                    cv2.circle(img, (x, y), 2, (240, 240, 240), -1)

            # Add noise
            noise = np.random.randint(-10, 10, img.shape).astype(np.int16)
            img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

            img_path = class_dir / f'{class_name}_{i:03d}.jpg'
            cv2.imwrite(str(img_path), img)

        print(f'Generated {samples_per_class} images for class: {class_name}')

    print(f'Sample dataset created at: {output_dir}')


if __name__ == '__main__':
    generate_sample_images()
