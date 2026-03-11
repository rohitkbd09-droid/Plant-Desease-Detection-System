import os
import json
import uuid
import sys
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
sys.path.insert(0, os.path.dirname(__file__))
from model import Model, PLANT_DISEASES_DB
from pdf_generator import PDFReportGenerator
from gtts import gTTS

# Try to import optional dependencies for PDF and weather
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.units import inch
    HAS_REPORTLAB = True
except Exception:
    HAS_REPORTLAB = False
    print('Warning: reportlab not installed - PDF reports disabled')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, '..', 'frontend'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = Model()

# Try to load translator, but allow app to run without it
translator = None
try:
    from googletrans import Translator
    translator = Translator()
except Exception as e:
    print(f'Warning: Translation unavailable: {e}')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception:
        return jsonify({'error': 'File not found'}), 404


@app.route('/predict', methods=['POST'])
def predict():
    try:
        print(f"[PREDICT] Request keys: {list(request.files.keys())}")
        print(f"[PREDICT] Content-Type: {request.content_type}")
        
        if 'image' not in request.files:
            error_msg = f"no image part. Received files: {list(request.files.keys())}"
            print(f"[ERROR] {error_msg}")
            return jsonify({'error': error_msg}), 400
        file = request.files['image']
        if file.filename == '':
            print(f"[ERROR] no selected file")
            return jsonify({'error': 'no selected file'}), 400
        if not (file and allowed_file(file.filename)):
            error_msg = f"file type not allowed: {file.filename}"
            print(f"[ERROR] {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        print(f"[PREDICT] File saved: {path}")
        pred = model.predict(path)
        print(f"[PREDICT] Prediction: {pred}")
        
        # load recommendations
        rec_file = os.path.join(BASE_DIR, '..', 'recommendations', 'recommendations.json')
        try:
            with open(rec_file, 'r', encoding='utf-8') as f:
                recs = json.load(f)
        except Exception:
            recs = {}
        
        disease = pred.get('disease', 'Unknown')
        rec = recs.get(disease, recs.get('default', {}))
        treatment_summary = get_treatment_summary(rec)
        complete_treatment_process = build_complete_treatment_process(disease, rec)
        
        # Get additional fields from request if available
        crop_type = request.form.get('crop_type', 'Unknown')
        field_location = request.form.get('field_location', '')
        user_id = request.form.get('user_id', '')
        latitude = request.form.get('latitude', '')
        longitude = request.form.get('longitude', '')
        
        # Determine severity if available from model
        severity = pred.get('severity', 'unknown')
        affected_area_percent = pred.get('affected_area_percent', 0.0)
        analysis_method = pred.get('analysis_method', 'unknown')
        
        # Generate enhanced suggestion based on disease
        suggestion = generate_disease_suggestion(disease, severity, affected_area_percent)
        
        # Get detailed disease information
        disease_details = get_disease_details(disease)
        
        response = {
            'disease': disease,
            'confidence': round(float(pred.get('confidence', 0.0)), 4),
            'severity': severity,
            'affected_area_percent': affected_area_percent,
            'analysis_method': analysis_method,
            'suggestion': suggestion,
            'disease_cause': disease_details.get('cause', 'Unknown'),
            'disease_symptoms': disease_details.get('symptoms', []),
            'conditions': disease_details.get('conditions', ''),
            'recovery_steps': disease_details.get('recovery_steps', []),
            'prevention': disease_details.get('prevention', ''),
            'recovery_time': disease_details.get('recovery_time', ''),
            'timestamp': datetime.now().isoformat(),
            'crop_type': crop_type,
            'field_location': field_location,
            'user_id': user_id,
            'latitude': latitude,
            'longitude': longitude,
            'recommendation': rec,
            'treatment_summary': treatment_summary,
            'complete_treatment_process': complete_treatment_process,
            'image_filename': filename
        }
        return jsonify(response)
    except Exception as e:
        print(f'Error in predict: {str(e)}')
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


def generate_disease_suggestion(disease, severity, confidence):
    """Generate helpful suggestion based on detected disease."""
    # Get disease details from database
    disease_info = PLANT_DISEASES_DB.get(disease, {})
    
    suggestions = {
        'Blight': {
            'High': '🚨 URGENT: Early blight detected! Immediately remove infected leaves and apply copper fungicide. Increase plant spacing for airflow.',
            'Medium': '⚠️ Blight detected. Remove affected leaves carefully, spray with fungicide weekly, and avoid overhead watering.',
            'Low': '💡 Minor blight symptoms. Monitor closely. Apply preventive fungicide if conditions are wet.',
        },
        'Rust': {
            'High': '🚨 URGENT: Rust infection is severe! Remove heavily infected leaves, apply sulfur-based fungicide, and increase air circulation.',
            'Medium': '⚠️ Rust detected. Spray with fungicide, remove affected leaves, and avoid wetting foliage when watering.',
            'Low': '💡 Light rust symptoms. Monitor and apply fungicide if weather stays humid.',
        },
        'Powdery Mildew': {
            'High': '🚨 URGENT: Heavy powdery mildew infection! Treat immediately with baking soda solution or sulfur spray. Prune affected areas.',
            'Medium': '⚠️ Powdery mildew present. Use sulfur-based fungicide. Remove heavily affected leaves and improve ventilation.',
            'Low': '💡 Early powdery mildew. Treat with neem oil or baking soda spray. Increase airflow between plants.',
        },
        'Healthy': {
            'High': '✅ Excellent! Your plant is healthy. Continue regular maintenance and monitor for any changes.',
            'Medium': '✅ Plant looks good! Keep up your care routine and stay vigilant for disease symptoms.',
            'None': '✅ Perfect! Your plant is in great condition. Maintain current care practices.',
        }
    }
    
    disease_sugg = suggestions.get(disease, {})
    return disease_sugg.get(severity, f'Monitor your {disease} condition closely.')


def get_disease_details(disease):
    """Get detailed information about a disease."""
    return PLANT_DISEASES_DB.get(disease, {
        'cause': 'Disease information not available',
        'symptoms': [],
        'conditions': 'Monitor plant conditions',
        'recovery_steps': ['Consult local agricultural expert'],
        'prevention': 'Maintain good plant health',
        'recovery_time': 'Unknown'
    })



def load_recommendations():
    rec_file = os.path.join(BASE_DIR, '..', 'recommendations', 'recommendations.json')
    try:
        with open(rec_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def get_treatment_summary(recommendation):
    """Extract key treatment highlights from recommendation payload."""
    if not isinstance(recommendation, dict):
        return {
            'pesticide': 'Not specified',
            'fertilizer': 'Not specified',
            'dosage': 'Follow product label',
            'application_method': 'Follow agronomist guidance'
        }

    pesticide_info = recommendation.get('pesticide_recommendation', {})
    fertilizer_info = recommendation.get('fertilizer_recommendation', {})

    pesticide = recommendation.get('pesticide') or pesticide_info.get('product') or 'Not specified'
    fertilizer = recommendation.get('fertilizer') or fertilizer_info.get('product') or 'Not specified'
    dosage = recommendation.get('dosage') or pesticide_info.get('dosage') or 'Follow product label'
    method = recommendation.get('method') or pesticide_info.get('application_method') or 'Follow agronomist guidance'

    return {
        'pesticide': pesticide,
        'fertilizer': fertilizer,
        'dosage': dosage,
        'application_method': method
    }


def build_complete_treatment_process(disease, recommendation):
    """Build a complete, actionable treatment workflow."""
    if disease == 'Healthy':
        return [
            'No pesticide or curative fertilizer needed right now.',
            'Continue balanced nutrition and irrigation as per crop stage.',
            'Inspect leaves and stems every 3 to 4 days for early symptoms.',
            'Use preventive sanitation: remove debris and keep tools clean.'
        ]

    if isinstance(recommendation, dict):
        process = recommendation.get('treatment_process')
        if isinstance(process, list) and process:
            return process

    summary = get_treatment_summary(recommendation)
    preventive = recommendation.get('preventive', []) if isinstance(recommendation, dict) else []
    schedule = recommendation.get('schedule', 'Re-evaluate in 5 to 7 days') if isinstance(recommendation, dict) else 'Re-evaluate in 5 to 7 days'

    steps = [
        'Step 1: Remove and destroy heavily infected leaves before chemical application.',
        'Step 2: Prepare spray tank with clean water and use protective gear (gloves, mask, full sleeves).',
        f"Step 3: Mix pesticide '{summary['pesticide']}' at recommended dose ({summary['dosage']}).",
        f"Step 4: Apply pesticide using this method: {summary['application_method']}.",
        f"Step 5: Apply fertilizer '{summary['fertilizer']}' after 24 to 48 hours to support recovery.",
        f"Step 6: Follow this schedule: {schedule}.",
    ]

    if preventive:
        steps.append(f"Step 7: Preventive actions: {', '.join(preventive)}.")

    steps.append('Step 8: Monitor symptom spread every 2 to 3 days and repeat only as per label instructions.')
    return steps


@app.route('/recommendation', methods=['POST'])
def recommendation():
    data = request.get_json(force=True)
    disease = data.get('disease', '').strip()
    if not disease:
        return jsonify({'error': 'no disease provided'}), 400
    recs = load_recommendations()
    rec = recs.get(disease, recs.get('default', {}))
    return jsonify({
        'disease': disease,
        'recommendation': rec,
        'treatment_summary': get_treatment_summary(rec),
        'complete_treatment_process': build_complete_treatment_process(disease, rec)
    })


@app.route('/treatment-plan', methods=['POST'])
def treatment_plan():
    """Comprehensive treatment plan with step-by-step process and multiple options."""
    data = request.get_json(force=True)
    disease = data.get('disease', '').strip()
    if not disease:
        return jsonify({'error': 'no disease provided'}), 400
    
    recs = load_recommendations()
    rec = recs.get(disease, recs.get('default', {}))
    
    # Build comprehensive response
    response = {
        'disease': disease,
        'disease_severity': rec.get('disease_severity', 'Unknown'),
        'recovery_time': rec.get('recovery_time', 'Unknown'),
        'primary_pesticide': {
            'product': rec.get('pesticide'),
            'details': rec.get('pesticide_recommendation', {})
        },
        'alternative_pesticides': rec.get('alternative_pesticides', []),
        'primary_fertilizer': {
            'product': rec.get('fertilizer'),
            'details': rec.get('fertilizer_recommendation', {})
        },
        'alternative_fertilizers': rec.get('alternative_fertilizers', []),
        'equipment_needed': rec.get('equipment_needed', []),
        'preventive_measures': rec.get('preventive', []),
        'step_by_step_treatment': rec.get('treatment_process', []),
        'success_indicators': rec.get('success_indicators', []),
        'key_precautions': rec.get('key_precautions', []),
        'monitoring_indicators': rec.get('monitoring_indicators', []),
        'important_notes': rec.get('important_notes', [])
    }
    
    return jsonify(response)


@app.route('/translate', methods=['POST'])
def translate():
    if translator is None:
        return jsonify({'error': 'Translation service unavailable (no internet)'}), 503
    data = request.get_json(force=True)
    text = data.get('text', '')
    dest = data.get('dest', 'en')
    if not text:
        return jsonify({'error': 'no text provided'}), 400
    try:
        # Note: googletrans 4.x returns async functions; use sync alternative or mock
        # For now, return a mock translation
        translations = {
            ('Healthy', 'es'): 'Saludable',
            ('Healthy', 'hi'): 'स्वस्थ',
            ('Healthy', 'te'): 'ఆరోగ్యకరమైన',
            ('Blight', 'es'): 'Tizón',
            ('Blight', 'hi'): 'अंगमारी',
            ('Blight', 'te'): 'ఆర్ద్ర రోగం',
            ('Powdery_Mildew', 'es'): 'Mildiu Polvoriento',
            ('Powdery_Mildew', 'hi'): 'चूर्णी फफूंद',
            ('Powdery_Mildew', 'te'): 'పొడి పట్టు',
            ('Rust', 'es'): 'Óxido',
            ('Rust', 'hi'): 'रस्ट',
            ('Rust', 'te'): 'గడ్డ',
        }
        key = (text, dest)
        translated = translations.get(key, text)
        return jsonify({'translated': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json(force=True)
    text = data.get('text', '')
    lang = data.get('lang', 'en')
    
    # Map language codes to gTTS language codes
    lang_map = {
        'en': 'en',
        'es': 'es',
        'hi': 'hi',
        'te': 'te',
        'en-US': 'en',
        'es-ES': 'es',
        'hi-IN': 'hi',
        'te-IN': 'te'
    }
    gtts_lang = lang_map.get(lang, 'en')
    
    if not text or len(text.strip()) == 0:
        print("ERROR: No text provided for speech")
        return jsonify({'error': 'No text provided for speech'}), 400
    
    # create unique filename
    fname = f"tts_{uuid.uuid4().hex}.mp3"
    out_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    
    try:
        print(f"Generating speech: lang={gtts_lang}, text_len={len(text)}")
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(out_path)
        print(f"✓ Audio saved to {out_path}")
        return jsonify({'file': fname, 'success': True})
    except Exception as e:
        error_msg = f"Speech generation failed: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# ===== NEW ENDPOINTS FOR ENHANCED FEATURES =====

@app.route('/severity', methods=['POST'])
def severity():
    """Detect disease severity based on image analysis"""
    if 'image' not in request.files:
        return jsonify({'error': 'no image part'}), 400
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        # Placeholder: In real implementation, analyze image intensity
        severity_score = 0.6  # 0-1 scale
        severity_level = 'Moderate' if severity_score > 0.5 else ('Mild' if severity_score > 0.3 else 'Severe')
        return jsonify({
            'severity': severity_level,
            'score': severity_score,
            'description': f'{severity_level} disease detected - {int(severity_score * 100)}% coverage'
        })
    return jsonify({'error': 'file type not allowed'}), 400


@app.route('/weather', methods=['POST'])
def weather():
    """Provide weather-based farming advice"""
    data = request.get_json(force=True)
    disease = data.get('disease', '').strip()
    location = data.get('location', 'default').lower()
    
    weather_advice = {
        'Blight': {
            'default': 'High humidity promotes blight. Ensure proper drainage and avoid overhead watering.',
            'monsoon': 'Blight thrives in monsoon. Apply preventive fungicides weekly.',
            'summer': 'Use shade nets to reduce stress. Monitor for disease signs.'
        },
        'Rust': {
            'default': 'Rust spreads in warm, humid conditions. Improve air circulation.',
            'monsoon': 'Rust is active in monsoon. Spray sulfur dust preventively.',
            'summer': 'Rust dormant in extreme heat. Focus on plant vigor.'
        },
        'Powdery Mildew': {
            'default': 'Powdery mildew prefers dry, cool conditions. Space plants well.',
            'monsoon': 'Less active in monsoon rains but can occur on covered areas.',
            'summer': 'Increase with temperature fluctuations. Spray neem oil.'
        }
    }
    
    advice = weather_advice.get(disease, {}).get(location, weather_advice.get(disease, {}).get('default', 'No specific advice available'))
    return jsonify({'weather_advice': advice, 'location': location})


@app.route('/crop-calendar', methods=['GET'])
def crop_calendar():
    """Get crop calendar based on current month"""
    month = datetime.now().month
    crop_tasks = {
        1: ['Prepare soil', 'Sow winter crops', 'Apply fertilizers'],
        2: ['Monitor seedlings', 'Prune trees', 'Apply fungicides'],
        3: ['Transplant seedlings', 'Mulch beds', 'Scout for pests'],
        4: ['Harvest early crops', 'Prepare for summer', 'Store water'],
        5: ['Irrigation schedule', 'Pest management', 'Soil conservation'],
        6: ['Monsoon prep', 'Drain excess water', 'Apply lime'],
        7: ['Monitor water logging', 'Disease prevention', 'Weed control'],
        8: ['Check for blight', 'Prune infected parts', 'Apply fungicides'],
        9: ['Prepare for harvest', 'Control pests', 'Nutrient management'],
        10: ['Harvest primary crop', 'Soil testing', 'Prepare for rabi'],
        11: ['Sow rabi crops', 'Fertilizer application', 'Pest scouting'],
        12: ['Monitor growth', 'Frost protection', 'Winter management']
    }
    tasks = crop_tasks.get(month, [])
    return jsonify({'month': month, 'tasks': tasks, 'month_name': datetime.now().strftime('%B')})


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard statistics"""
    # Count uploaded images
    upload_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.png', '.jpg', '.jpeg'))]
    stats = {
        'total_analyses': len(upload_files),
        'healthy_detected': max(1, len(upload_files) // 4),
        'disease_detected': len(upload_files) - max(1, len(upload_files) // 4),
        'alerts_today': 2,
        'last_analysis': datetime.now().isoformat()
    }
    return jsonify(stats)


@app.route('/location-alert', methods=['POST'])
def location_alert():
    """Get location-based disease alerts"""
    data = request.get_json(force=True)
    location = data.get('location', 'unknown').lower()
    
    alerts = {
        'north': 'Blight outbreak reported in northern regions. Spray copper fungicides.',
        'south': 'Powdery mildew increasing. Maintain proper spacing.',
        'east': 'Rust detected. Apply sulfur dust preventively.',
        'west': 'Monitor for multiple diseases due to warm weather.',
        'unknown': 'No specific alerts. Monitor your crops regularly.'
    }
    
    alert = alerts.get(location, alerts['unknown'])
    return jsonify({'alert': alert, 'severity': 'High', 'region': location})


@app.route('/report/pdf', methods=['POST'])
def generate_pdf_report():
    """Generate professional PDF report for disease detection."""
    data = request.get_json(force=True)
    
    # Map the data to the format expected by PDFReportGenerator
    detection_data = {
        'disease_name': data.get('disease', 'Unknown'),
        'confidence': data.get('confidence', 0.0),
        'severity_level': data.get('severity', 'Unknown'),
        'affected_area_percent': data.get('affected_area_percent', 0.0),
        'recommendations': data.get('recommendation', {}),
        'complete_treatment_process': data.get('complete_treatment_process', []),
        'environmental_data': data.get('environmental_data', {}),
        'scan_id': f"SCAN_{uuid.uuid4().hex[:8].upper()}",
        'crop_type': data.get('crop_type', 'Unknown')
    }
    
    # Try to get image path
    image_filename = data.get('image_filename')
    image_path = None
    if image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

    try:
        # Use PDFReportGenerator if reportlab is available
        if HAS_REPORTLAB:
            generator = PDFReportGenerator(output_dir=app.config['UPLOAD_FOLDER'])
            filepath = generator.generate_detection_report(detection_data, image_path)
            report_name = os.path.basename(filepath)
            return jsonify({'file': report_name})
        
        # Fallback to HTML if reportlab not available
        report_name = f"Report_{uuid.uuid4().hex[:8]}.html"
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], report_name)
        
        # Generate HTML styled as PDF (original implementation)
        disease = data.get('disease', 'Analysis Report')
        confidence = data.get('confidence', 0.0)
        recommendation = data.get('recommendation', {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Disease Detection Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        @media print {{
            body {{
                background: white;
            }}
        }}
        .container {{
            max-width: 800px;
            margin: 20px auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        h1 {{
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
        }}
        .section {{
            margin: 25px 0;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #764ba2;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            padding-left: 12px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px;
            background: #f9f9f9;
            margin: 8px 0;
            border-radius: 4px;
            border-left: 3px solid #4facfe;
        }}
        .label {{
            font-weight: 600;
            color: #667eea;
            min-width: 150px;
        }}
        .value {{
            color: #333;
            flex: 1;
            text-align: right;
        }}
        .recommendation-item {{
            background: #f0f4ff;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            border-left: 4px solid #4facfe;
        }}
        .recommendation-item strong {{
            color: #667eea;
        }}
        .recommendation-item ul {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        .recommendation-item li {{
            margin: 5px 0;
            color: #555;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #999;
            font-size: 12px;
        }}
        .timestamp {{
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }}
        .confidence-bar {{
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: {confidence*100:.1f}%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: bold;
        }}
        @media print {{
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
            body {{
                background: white;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 Plant Disease Detection Report</h1>
        
        <div class="section">
            <div class="section-title">Disease Analysis</div>
            <div class="info-row">
                <span class="label">Disease Detected:</span>
                <span class="value"><strong>{disease}</strong></span>
            </div>
            <div class="info-row">
                <span class="label">Confidence Level:</span>
                <span class="value"><strong>{confidence*100:.1f}%</strong></span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill"></div>
            </div>
            <div class="info-row">
                <span class="label">Severity:</span>
                <span class="value">{data.get('severity', 'Unknown')}</span>
            </div>
            <div class="info-row">
                <span class="label">Affected Area:</span>
                <span class="value">{data.get('affected_area_percent', 0.0):.1f}%</span>
            </div>
            <div class="info-row">
                <span class="label">Analysis Method:</span>
                <span class="value">{data.get('analysis_method', 'Advanced Analysis')}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">What Caused This Disease?</div>
            <div class="recommendation-item">
                {data.get('disease_cause', 'Cause information not available')}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Recovery Steps</div>
"""
        
        recovery_steps = data.get('recovery_steps', [])
        if recovery_steps and isinstance(recovery_steps, list):
            for i, step in enumerate(recovery_steps, 1):
                html_content += f"""            <div class="recommendation-item">
                <strong>Step {i}:</strong> {step}
            </div>
"""
        
        html_content += f"""        </div>
        
        <div class="section">
            <div class="section-title">Prevention Tips</div>
            <div class="recommendation-item">
                {data.get('prevention', 'Maintain good plant care practices')}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Recovery Timeline</div>
            <div class="info-row">
                <span class="label">Estimated Recovery Time:</span>
                <span class="value"><strong>{data.get('recovery_time', 'Unknown')}</strong></span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Treatment Recommendations</div>
"""
        
        if isinstance(recommendation, dict) and recommendation:
            for key, value in recommendation.items():
                if value:
                    key_display = key.replace('_', ' ').title()
                    if isinstance(value, list):
                        html_content += f"""            <div class="recommendation-item">
                <strong>{key_display}:</strong>
                <ul>
"""
                        for item in value:
                            html_content += f"                    <li>{item}</li>\n"
                        html_content += """                </ul>
            </div>
"""
                    else:
                        html_content += f"""            <div class="recommendation-item">
                <strong>{key_display}:</strong> {value}
            </div>
"""
        else:
            html_content += """            <div class="recommendation-item">
                <strong>General Care:</strong> Monitor your plants regularly and consult with agricultural experts for specific treatment options.
            </div>
"""
        
        html_content += f"""        </div>
        
        <div class="footer">
            <p>For more information about plant disease management, please consult with agricultural experts or your local extension office.</p>
        </div>
        
        <div class="timestamp">
            Generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({'file': report_name})
    except Exception as e:
        print(f'Error generating report: {str(e)}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
