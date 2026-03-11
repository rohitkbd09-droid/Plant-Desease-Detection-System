"""
Crop calendar management with seasonal schedules and recommendations.
"""

import json
from typing import Dict, List
from datetime import datetime, timedelta


# Global crop calendar database
CROP_CALENDAR_DB = {
    'Rice': {
        'North_India': {
            'season': 'Kharif',
            'events': [
                {'month': 5, 'event': 'Field Preparation', 'duration': 15, 'details': 'Ploughing and puddling'},
                {'month': 5, 'event': 'Sowing', 'duration': 20, 'details': 'Transplanting seedlings'},
                {'month': 6, 'event': 'Weeding', 'duration': 30, 'details': 'Remove weeds'},
                {'month': 6, 'event': 'First Fertilizer', 'duration': 1, 'details': 'Apply NPK 20:20:20 at 50kg/ha'},
                {'month': 7, 'event': 'Second Fertilizer', 'duration': 1, 'details': 'Apply Urea 50kg/ha'},
                {'month': 8, 'event': 'Pest Monitoring', 'duration': 30, 'details': 'Check for stem borer, leaf roller'},
                {'month': 9, 'event': 'Disease Surveillance', 'duration': 30, 'details': 'Monitor for blast, sheath blight'},
                {'month': 10, 'event': 'Harvesting Preparation', 'duration': 15, 'details': 'Reduce irrigation'},
                {'month': 11, 'event': 'Harvesting', 'duration': 10, 'details': 'Harvest when grain is mature'}
            ]
        },
        'South_India': {
            'season': 'Kharif and Rabi',
            'events': [
                {'month': 7, 'event': 'Kharif Sowing', 'duration': 20, 'details': 'Transplant during monsoon'},
                {'month': 10, 'event': 'Kharif Harvest', 'duration': 10, 'details': 'Harvest in October-November'},
                {'month': 1, 'event': 'Rabi Sowing', 'duration': 20, 'details': 'Direct sowing or transplanting'},
                {'month': 4, 'event': 'Rabi Harvest', 'duration': 10, 'details': 'Harvest in April-May'}
            ]
        }
    },
    'Wheat': {
        'North_India': {
            'season': 'Rabi',
            'events': [
                {'month': 10, 'event': 'Land Preparation', 'duration': 15, 'details': '2-3 ploughings'},
                {'month': 11, 'event': 'Sowing', 'duration': 30, 'details': 'Seed rate: 100kg/ha'},
                {'month': 12, 'event': 'First Irrigation', 'duration': 1, 'details': 'Crown root stage'},
                {'month': 12, 'event': 'First Fertilizer', 'duration': 1, 'details': 'Apply NPK 100:50:40 kg/ha'},
                {'month': 1, 'event': 'Second Irrigation', 'duration': 1, 'details': 'Tillering stage'},
                {'month': 2, 'event': 'Third Irrigation', 'duration': 1, 'details': 'Boot stage'},
                {'month': 3, 'event': 'Disease Surveillance', 'duration': 30, 'details': 'Monitor for rust'},
                {'month': 4, 'event': 'Fourth Irrigation', 'duration': 1, 'details': 'Grain filling stage'},
                {'month': 5, 'event': 'Harvesting', 'duration': 10, 'details': 'When grain becomes hard'}
            ]
        }
    },
    'Cotton': {
        'Global': {
            'season': 'Annual',
            'events': [
                {'month': 3, 'event': 'Soil Preparation', 'duration': 15, 'details': 'Deep ploughing'},
                {'month': 4, 'event': 'Sowing', 'duration': 30, 'details': 'Seed rate: 20kg/ha'},
                {'month': 5, 'event': 'First Weeding', 'duration': 7, 'details': 'Manual or mechanical'},
                {'month': 6, 'event': 'Second Weeding', 'duration': 7, 'details': 'Manual or mechanical'},
                {'month': 7, 'event': 'Fertilizer Application', 'duration': 1, 'details': 'Apply NPK 150:75:75'},
                {'month': 8, 'event': 'Pest Surveillance', 'duration': 30, 'details': 'Monitor for bollworms'},
                {'month': 9, 'event': 'Irrigation', 'duration': 1, 'details': 'Last irrigation'},
                {'month': 11, 'event': 'Harvesting', 'duration': 30, 'details': 'Mechanical or manual picking'}
            ]
        }
    }
}


