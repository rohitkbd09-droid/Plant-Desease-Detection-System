"""
Weather data integration and location-based recommendation services.
"""

import os
import json
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import pytz

# Weather API configurations
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY', '')


class WeatherService:
    """Fetch real-time weather data for crop advisory."""
    
    @staticmethod
    def get_weather_openweather(lat: float, lon: float, api_key: str = OPENWEATHER_API_KEY) -> Optional[Dict]:
        """
        Fetch weather data from OpenWeatherMap API.
        
        Args:
            lat: Latitude
            lon: Longitude
            api_key: OpenWeatherMap API key
            
        Returns:
            Dictionary with weather information
        """
        if not api_key:
            return None
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'clouds': data['clouds']['all'],
                    'rain_probability': data.get('rain', {}).get('1h', 0),
                    'timestamp': datetime.fromtimestamp(data['dt']).isoformat(),
                    'source': 'openweathermap'
                }
        except Exception as e:
            print(f"Error fetching weather from OpenWeatherMap: {e}")
        
        return None

    @staticmethod
    def get_weather_weatherapi(lat: float, lon: float, api_key: str = WEATHERAPI_KEY) -> Optional[Dict]:
        """
        Fetch weather data from WeatherAPI.com.
        
        Args:
            lat: Latitude
            lon: Longitude
            api_key: WeatherAPI key
            
        Returns:
            Dictionary with weather information
        """
        if not api_key:
            return None
        
        try:
            url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&aqi=yes"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current']
                return {
                    'temperature': current['temp_c'],
                    'humidity': current['humidity'],
                    'weather': current['condition']['text'],
                    'wind_speed': current['wind_kph'],
                    'uv_index': current.get('uv', 0),
                    'visibility_km': current.get('vis_km', 0),
                    'precipitation_mm': current.get('precip_mm', 0),
                    'timestamp': datetime.fromisoformat(current['last_updated']).isoformat(),
                    'source': 'weatherapi'
                }
        except Exception as e:
            print(f"Error fetching weather from WeatherAPI: {e}")
        
        return None

    @staticmethod
    def get_weather(lat: float, lon: float) -> Optional[Dict]:
        """Get weather data from available APIs."""
        # Try primary API
        weather = WeatherService.get_weather_openweather(lat, lon)
        if weather:
            return weather
        
        # Fallback to secondary API
        weather = WeatherService.get_weather_weatherapi(lat, lon)
        if weather:
            return weather
        
        return None


class LocationService:
    """Handle geolocation and region-specific services."""
    
    # Crop disease patterns by region
    REGIONAL_DISEASE_PATTERNS = {
        'South_Asia': {
            'crops': ['Rice', 'Wheat', 'Cotton'],
            'common_diseases': {
                'Rice': ['Blast', 'Sheath Blight', 'Brown Spot', 'Bacterial Leaf Blight'],
                'Wheat': ['Rust', 'Powdery Mildew', 'Septoria Tritici Blotch'],
                'Cotton': ['Leaf Curl', 'Fusarium Wilt', 'Bacterial Blight']
            },
            'seasons': {
                'monsoon': {'start_month': 6, 'end_month': 10, 'high_disease_risk': True},
                'winter': {'start_month': 11, 'end_month': 2, 'high_disease_risk': False},
                'summer': {'start_month': 3, 'end_month': 5, 'high_disease_risk': False}
            }
        },
        'Sub_Saharan_Africa': {
            'crops': ['Maize', 'Sorghum', 'Cassava'],
            'common_diseases': {
                'Maize': ['Leaf Blight', 'Stem Rot', 'Maize Lethal Necrosis'],
                'Sorghum': ['Anthracnose', 'Ergot'],
                'Cassava': ['Cassava Brown Streak', 'Cassava Mosaic']
            },
            'seasons': {
                'rainy': {'start_month': 3, 'end_month': 11, 'high_disease_risk': True},
                'dry': {'start_month': 12, 'end_month': 2, 'high_disease_risk': False}
            }
        },
        'Latin_America': {
            'crops': ['Maize', 'Cassava', 'Potato'],
            'common_diseases': {
                'Maize': ['Rust', 'Blight', 'Rust'],
                'Cassava': ['Brown Leaf Spot', 'Superficial Scald'],
                'Potato': ['Late Blight', 'Early Blight']
            }
        }
    }

    @staticmethod
    def get_region_from_coordinates(lat: float, lon: float) -> Dict:
        """
        Determine region based on latitude and longitude.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with region information
        """
        # Simplified region detection
        if 5 <= lat <= 35 and 60 <= lon <= 100:
            region = 'South_Asia'
            countries = ['India', 'Pakistan', 'Bangladesh', 'Nepal', 'Sri Lanka']
        elif -35 <= lat <= 15 and -20 <= lon <= 55:
            region = 'Sub_Saharan_Africa'
            countries = ['Nigeria', 'Kenya', 'Uganda', 'Ethiopia', 'Zambia']
        elif -56 <= lat <= 13 and -117 <= lon <= -35:
            region = 'Latin_America'
            countries = ['Brazil', 'Mexico', 'Colombia', 'Argentina']
        else:
            region = 'Other'
            countries = []
        
        return {
            'region': region,
            'countries': countries,
            'latitude': lat,
            'longitude': lon
        }

    @staticmethod
    def get_seasonal_diseases(region: str, crop: str, month: int) -> list:
        """
        Get seasonal disease forecast for a crop in a region.
        
        Args:
            region: Region name
            crop: Crop name
            month: Month (1-12)
            
        Returns:
            List of likely diseases
        """
        try:
            region_data = LocationService.REGIONAL_DISEASE_PATTERNS.get(region, {})
            crop_diseases = region_data.get('common_diseases', {}).get(crop, [])
            
            # Filter by season
            seasons = region_data.get('seasons', {})
            is_high_risk_season = False
            
            for season, info in seasons.items():
                if info['start_month'] <= month <= info['end_month'] or \
                   (info['start_month'] > info['end_month'] and (month >= info['start_month'] or month <= info['end_month'])):
                    is_high_risk_season = info.get('high_disease_risk', False)
                    break
            
            return {
                'crop': crop,
                'region': region,
                'likely_diseases': crop_diseases,
                'high_risk_season': is_high_risk_season,
                'month': month
            }
        except Exception as e:
            print(f"Error getting seasonal diseases: {e}")
            return {'likely_diseases': []}

    @staticmethod
    def get_region_specific_recommendations(region: str, disease: str, severity: str) -> Dict:
        """
        Get region-specific treatment recommendations.
        
        Args:
            region: Region name
            disease: Disease name
            severity: Severity level
            
        Returns:
            Dictionary with region-specific recommendations
        """
        recommendations = {
            'pest_management_practices': [],
            'approved_pesticides': [],
            'local_contacts': [],
            'timing_considerations': []
        }
        
        # South Asia specific
        if region == 'South_Asia':
            if disease == 'Blast' or disease == 'Rice Blast':
                recommendations['approved_pesticides'] = [
                    'Tricyclazole (0.6 g/L)',
                    'Hexaconazole (1.25 mL/L)',
                    'Kasugamycin (3 mL/L)'
                ]
                recommendations['timing_considerations'] = [
                    'Spray during monsoon season',
                    'Apply every 7-10 days',
                    'Early morning application best'
                ]
            
            recommendations['pest_management_practices'] = [
                'Remove infected plant parts',
                'Improve field drainage',
                'Use resistant varieties',
                'Maintain proper spacing'
            ]
        
        # Add severity-based recommendations
        if severity == 'severe':
            recommendations['immediate_action'] = [
                'Quarantine affected area',
                'Consult with local agricultural officer',
                'Consider removing severely affected plants',
                'Increase spray frequency'
            ]
        
        return recommendations


