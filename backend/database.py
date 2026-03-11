"""
Database models and initialization for the smart plant disease detection system.
Handles: scan history, user data, crop information, and environmental conditions.
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import String, Integer, Float, DateTime, Boolean, JSON, Text

db = SQLAlchemy()


class ScanHistory(db.Model):
    """Stores all plant disease detection scans."""
    __tablename__ = 'scan_history'
    
    id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    user_id = db.Column(String(36), index=True)
    image_filename = db.Column(String(255), nullable=False)
    image_path = db.Column(String(500), nullable=False)
    disease_name = db.Column(String(100), nullable=False)
    severity_level = db.Column(String(20), nullable=False)  # mild, moderate, severe
    confidence = db.Column(Float, nullable=False)
    recommendations = db.Column(JSON)
    environmental_data = db.Column(JSON)  # temperature, humidity, location, weather
    crop_type = db.Column(String(100))
    field_location = db.Column(String(255))
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    timestamp = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(Text)
    treatment_applied = db.Column(Boolean, default=False)
    recovery_status = db.Column(String(50))  # not-started, in-progress, recovered
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disease_name': self.disease_name,
            'severity_level': self.severity_level,
            'confidence': self.confidence,
            'crop_type': self.crop_type,
            'field_location': self.field_location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat(),
            'environmental_data': self.environmental_data,
            'recovery_status': self.recovery_status,
            'recommendations': self.recommendations
        }


class UserProfile(db.Model):
    """Stores user information and preferences."""
    __tablename__ = 'user_profile'
    
    user_id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    name = db.Column(String(255))
    email = db.Column(String(255), unique=True, index=True)
    phone = db.Column(String(20))
    default_latitude = db.Column(Float)
    default_longitude = db.Column(Float)
    region = db.Column(String(255))
    state = db.Column(String(100))
    country = db.Column(String(100))
    language = db.Column(String(20), default='en')
    preferred_unit = db.Column(String(10), default='metric')  # metric or imperial
    notification_enabled = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'region': self.region,
            'state': self.state,
            'country': self.country,
            'language': self.language
        }


class CropInformation(db.Model):
    """Stores information about crops managed by user."""
    __tablename__ = 'crop_information'
    
    crop_id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    user_id = db.Column(String(36), db.ForeignKey('user_profile.user_id'), nullable=False)
    crop_name = db.Column(String(100), nullable=False)  # e.g., 'Wheat', 'Corn', 'Rice'
    crop_variety = db.Column(String(100))
    field_name = db.Column(String(255))
    field_area_hectares = db.Column(Float)
    sowing_date = db.Column(DateTime)
    expected_harvest_date = db.Column(DateTime)
    current_stage = db.Column(String(50))  # seedling, vegetative, flowering, maturation
    status = db.Column(String(50), default='active')  # active, completed, inactive
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    soil_type = db.Column(String(100))
    irrigation_type = db.Column(String(100))  # drip, flood, sprinkler, rain-fed
    notes = db.Column(Text)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'crop_id': self.crop_id,
            'crop_name': self.crop_name,
            'crop_variety': self.crop_variety,
            'field_name': self.field_name,
            'current_stage': self.current_stage,
            'status': self.status,
            'sowing_date': self.sowing_date.isoformat() if self.sowing_date else None,
            'expected_harvest_date': self.expected_harvest_date.isoformat() if self.expected_harvest_date else None
        }


class CropCalendar(db.Model):
    """Stores crop calendar with farming schedule."""
    __tablename__ = 'crop_calendar'
    
    event_id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    crop_id = db.Column(String(36), db.ForeignKey('crop_information.crop_id'), nullable=False)
    crop_name = db.Column(String(100), nullable=False)
    region = db.Column(String(255), nullable=False)
    event_type = db.Column(String(50), nullable=False)  # sowing, fertilizer, irrigation, spraying, harvesting
    recommended_month = db.Column(Integer)
    recommended_date = db.Column(DateTime)
    duration_days = db.Column(Integer)
    description = db.Column(Text)
    details = db.Column(JSON)  # e.g., fertilizer type, irrigation hours, pesticide name
    
    def to_dict(self):
        return {
            'event_id': self.event_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop_name,
            'region': self.region,
            'event_type': self.event_type,
            'recommended_month': self.recommended_month,
            'recommended_date': self.recommended_date.isoformat() if self.recommended_date else None,
            'description': self.description,
            'details': self.details
        }


class EnvironmentalData(db.Model):
    """Stores environmental conditions at time of scan."""
    __tablename__ = 'environmental_data'
    
    data_id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    scan_id = db.Column(String(36), db.ForeignKey('scan_history.id'), nullable=False)
    temperature_celsius = db.Column(Float)
    humidity_percent = db.Column(Float)
    rainfall_mm = db.Column(Float)
    wind_speed_kmh = db.Column(Float)
    uv_index = db.Column(Float)
    soil_moisture = db.Column(Float)
    weather_condition = db.Column(String(100))  # sunny, cloudy, rainy, etc.
    disease_risk_level = db.Column(String(20))  # low, medium, high
    optimal_spray_time = db.Column(String(100))  # early morning, late afternoon, etc.
    timestamp = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'data_id': self.data_id,
            'scan_id': self.scan_id,
            'temperature_celsius': self.temperature_celsius,
            'humidity_percent': self.humidity_percent,
            'weather_condition': self.weather_condition,
            'disease_risk_level': self.disease_risk_level,
            'optimal_spray_time': self.optimal_spray_time
        }


class HealthTrendAnalysis(db.Model):
    """Stores aggregated health analytics for dashboard."""
    __tablename__ = 'health_trend_analysis'
    
    analysis_id = db.Column(String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    user_id = db.Column(String(36), db.ForeignKey('user_profile.user_id'), nullable=False)
    crop_id = db.Column(String(36), db.ForeignKey('crop_information.crop_id'))
    period_start = db.Column(DateTime, nullable=False)
    period_end = db.Column(DateTime, nullable=False)
    total_scans = db.Column(Integer, default=0)
    healthy_count = db.Column(Integer, default=0)
    disease_count = db.Column(Integer, default=0)
    avg_severity = db.Column(Float)  # average severity level
    recovery_rate = db.Column(Float)  # percentage of recovered plants
    most_common_disease = db.Column(String(100))
    disease_frequency = db.Column(JSON)  # disease -> count mapping
    severity_distribution = db.Column(JSON)  # mild, moderate, severe counts
    trend_analysis = db.Column(JSON)  # trend data for charts
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'analysis_id': self.analysis_id,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'total_scans': self.total_scans,
            'healthy_count': self.healthy_count,
            'disease_count': self.disease_count,
            'avg_severity': self.avg_severity,
            'recovery_rate': self.recovery_rate,
            'most_common_disease': self.most_common_disease,
            'disease_frequency': self.disease_frequency,
            'severity_distribution': self.severity_distribution
        }


def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully")