class CropCalendarManager:
    """Manage crop calendars and farming schedules."""
    
    @staticmethod
    def get_crop_calendar(crop_name: str, region: str = None) -> Dict:
        """
        Get crop calendar for specific crop and region.
        
        Args:
            crop_name: Name of crop
            region: Region/area for crop cultivation
            
        Returns:
            Dictionary with crop calendar events
        """
        crop_data = CROP_CALENDAR_DB.get(crop_name, {})
        
        if not crop_data:
            return {'error': f'No calendar found for {crop_name}'}
        
        # Try to get region-specific calendar
        if region and region in crop_data:
            calendar = crop_data[region]
        else:
            # Get global or default calendar
            calendar = crop_data.get('Global', crop_data.get(list(crop_data.keys())[0], {}))
        
        return {
            'crop_name': crop_name,
            'region': region or 'Default',
            'season': calendar.get('season', 'Annual'),
            'events': calendar.get('events', [])
        }
    
    @staticmethod
    def get_upcoming_tasks(crop_name: str, current_month: int, region: str = None, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming farming tasks.
        
        Args:
            crop_name: Crop name
            current_month: Current month (1-12)
            region: Region
            days_ahead: How many days ahead to look
            
        Returns:
            List of upcoming tasks sorted by date
        """
        calendar = CropCalendarManager.get_crop_calendar(crop_name, region)
        events = calendar.get('events', [])
        
        # Calculate relevant months
        current_year = datetime.now().year
        upcoming_tasks = []
        
        for event in events:
            event_month = event.get('month', current_month)
            
            # Handle year wraparound for Rabi crops
            if event_month < current_month:
                event_year = current_year + 1
            else:
                event_year = current_year
            
            # Calculate task date (15th of the month by default)
            task_date = datetime(event_year, event_month, 15)
            days_until = (task_date - datetime.now()).days
            
            if 0 <= days_until <= days_ahead:
                upcoming_tasks.append({
                    'event_type': event['event'],
                    'scheduled_date': task_date.isoformat(),
                    'days_until': days_until,
                    'duration_days': event.get('duration', 1),
                    'description': event.get('details', ''),
                    'priority': 'high' if days_until <= 7 else 'medium' if days_until <= 14 else 'low'
                })
        
        return sorted(upcoming_tasks, key=lambda x: x['days_until'])
    
    @staticmethod
    def get_weather_based_recommendations(crop_name: str, month: int, weather: Dict) -> Dict:
        """
        Get weather-based farming recommendations.
        
        Args:
            crop_name: Crop name
            month: Current month
            weather: Weather data dictionary
            
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'irrigation_advice': '',
            'pesticide_timing': '',
            'fertilizer_timing': '',
            'activity_recommendations': []
        }
        
        temp = weather.get('temperature', 20)
        humidity = weather.get('humidity', 60)
        weather_cond = weather.get('weather', 'clear').lower()
        rainfall = weather.get('rainfall_mm', 0)
        
        # Irrigation recommendations
        if humidity < 40:
            recommendations['irrigation_advice'] = 'Low humidity detected. Increase irrigation frequency.'
        elif humidity > 80 and rainfall > 10:
            recommendations['irrigation_advice'] = 'High humidity and rainfall. Reduce irrigation to prevent waterlogging.'
        else:
            recommendations['irrigation_advice'] = 'Current humidity is favorable. Maintain normal irrigation schedule.'
        
        # Pesticide timing
        if temp > 25 and humidity > 70:
            recommendations['pesticide_timing'] = 'Conditions are favorable for fungal diseases. Consider preventive spray in early morning.'
        elif 'rain' in weather_cond:
            recommendations['pesticide_timing'] = 'Rain detected. Reschedule spray activities. Reapply after rain stops.'
        else:
            recommendations['pesticide_timing'] = 'Conditions suitable for pesticide application. Apply in late afternoon.'
        
        # Fertilizer timing
        if rainfall > 20:
            recommendations['fertilizer_timing'] = 'Adequate rainfall detected. Proceed with fertilizer application.'
        elif humidity > 60:
            recommendations['fertilizer_timing'] = 'Good moisture. Optimal time for granular fertilizer application.'
        else:
            recommendations['fertilizer_timing'] = 'Low moisture. Wait for irrigation or rainfall before applying fertilizer.'
        
        # Activity recommendations
        if temp < 15:
            recommendations['activity_recommendations'].append('Low temperature. Reduce pest activity. Monitor for cold-related stress.')
        elif temp > 35:
            recommendations['activity_recommendations'].append('High temperature. Increase irrigation frequency. Watch for heat stress.')
        
        if 'clear' in weather_cond or 'sunny' in weather_cond:
            recommendations['activity_recommendations'].append('Clear weather. Good time for field operations.')
        
        return recommendations
    
    @staticmethod
    def get_fertilizer_schedule(crop_name: str, field_area_hectares: float) -> List[Dict]:
        """
        Get fertilizer application schedule.
        
        Args:
            crop_name: Crop name
            field_area_hectares: Field area in hectares
            
        Returns:
            List of fertilizer applications with quantities
        """
        schedules = {
            'Rice': [
                {
                    'stage': 'Transplanting',
                    'fertilizer': 'NPK 20:20:20',
                    'quantity_kg': 50 * field_area_hectares,
                    'timing': 'At transplanting'
                },
                {
                    'stage': 'Tillering',
                    'fertilizer': 'Urea',
                    'quantity_kg': 50 * field_area_hectares,
                    'timing': '30-40 days after transplanting'
                },
                {
                    'stage': 'Panicle initiation',
                    'fertilizer': 'Urea',
                    'quantity_kg': 40 * field_area_hectares,
                    'timing': 'At panicle initiation stage'
                }
            ],
            'Wheat': [
                {
                    'stage': 'At sowing',
                    'fertilizer': 'DAP',
                    'quantity_kg': 80 * field_area_hectares,
                    'timing': 'During seed bed preparation'
                },
                {
                    'stage': 'Crown root',
                    'fertilizer': 'Urea',
                    'quantity_kg': 50 * field_area_hectares,
                    'timing': '30-40 days after sowing'
                },
                {
                    'stage': 'Tillering',
                    'fertilizer': 'Urea',
                    'quantity_kg': 50 * field_area_hectares,
                    'timing': '50-60 days after sowing'
                },
                {
                    'stage': 'Boot stage',
                    'fertilizer': 'Potassium',
                    'quantity_kg': 30 * field_area_hectares,
                    'timing': 'At boot stage'
                }
            ]
        }
        
        return schedules.get(crop_name, [])
    
    @staticmethod
    def get_irrigation_schedule(crop_name: str, region: str = None) -> Dict:
        """
        Get irrigation schedule for crop.
        
        Args:
            crop_name: Crop name
            region: Region
            
        Returns:
            Dictionary with irrigation details
        """
        schedules = {
            'Rice': {
                'total_irrigations': '7-10',
                'water_requirement_mm': '1000-1500',
                'schedule': [
                    {'stage': 'Puddling', 'depth_cm': 7.5, 'timing': 'Before transplanting'},
                    {'stage': 'Maintenance', 'depth_cm': 5, 'timing': 'Till panicle emergence'},
                    {'stage': 'Reproduction', 'depth_cm': 5, 'timing': 'During flowering'},
                    {'stage': 'Maturation', 'depth_cm': 2.5, 'timing': 'Last irrigation 15 days before harvest'}
                ]
            },
            'Wheat': {
                'total_irrigations': '4-6',
                'water_requirement_mm': '600-900',
                'schedule': [
                    {'stage': 'Crown root', 'depth_cm': 5, 'timing': '20-25 days after sowing'},
                    {'stage': 'Tillering', 'depth_cm': 5, 'timing': '45-50 days after sowing'},
                    {'stage': 'Boot stage', 'depth_cm': 5, 'timing': '70-75 days after sowing'},
                    {'stage': 'Grain filling', 'depth_cm': 5, 'timing': '90-95 days after sowing'}
                ]
            },
            'Cotton': {
                'total_irrigations': '10-15',
                'water_requirement_mm': '600-1200',
                'schedule': [
                    {'stage': 'Establishment', 'depth_cm': 5, 'timing': '20-25 days after sowing'},
                    {'stage': 'Vegetative', 'depth_cm': 5, 'timing': 'Every 10-15 days'},
                    {'stage': 'Flowering', 'depth_cm': 5, 'timing': 'Every 7-10 days'},
                    {'stage': 'Boll maturation', 'depth_cm': 5, 'timing': 'Every 15-20 days'}
                ]
            }
        }
        
        return schedules.get(crop_name, {'schedule': []})
