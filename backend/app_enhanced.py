"""
Advanced Smart Plant Disease Detection and Crop Advisory System
Features: Real-time detection, severity classification, weather integration,
location-based recommendations, crop calendar, health tracking, PDF reports
"""

import os
import json
import uuid
import sys
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import enhanced modules
from enhanced_model import EnhancedModel
from database import db, ScanHistory, UserProfile, CropInformation, CropCalendar, EnvironmentalData, HealthTrendAnalysis, init_db
from weather_service import WeatherService, LocationService, DiseaseRiskAnalyzer
from crop_calendar import CropCalendarManager
from pdf_generator import PDFReportGenerator

# Optional dependencies
try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

try:
    from googletrans import Translator
    translator = Translator()
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# Initialize Flask app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, '..', 'frontend'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///plant_disease.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and CORS
CORS(app)
init_db(app)

# Initialize models
model = EnhancedModel()
pdf_generator = PDFReportGenerator(REPORTS_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_recommendations(disease=None):
    """Load recommendations from JSON file."""
    rec_file = os.path.join(BASE_DIR, '..', 'recommendations', 'recommendations.json')
    try:
        with open(rec_file, 'r', encoding='utf-8') as f:
            recs = json.load(f)
            if disease:
                return recs.get(disease, recs.get('default', {}))
            return recs
    except Exception as e:
        print(f"Error loading recommendations: {e}")
        return {} if disease else {'default': {}}


# ============= CORE DETECTION ENDPOINTS =============

@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease with severity classification and recommendations."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'no image part'}), 400
        
        file = request.files['image']
        user_id = request.form.get('user_id', 'anonymous')
        crop_type = request.form.get('crop_type', 'Unknown')
        field_location = request.form.get('field_location', '')
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Save uploaded image
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get model prediction
        prediction = model.predict(filepath)
        disease = prediction.get('disease', 'Unknown')
        confidence = prediction.get('confidence', 0.0)
        severity = prediction.get('severity', 'unknown')
        severity_score = prediction.get('severity_score', 0)
        affected_area = prediction.get('affected_area_percent', 0)
        
        # Load recommendations
        recommendations = load_recommendations(disease)
        
        # Get weather data if coordinates provided
        environmental_data = {}
        disease_risk = {}
        if latitude and longitude:
            weather = WeatherService.get_weather(latitude, longitude)
            if weather:
                environmental_data = {
                    'temperature': weather.get('temperature'),
                    'humidity': weather.get('humidity'),
                    'weather_condition': weather.get('weather'),
                    'wind_speed': weather.get('wind_speed')
                }
                
                # Analyze disease risk
                disease_risk = DiseaseRiskAnalyzer.calculate_disease_risk(weather, 'South_Asia', crop_type, disease)
        
        # Store scan in database
        scan = ScanHistory(
            user_id=user_id,
            image_filename=filename,
            image_path=filepath,
            disease_name=disease,
            severity_level=severity,
            confidence=confidence,
            recommendations=recommendations,
            environmental_data=environmental_data,
            crop_type=crop_type,
            field_location=field_location,
            latitude=latitude,
            longitude=longitude,
            notes=f"Affected area: {affected_area:.1f}%"
        )
        db.session.add(scan)
        db.session.commit()
        
        response = {
            'scan_id': scan.id,
            'disease': disease,
            'confidence': round(confidence, 4),
            'severity': severity,
            'severity_score': severity_score,
            'affected_area_percent': round(affected_area, 2),
            'recommendation_urgency': prediction.get('recommendation_urgency', 'medium'),
            'recommendations': recommendations,
            'environmental_data': environmental_data,
            'disease_risk': disease_risk,
            'timestamp': scan.timestamp.isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error in /predict: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    """Retrieve previous scan results."""
    try:
        scan = ScanHistory.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= USER & CROP MANAGEMENT =============

@app.route('/user', methods=['POST'])
def create_user():
    """Create or update user profile."""
    try:
        data = request.get_json()
        
        user = UserProfile.query.filter_by(email=data.get('email')).first()
        if not user:
            user = UserProfile(
                user_id=str(uuid.uuid4()),
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                region=data.get('region'),
                state=data.get('state'),
                country=data.get('country'),
                language=data.get('language', 'en'),
                default_latitude=data.get('latitude'),
                default_longitude=data.get('longitude')
            )
            db.session.add(user)
        else:
            # Update existing user
            user.name = data.get('name', user.name)
            user.phone = data.get('phone', user.phone)
            user.region = data.get('region', user.region)
            user.language = data.get('language', user.language)
        
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile."""
    try:
        user = UserProfile.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/crop', methods=['POST'])
def create_crop():
    """Create crop information."""
    try:
        data = request.get_json()
        
        crop = CropInformation(
            crop_id=str(uuid.uuid4()),
            user_id=data.get('user_id'),
            crop_name=data.get('crop_name'),
            crop_variety=data.get('crop_variety'),
            field_name=data.get('field_name'),
            field_area_hectares=data.get('field_area_hectares', type=float),
            current_stage=data.get('current_stage', 'seedling'),
            status=data.get('status', 'active'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            soil_type=data.get('soil_type'),
            irrigation_type=data.get('irrigation_type')
        )
        
        db.session.add(crop)
        db.session.commit()
        return jsonify(crop.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/crop/<crop_id>', methods=['GET'])
def get_crop(crop_id):
    """Get crop information."""
    try:
        crop = CropInformation.query.get(crop_id)
        if not crop:
            return jsonify({'error': 'Crop not found'}), 404
        return jsonify(crop.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/crops/<user_id>', methods=['GET'])
def get_user_crops(user_id):
    """Get all crops for a user."""
    try:
        crops = CropInformation.query.filter_by(user_id=user_id).all()
        return jsonify([crop.to_dict() for crop in crops]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= CROP CALENDAR & SCHEDULING =============

@app.route('/calendar/crop/<crop_name>', methods=['GET'])
def get_calendar(crop_name):
    """Get crop calendar."""
    try:
        region = request.args.get('region', None)
        calendar = CropCalendarManager.get_crop_calendar(crop_name, region)
        return jsonify(calendar), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calendar/tasks/<crop_id>', methods=['GET'])
def get_upcoming_tasks(crop_id):
    """Get upcoming farming tasks."""
    try:
        crop = CropInformation.query.get(crop_id)
        if not crop:
            return jsonify({'error': 'Crop not found'}), 404
        
        current_month = datetime.now().month
        days_ahead = request.args.get('days_ahead', 30, type=int)
        
        tasks = CropCalendarManager.get_upcoming_tasks(
            crop.crop_name, 
            current_month, 
            crop.crop_id,
            days_ahead
        )
        
        return jsonify({
            'crop_name': crop.crop_name,
            'upcoming_tasks': tasks
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calendar/fertilizer/<crop_name>/<float:field_area>', methods=['GET'])
def get_fertilizer_schedule(crop_name, field_area):
    """Get fertilizer application schedule."""
    try:
        schedule = CropCalendarManager.get_fertilizer_schedule(crop_name, field_area)
        return jsonify({
            'crop_name': crop_name,
            'field_area_hectares': field_area,
            'schedule': schedule
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calendar/irrigation/<crop_name>', methods=['GET'])
def get_irrigation_schedule(crop_name):
    """Get irrigation schedule."""
    try:
        region = request.args.get('region', None)
        schedule = CropCalendarManager.get_irrigation_schedule(crop_name, region)
        return jsonify({
            'crop_name': crop_name,
            'irrigation_schedule': schedule
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= WEATHER & LOCATION SERVICES =============

@app.route('/weather', methods=['POST'])
def get_weather():
    """Get weather data and disease risk assessment."""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        disease = data.get('disease', 'General')
        crop_type = data.get('crop_type', 'Unknown')
        
        if not latitude or not longitude:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Get weather
        weather = WeatherService.get_weather(latitude, longitude)
        
        # Get region info
        region_info = LocationService.get_region_from_coordinates(latitude, longitude)
        
        # Calculate disease risk
        disease_risk = DiseaseRiskAnalyzer.calculate_disease_risk(weather, region_info['region'], crop_type, disease)
        
        # Get region-specific recommendations
        region_recommendations = LocationService.get_region_specific_recommendations(
            region_info['region'], 
            disease, 
            disease_risk.get('risk_level', 'medium')
        )
        
        response = {
            'weather': weather,
            'region_info': region_info,
            'disease_risk': disease_risk,
            'region_recommendations': region_recommendations
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/location/region', methods=['POST'])
def get_region():
    """Get region information from coordinates."""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        region_info = LocationService.get_region_from_coordinates(latitude, longitude)
        current_month = datetime.now().month
        
        # Get seasonal diseases
        crop = data.get('crop', 'Rice')
        seasonal_diseases = LocationService.get_seasonal_diseases(region_info['region'], crop, current_month)
        
        response = {
            'region_info': region_info,
            'seasonal_disease_forecast': seasonal_diseases
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= SCAN HISTORY & ANALYTICS =============

@app.route('/scans/<user_id>', methods=['GET'])
def get_user_scans(user_id):
    """Get all scans for a user."""
    try:
        limit = request.args.get('limit', 50, type=int)
        scans = ScanHistory.query.filter_by(user_id=user_id).order_by(ScanHistory.timestamp.desc()).limit(limit).all()
        return jsonify([scan.to_dict() for scan in scans]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/scans/crop/<crop_id>', methods=['GET'])
def get_crop_scans(crop_id):
    """Get all scans for a specific crop."""
    try:
        scans = ScanHistory.query.filter_by(crop_type=crop_id).order_by(ScanHistory.timestamp.desc()).all()
        return jsonify([scan.to_dict() for scan in scans]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dashboard/<user_id>', methods=['GET'])
def get_dashboard(user_id):
    """Get crop health dashboard analytics."""
    try:
        # Get user's scans
        scans = ScanHistory.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_scans = len(scans)
        healthy_count = sum(1 for s in scans if s.disease_name == 'Healthy')
        disease_count = total_scans - healthy_count
        
        # Disease frequency
        disease_freq = {}
        severity_dist = {'mild': 0, 'moderate': 0, 'severe': 0}
        
        for scan in scans:
            disease_freq[scan.disease_name] = disease_freq.get(scan.disease_name, 0) + 1
            severity_dist[scan.severity_level] = severity_dist.get(scan.severity_level, 0) + 1
        
        most_common_disease = max(disease_freq.items(), key=lambda x: x[1])[0] if disease_freq else 'Unknown'
        
        # Calculate recovery rate (scans with recovery status)
        recovered = sum(1 for s in scans if s.recovery_status == 'recovered')
        recovery_rate = (recovered / total_scans * 100) if total_scans > 0 else 0
        
        dashboard_data = {
            'total_scans': total_scans,
            'healthy_count': healthy_count,
            'disease_count': disease_count,
            'disease_frequency': disease_freq,
            'severity_distribution': severity_dist,
            'most_common_disease': most_common_disease,
            'recovery_rate': round(recovery_rate, 2),
            'recent_scans': [s.to_dict() for s in scans[-10:]]
        }
        
        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= REPORT GENERATION =============

@app.route('/report/pdf/<scan_id>', methods=['GET'])
def generate_disease_report(scan_id):
    """Generate PDF report for a scan."""
    try:
        scan = ScanHistory.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        # Prepare report data
        detection_data = {
            'scan_id': scan.id,
            'disease_name': scan.disease_name,
            'confidence': scan.confidence,
            'severity_level': scan.severity_level,
            'affected_area_percent': 35.0,  # Would be extracted from model
            'recommendations': scan.recommendations,
            'environmental_data': scan.environmental_data,
            'crop_type': scan.crop_type,
            'timestamp': scan.timestamp.isoformat()
        }
        
        # Generate PDF
        report_path = pdf_generator.generate_detection_report(detection_data, scan.image_path)
        
        return send_file(report_path, as_attachment=True, download_name=f"disease_report_{scan_id}.pdf")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/report/summary/<user_id>', methods=['GET'])
def generate_summary_report(user_id):
    """Generate summary PDF report for all user's scans."""
    try:
        user = UserProfile.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        scans = ScanHistory.query.filter_by(user_id=user_id).all()
        if not scans:
            return jsonify({'error': 'No scans found for user'}), 404
        
        user_data = user.to_dict()
        scans_data = [s.to_dict() for s in scans]
        
        # Generate PDF
        report_path = pdf_generator.generate_summary_report(user_data, scans_data)
        
        return send_file(report_path, as_attachment=True, download_name=f"farm_summary_{user_id}.pdf")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= MODEL IMPROVEMENT & CONTINUOUS LEARNING =============

@app.route('/training/upload', methods=['POST'])
def upload_training_image():
    """Upload image for model retraining."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'no image part'}), 400
        
        file = request.files['image']
        disease_label = request.form.get('disease_label')
        
        if not disease_label:
            return jsonify({'error': 'disease_label required'}), 400
        
        filename = f"training_{disease_label}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'training_data', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        file.save(filepath)
        
        return jsonify({
            'message': 'Image uploaded for retraining',
            'filename': filename,
            'disease_label': disease_label
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= UTILITY ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_info': model.get_model_info(),
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/recommendations/<disease>', methods=['GET'])
def get_recommendations(disease):
    """Get recommendations for a disease."""
    try:
        recs = load_recommendations(disease)
        return jsonify({
            'disease': disease,
            'recommendations': recs
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Serve frontend."""
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
