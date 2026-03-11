# Advanced Smart Plant Disease Detection System - API Documentation

## Overview
This is a comprehensive, mobile-first agricultural technology platform that combines deep learning-based disease detection with weather integration, crop calendars, and farm management tools.

## Key Features

### 1. **Real-time Disease Detection with Severity Classification**
- Deep learning model predicting disease type and severity (mild, moderate, severe)
- Affected area percentage calculation
- Confidence scoring

### 2. **Mobile-First Design**
- Responsive interface optimized for smartphones and tablets
- Real-time camera capture for plant leaf scanning
- Progressive Web App (PWA) ready
- Works offline with local caching

### 3. **Weather Integration**
- Real-time weather data from OpenWeatherMap/WeatherAPI
- Disease risk assessment based on environmental conditions
- Region-specific weather recommendations
- Optimal spray timing suggestions

### 4. **Geolocation & Regional Services**
- Automatic region detection from coordinates
- Seasonal disease forecasting
- Region-specific crop recommendations
- Local agricultural contact information

### 5. **Crop Calendar Management**
- Crop-specific sowing to harvesting schedules
- Fertilizer application timelines
- Irrigation schedules
- Pest and disease surveillance calendars

### 6. **Scan History & Analytics**
- Complete scan history with timestamps
- Crop health dashboard with statistics
- Disease trend analysis
- Recovery tracking

### 7. **PDF Report Generation**
- Professional disease analysis reports
- Farm summary reports
- Downloadable recommendations
- Environmental data logs

### 8. **Continuous Learning**
- Upload facility for new training images
- Model improvement capabilities
- Field data collection for accuracy enhancement

---

## API Endpoints

### Authentication & User Management

#### POST `/user`
Create or update user profile
```json
{
  "name": "Farmer Name",
  "email": "farmer@email.com",
  "phone": "+91-9999999999",
  "region": "North India",
  "state": "Punjab",
  "country": "India",
  "latitude": 31.5204,
  "longitude": 74.3587,
  "language": "en"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "name": "Farmer Name",
  "email": "farmer@email.com",
  "region": "North India"
}
```

#### GET `/user/<user_id>`
Get user profile

---

### Disease Detection

#### POST `/predict`
Predict disease from image with severity classification

**Form Data:**
- `image` (file) - Plant leaf image
- `user_id` (string) - User identifier
- `crop_type` (string) - Crop name (Rice, Wheat, Cotton, etc.)
- `field_location` (string) - Field name or area
- `latitude` (float, optional) - GPS latitude
- `longitude` (float, optional) - GPS longitude

**Response:**
```json
{
  "scan_id": "uuid",
  "disease": "Blight",
  "confidence": 0.92,
  "severity": "moderate",
  "severity_score": 2,
  "affected_area_percent": 35.5,
  "recommendation_urgency": "high",
  "recommendations": {
    "pesticide": "Copper oxychloride",
    "dosage": "2 g/l",
    "method": "Spray on affected leaves",
    "preventive": ["Remove infected leaves", "Improve air circulation"]
  },
  "environmental_data": {
    "temperature": 28.5,
    "humidity": 82,
    "weather_condition": "cloudy"
  },
  "disease_risk": {
    "risk_level": "high",
    "risk_score": 85,
    "recommendations": ["High risk detected", "Increase surveillance"]
  },
  "timestamp": "2026-01-21T10:30:00"
}
```

#### GET `/predict/<scan_id>`
Retrieve previous scan results

---

### Crop Management

#### POST `/crop`
Create crop information
```json
{
  "user_id": "user_uuid",
  "crop_name": "Rice",
  "crop_variety": "Basmati",
  "field_name": "Field A",
  "field_area_hectares": 5.0,
  "current_stage": "vegetative",
  "latitude": 31.5204,
  "longitude": 74.3587,
  "soil_type": "Loamy",
  "irrigation_type": "Drip"
}
```

#### GET `/crop/<crop_id>`
Get crop information

#### GET `/crops/<user_id>`
Get all crops for a user

