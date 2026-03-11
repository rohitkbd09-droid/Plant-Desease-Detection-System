# Smart Plant Disease Detection and Recommendation System

A full-stack deep learning application for detecting plant diseases from leaf images and providing treatment recommendations.

## Features

- **Disease Detection**: Upload/capture leaf images and get instant disease classification
- **ML Model**: Scikit-learn RandomForest classifier with color histogram features (Python 3.14 compatible)
- **Treatment Recommendations**: Get pesticide, fertilizer, and preventive measures for detected diseases
- **Voice Interface**: Speak disease names to get recommendations and hear results (Web Speech API)
- **Multilingual Support**: Translate recommendations to Spanish, Hindi, and more
- **Text-to-Speech**: Audio output in multiple languages
- **User-Friendly UI**: Simple web interface with image upload and mobile camera support

## Quick Start

### 1. Install Python 3.8+

Download from https://www.python.org/downloads/ and ensure "Add Python to PATH" is checked.

### 2. Setup Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 4. Generate Sample Dataset and Train Model

```powershell
# From project root
python ml\generate_sample_data.py
python ml\train.py --data_dir data\sample_dataset --epochs 10
```

This creates:
- `backend/model.pkl` - trained classifier
- `backend/model.json` - class metadata

### 5. Run Backend Server

```powershell
cd backend
python app.py
```

Server will start at: http://localhost:5000

### 6. Open Frontend

Visit http://localhost:5000/ in your browser (Chrome recommended for voice features).

## Testing

Run the API test suite:

```powershell
python test_api_direct.py
```

Expected output:
- Frontend route: PASS
- Disease recommendation: PASS
- Image prediction: PASS
- Translation: PASS

## Project Structure

```
PLANT/
├── backend/              # Flask API
│   ├── app.py           # Main Flask application
│   ├── model.py         # Model loader & predictor
│   ├── requirements.txt  # Python dependencies
│   └── uploads/         # Uploaded images & generated audio
├── frontend/            # Web UI
│   └── index.html       # Single-page app with voice support
├── ml/                  # Training & inference
│   ├── train.py         # Model training script
│   ├── infer.py         # Single image inference
│   ├── validate_dataset.py  # Dataset validator
│   └── generate_sample_data.py  # Synthetic data generator
├── data/                # Datasets
│   └── sample_dataset/  # Generated sample for testing
├── recommendations/     # Disease treatment DB
│   └── recommendations.json
├── dataset/            # Dataset preparation guide
└── test_api_direct.py  # API tests
```

## API Endpoints

### POST `/predict`
Upload a leaf image to detect disease.
```
Request: multipart/form-data with 'image' field
Response: { disease, confidence, recommendation }
```

### POST `/recommendation`
Get treatment for a disease name.
```
Request: { "disease": "Blight" }
Response: { "disease", "recommendation" }
```

### POST `/translate`
Translate text to another language.
```
Request: { "text": "Healthy", "dest": "es" }
Response: { "translated": "Saludable" }
```

### POST `/speak`
Generate TTS audio (requires internet).
```
Request: { "text": "Disease detected", "lang": "en" }
Response: { "file": "tts_abc123.mp3" }
```

## Training Your Own Model

### 1. Prepare Dataset

Organize images into folders by disease:
```
data/my_dataset/
  ├── Healthy/
  ├── Blight/
  ├── Rust/
  └── Powdery_Mildew/
```

Each folder should have 100+ images (JPG/PNG).

### 2. Validate Dataset

```powershell
python ml\validate_dataset.py data\my_dataset --min 50
```

### 3. Train Model

```powershell
python ml\train.py --data_dir data\my_dataset --epochs 20
```

### 4. Test Single Image

```powershell
python ml\infer.py --model backend\model.pkl --image data\my_dataset\Healthy\sample.jpg
```

## Frontend Features

- **Image Upload**: Click to upload or drag-drop leaf images
- **Mobile Camera**: Capture directly from device camera (iOS/Android)
- **Voice Input**: Speak disease name (Chrome/Edge required)
- **Voice Output**: Hear disease recommendations in selected language
- **Language Selection**: Choose from English, Hindi, Spanish

## Troubleshooting

### "Cannot connect to localhost:5000"
- Ensure Flask server is running: `python backend/app.py`
- Try: http://127.0.0.1:5000

### Translation/TTS not working
- Check internet connection
- Mock translations are available offline
- Frontend gracefully degrades without internet

### Model not loading
- Verify `backend/model.pkl` exists
- Check `backend/model.json` has class indices
- App falls back to random predictions if model missing

### Voice input not working
- Use Chrome or Edge browser
- Enable microphone permissions
- Check browser console for errors (F12)

## Technical Stack

- **Backend**: Flask (Python)
- **ML Model**: scikit-learn RandomForest
- **Image Processing**: OpenCV
- **Frontend**: HTML5, JavaScript
- **Voice**: Web Speech API (client), gTTS (server)
- **Translation**: Mock translations (local) + googletrans (online)
- **Database**: JSON recommendations (upgrade to DB for production)

## Next Steps (Production Ready)

- Replace mock translations with cloud API (Google Cloud Translate, etc.)
- Add database (MySQL, PostgreSQL) for disease/recommendation management
- Build mobile app (React Native / Flutter)
- Deploy backend (Heroku, AWS, GCP)
- Add admin panel for managing diseases and stats
- Improve ML model with transfer learning (MobileNet, EfficientNet)
- Add CI/CD pipeline (GitHub Actions)

## License

MIT

## Support

For issues, see troubleshooting section or check Flask debug output.
