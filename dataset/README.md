Dataset preparation guidance

Folder structure

Organize images into a directory with one subfolder per class. Example:

data/your_dataset/
  Healthy/
  Blight/
  Rust/
  Powdery_Mildew/

Each class folder should contain JPEG/PNG images of leaves for that class.

Tips
- Minimum: aim for 200 images per class for decent baseline results.
- Use data augmentation (rotation, flips, shifts) to expand small classes.
- Keep filenames unique and avoid special characters.
- Split dataset using an 80/20 train/validation ratio (the training script uses `validation_split=0.2`).

Public datasets
- PlantVillage: https://github.com/spMohanty/PlantVillage-Dataset
- Kaggle plant disease datasets

Labeling
- Use folder names as labels. If you need canonical names, keep a mapping file.

Notes
- If class names contain spaces, the training pipeline will still work, but using underscores is safer for filenames and URLs.