---

### Crop Calendar

#### GET `/calendar/crop/<crop_name>?region=North_India`
Get crop calendar
```json
{
  "crop_name": "Rice",
  "region": "North India",
  "season": "Kharif",
  "events": [
    {
      "month": 5,
      "event": "Sowing",
      "duration": 20,
      "details": "Transplanting seedlings"
    }
  ]
}
```

#### GET `/calendar/tasks/<crop_id>?days_ahead=30`
Get upcoming farming tasks
```json
{
  "crop_name": "Rice",
  "upcoming_tasks": [
    {
      "event_type": "First Fertilizer",
      "scheduled_date": "2026-02-15",
      "days_until": 5,
      "duration_days": 1,
      "description": "Apply NPK 20:20:20",
      "priority": "high"
    }
  ]
}
```

#### GET `/calendar/fertilizer/<crop_name>/<field_area>`
Get fertilizer application schedule

#### GET `/calendar/irrigation/<crop_name>`
Get irrigation schedule

---

### Weather & Location

#### POST `/weather`
Get weather data and disease risk assessment
```json
{
  "latitude": 31.5204,
  "longitude": 74.3587,
  "disease": "Blight",
  "crop_type": "Rice"
}
```

**Response:**
```json
{
  "weather": {
    "temperature": 28.5,
    "humidity": 82,
    "weather": "cloudy",
    "wind_speed": 12.5
  },
  "region_info": {
    "region": "South_Asia",
    "countries": ["India", "Pakistan"]
  },
  "disease_risk": {
    "disease": "Blight",
    "risk_level": "high",
    "risk_score": 85,
    "risk_factors": ["Temperature is favorable", "High humidity increases risk"]
  },
  "region_recommendations": {
    "approved_pesticides": ["Tricyclazole", "Hexaconazole"],
    "timing_considerations": ["Spray during monsoon", "Apply every 7-10 days"]
  }
}
```

#### POST `/location/region`
Get region information and seasonal diseases
```json
{
  "latitude": 31.5204,
  "longitude": 74.3587,
  "crop": "Rice"
}
```

---

### Scan History & Analytics

#### GET `/scans/<user_id>?limit=50`
Get all scans for a user

#### GET `/scans/crop/<crop_id>`
Get scans for specific crop

#### GET `/dashboard/<user_id>`
Get crop health dashboard
```json
{
  "total_scans": 45,
  "healthy_count": 30,
  "disease_count": 15,
  "disease_frequency": {
    "Healthy": 30,
    "Blight": 10,
    "Rust": 5
  },
  "severity_distribution": {
    "mild": 5,
    "moderate": 7,
    "severe": 3
  },
  "most_common_disease": "Blight",
  "recovery_rate": 65.5,
  "recent_scans": []
}
```

---

### Report Generation

#### GET `/report/pdf/<scan_id>`
Download PDF report for a specific scan

#### GET `/report/summary/<user_id>`
Download summary report for all user's scans

---

### Model Training & Improvement

#### POST `/training/upload`
Upload image for model retraining
```
Form Data:
- image (file)
- disease_label (string)
```

---

### Health & Status

#### GET `/health`
Health check endpoint
```json
{
  "status": "healthy",
  "model_info": {
    "has_tensorflow_model": true,
    "has_sklearn_model": true,
    "supported_classes": ["Healthy", "Blight", "Rust", "Powdery Mildew"],
    "class_count": 4
  },
  "timestamp": "2026-01-21T10:30:00"
}
```

#### GET `/recommendations/<disease>`
Get recommendations for a disease

---

## Database Models

### ScanHistory
Stores all plant disease detection scans
- id, user_id, disease_name, severity_level, confidence
- affected_area_percent, recommendations, environmental_data
- crop_type, field_location, latitude, longitude
- timestamp, recovery_status

### UserProfile
User account and preference information
- user_id, name, email, phone
- region, state, country, language
- default_latitude, default_longitude

