Smart Plant Disease Detection and Recommendation System

Minimal scaffold for the Smart Plant Disease Detection project.

Structure
- `backend/` - Flask API and placeholder model
- `ml/` - training script for CNN model (Keras/TensorFlow)
- `frontend/` - simple web UI for image upload and result display
- `recommendations/` - JSON mapping of disease -> recommendations

Quick start (Windows)

1. Create a Python virtual environment and activate it

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

2. Run the backend

```powershell
cd backend
python app.py
```

3. Open `frontend/index.html` in a browser (or serve it via the Flask static endpoint).

Training

Use the training script in `ml/train.py`. Provide a dataset folder organized by class subfolders.

```powershell
python ml\train.py --data_dir path\to\dataset --epochs 10
```