class DiseaseRiskAnalyzer:
    """Analyze disease risk based on weather and regional conditions."""
    
    @staticmethod
    def calculate_disease_risk(weather_data: Dict, region: str, crop: str, disease: str) -> Dict:
        """
        Calculate disease risk based on environmental conditions.
        
        Args:
            weather_data: Weather data dictionary
            region: Region name
            crop: Crop name
            disease: Disease name
            
        Returns:
            Dictionary with risk assessment
        """
        risk_score = 0
        risk_factors = []
        recommendations = []
        
        if not weather_data:
            return {'risk_level': 'unknown', 'score': 0, 'factors': [], 'recommendations': []}
        
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        
        # Generic disease-weather relationships
        disease_conditions = {
            'Blight': {'temp_range': (15, 25), 'min_humidity': 80},
            'Rust': {'temp_range': (10, 20), 'min_humidity': 70},
            'Powdery Mildew': {'temp_range': (15, 25), 'min_humidity': 50},
            'Blast': {'temp_range': (25, 30), 'min_humidity': 90},
            'Leaf Blight': {'temp_range': (20, 28), 'min_humidity': 85}
        }
        
        conditions = disease_conditions.get(disease, {'temp_range': (15, 25), 'min_humidity': 70})
        temp_min, temp_max = conditions['temp_range']
        
        # Temperature check
        if temp_min <= temp <= temp_max:
            risk_score += 30
            risk_factors.append(f"Temperature ({temp}°C) is favorable for {disease}")
        
        # Humidity check
        if humidity >= conditions['min_humidity']:
            risk_score += 40
            risk_factors.append(f"High humidity ({humidity}%) increases disease risk")
        
        # Weather conditions
        weather = weather_data.get('weather', '').lower()
        if 'rain' in weather or 'cloud' in weather:
            risk_score += 20
            risk_factors.append("Wet conditions increase disease spread")
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = 'high'
            recommendations = [
                f"High risk for {disease} detected",
                "Increase surveillance and scouting",
                "Prepare preventive spray schedule",
                f"Best spray time: early morning (before {temp}°C peak)"
            ]
        elif risk_score >= 50:
            risk_level = 'moderate'
            recommendations = [
                f"Moderate risk for {disease}",
                "Monitor field closely",
                "Have fungicide available"
            ]
        else:
            risk_level = 'low'
            recommendations = [
                "Continue regular monitoring",
                "Maintain good farm hygiene"
            ]
        
        return {
            'disease': disease,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'weather_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'condition': weather_data.get('weather', 'Unknown')
            }
        }
