"""
Tests for weather alert system
"""

import pytest
from utils.weather_alerts import (
    check_weather_alerts,
    _is_outdoor_activity,
    _is_water_activity,
    _is_extended_outdoor,
    generate_weather_briefing
)


class TestWeatherAlerts:
    """Test weather alert generation"""

    def test_rain_alert(self):
        """Test rain alert generation"""
        activities = [{
            'activity': 'Beach Time',
            'date': '2025-11-09',
            'time': '02:00 PM',
            'category': 'Outdoor'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'rain_chance': 70,
                'high': 80,
                'low': 65
            }]
        }

        alerts = check_weather_alerts(activities, weather)

        # Should generate rain alert
        assert len(alerts) >= 1
        assert any(a['type'] == 'rain' for a in alerts)
        assert any(a['severity'] == 'warning' for a in alerts)

    def test_uv_alert(self):
        """Test UV index alert"""
        activities = [{
            'activity': 'Boat Tour',
            'date': '2025-11-09',
            'time': '10:00 AM',
            'duration': '3 hours',
            'category': 'Outdoor'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'rain_chance': 0,
                'high': 85,
                'low': 70,
                'uv_index': 9
            }]
        }

        alerts = check_weather_alerts(activities, weather)

        # Should generate UV alert
        assert any(a['type'] == 'uv' for a in alerts)

    def test_wind_alert(self):
        """Test wind alert for water activities"""
        activities = [{
            'activity': 'Boat Tour',
            'date': '2025-11-09',
            'time': '10:00 AM'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'rain_chance': 0,
                'high': 75,
                'low': 65,
                'wind_speed': 25
            }]
        }

        alerts = check_weather_alerts(activities, weather)

        # Should generate wind alert
        assert any(a['type'] == 'wind' for a in alerts)

    def test_heat_alert(self):
        """Test high temperature alert"""
        activities = [{
            'activity': 'Photography Session',
            'date': '2025-11-09',
            'time': '02:00 PM',
            'duration': '2 hours',
            'category': 'Outdoor'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'rain_chance': 0,
                'high': 92,
                'low': 75
            }]
        }

        alerts = check_weather_alerts(activities, weather)

        # Should generate heat alert
        assert any(a['type'] == 'heat' for a in alerts)


class TestActivityClassification:
    """Test activity classification functions"""

    def test_outdoor_activity_detection(self):
        """Test detection of outdoor activities"""
        # Beach activity
        assert _is_outdoor_activity({'activity': 'Beach Time'})

        # Boat activity
        assert _is_outdoor_activity({'activity': 'Boat Tour'})

        # Indoor activity
        assert not _is_outdoor_activity({'activity': 'Spa Massage'})

    def test_water_activity_detection(self):
        """Test detection of water activities"""
        # Boat activity
        assert _is_water_activity({'activity': 'Boat Tour'})

        # Swimming
        assert _is_water_activity({'activity': 'Swimming'})

        # Not water activity
        assert not _is_water_activity({'activity': 'Hiking'})

    def test_extended_outdoor_detection(self):
        """Test detection of extended outdoor activities"""
        # Long duration
        assert _is_extended_outdoor({'activity': 'Beach', 'duration': '3 hours'})

        # Short duration
        assert not _is_extended_outdoor({'activity': 'Walk', 'duration': '1 hour'})

        # All-day activity
        assert _is_extended_outdoor({'activity': 'Full Day at Beach'})


class TestWeatherBriefing:
    """Test weather briefing generation"""

    def test_briefing_structure(self):
        """Test that briefing has proper structure"""
        activities = [{
            'activity': 'Beach Time',
            'date': '2025-11-09',
            'time': '02:00 PM'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'condition': 'Partly Cloudy',
                'high': 80,
                'low': 65,
                'rain_chance': 20
            }]
        }

        briefing = generate_weather_briefing(activities, weather, '2025-11-09')

        # Verify structure
        assert 'date' in briefing
        assert 'summary' in briefing
        assert 'alerts' in briefing
        assert 'recommendations' in briefing

        # Verify content
        assert briefing['date'] == '2025-11-09'
        assert 'Partly Cloudy' in briefing['summary']

    def test_recommendations_for_outdoor_activities(self):
        """Test that recommendations are generated for outdoor activities"""
        activities = [{
            'activity': 'Beach Time',
            'date': '2025-11-09',
            'time': '02:00 PM',
            'category': 'Outdoor'
        }]

        weather = {
            'forecast': [{
                'date': '2025-11-09',
                'condition': 'Sunny',
                'high': 88,
                'low': 70,
                'rain_chance': 10,
                'uv_index': 8
            }]
        }

        briefing = generate_weather_briefing(activities, weather, '2025-11-09')

        # Should have recommendations
        assert len(briefing['recommendations']) > 0
        assert briefing['outdoor_count'] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