### CropInformation
Crop and field details
- crop_id, crop_name, crop_variety, field_name
- current_stage, status, sowing_date, expected_harvest_date
- field_area_hectares, soil_type, irrigation_type

### CropCalendar
Farming schedules and events
- event_id, crop_id, event_type
- recommended_month, description, details

### EnvironmentalData
Environmental conditions at scan time
- temperature_celsius, humidity_percent, weather_condition
- disease_risk_level, optimal_spray_time

### HealthTrendAnalysis
Aggregated crop health analytics
- total_scans, healthy_count, disease_count
- disease_frequency, severity_distribution
- recovery_rate, trend_analysis

---

## Installation & Setup

### Backend Requirements
```bash
pip install -r backend/requirements.txt
```

### Environment Variables
Create `.env` file:
```
DATABASE_URL=sqlite:///plant_disease.db
OPENWEATHER_API_KEY=your_key
WEATHERAPI_KEY=your_key
FLASK_ENV=production
```

### Run Backend
```bash
cd backend
python app_enhanced.py
```

### Frontend Setup
The frontend is in `frontend/index_mobile.html` with `frontend/app.js`

Serve using:
```bash
# Using Python
python -m http.server 8000

# Or using Flask built-in server
# Already served by app_enhanced.py on port 5000
```

---

## Usage Examples

### 1. Create User Account
```bash
curl -X POST http://localhost:5000/user \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rajesh Kumar",
    "email": "rajesh@farm.com",
    "region": "North India",
    "latitude": 31.5204,
    "longitude": 74.3587
  }'
```

### 2. Analyze Plant Image
```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@leaf.jpg" \
  -F "user_id=user_123" \
  -F "crop_type=Rice" \
  -F "field_location=Field A" \
  -F "latitude=31.5204" \
  -F "longitude=74.3587"
```

### 3. Get Weather Data
```bash
curl -X POST http://localhost:5000/weather \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 31.5204,
    "longitude": 74.3587,
    "disease": "Blight",
    "crop_type": "Rice"
  }'
```

### 4. Get Crop Calendar
```bash
curl "http://localhost:5000/calendar/crop/Rice?region=North_India"
```

### 5. Download Report
```bash
curl "http://localhost:5000/report/pdf/scan_id_123" -o report.pdf
```

---

## Mobile Features

### Camera Capture
- Real-time video from device camera
- Manual photo capture with preview
- Auto-orientation support

### Geolocation
- Optional GPS location detection
- Used for weather and region-specific recommendations

### Offline Support
- Local storage of scan history
- Settings cache
- Works without internet (limited functionality)

### Progressive Web App
- Installable on home screen
- Offline access to dashboard
- Native app-like experience

---

## Performance & Optimization

- Model inference: < 2 seconds on mobile
- Image compression before transmission (90% quality)
- Lazy loading of camera and heavy modules
- Caching of API responses
- Database query optimization with indexes

---

## Security

- CORS enabled for cross-origin requests
- Input validation on all endpoints
- SQL injection prevention (SQLAlchemy ORM)
- File upload validation
- Environment variable protection

---

## Troubleshooting

### Camera not working
- Check browser permissions
- Ensure HTTPS on production
- Test on different browsers

### Geolocation not available
- Check device location services
- Ensure HTTPS connection
- Browser permissions required

### API connection failed
- Verify backend is running
- Check CORS settings
- Verify API_BASE URL in app.js

### Database errors
- Ensure database is initialized
- Check database file permissions
- Verify SQLAlchemy configuration

---

## Future Enhancements

1. Multi-language support (Hindi, Tamil, Telugu)
2. Offline ML model using TensorFlow.js
3. Video-based disease detection
4. Pest detection capabilities
5. Weather-triggered alerts
6. Integration with agricultural markets
7. Community sharing and knowledge base
8. Government subsidy information
9. Drone image analysis
10. API rate limiting and usage analytics

---

## Contact & Support

For issues, feature requests, or questions, please contact the development team.

**System Version:** 2.0 Advanced
**Last Updated:** January 2026
