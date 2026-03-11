import os
from pathlib import Path


def validate_dataset(path, min_per_class=20):
    p = Path(path)
    if not p.exists():
        print('Path does not exist:', path)
        return False
    classes = [d for d in p.iterdir() if d.is_dir()]
    if len(classes) < 2:
        print('Need at least 2 class folders. Found:', len(classes))
        return False
    ok = True
    for c in classes:
        imgs = [f for f in c.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png')]
        print(f'Class "{c.name}": {len(imgs)} images')
        if len(imgs) < min_per_class:
            print(f'  WARNING: fewer than {min_per_class} images in class "{c.name}"')
            ok = False
    if ok:
        print('Dataset looks valid')
    else:
        print('Dataset may be insufficient; consider augmentation or more samples')
    return ok


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('path')
    p.add_argument('--min', type=int, default=20, help='Minimum images per class')
    args = p.parse_args()
    validate_dataset(args.path, min_per_class=args.min)
