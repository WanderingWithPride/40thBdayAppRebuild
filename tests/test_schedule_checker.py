"""
Tests for schedule conflict detection
"""

import pytest
from datetime import datetime, timedelta
from utils.schedule_checker import (
    check_schedule_conflicts,
    _parse_duration_to_hours,
    _get_location_name
)


class TestScheduleConflicts:
    """Test schedule conflict detection"""

    def test_no_conflicts(self):
        """Test activities with good spacing"""
        activities = [
            {
                'activity': 'Spa Treatment',
                'date': '2025-11-09',
                'time': '10:00 AM',
                'duration': '2 hours',
                'location': {'name': 'Ritz Spa'}
            },
            {
                'activity': 'Lunch',
                'date': '2025-11-09',
                'time': '01:00 PM',
                'duration': '1.5 hours',
                'location': {'name': 'Beach Restaurant'}
            }
        ]

        conflicts, warnings, suggestions = check_schedule_conflicts(activities)

        assert len(conflicts) == 0
        assert len(warnings) == 0
        assert len(suggestions) >= 1

    def test_overlap_detected(self):
        """Test detection of overlapping activities"""
        activities = [
            {
                'activity': 'Massage',
                'date': '2025-11-09',
                'time': '10:00 AM',
                'duration': '2 hours',
                'location': {'name': 'Spa'}
            },
            {
                'activity': 'Lunch',
                'date': '2025-11-09',
                'time': '11:30 AM',
                'duration': '1.5 hours',
                'location': {'name': 'Restaurant'}
            }
        ]

        conflicts, warnings, suggestions = check_schedule_conflicts(activities)

        # Should detect overlap
        assert len(conflicts) == 1
        assert conflicts[0]['severity'] == 'critical'
        assert 'OVERLAP' in conflicts[0]['message']

    def test_tight_transition_warning(self):
        """Test warning for tight transitions between locations"""
        activities = [
            {
                'activity': 'Beach Time',
                'date': '2025-11-09',
                'time': '02:00 PM',
                'duration': '2 hours',
                'location': {'name': 'Beach'}
            },
            {
                'activity': 'Dinner',
                'date': '2025-11-09',
                'time': '04:15 PM',
                'duration': '2 hours',
                'location': {'name': 'Downtown Restaurant'}
            }
        ]

        conflicts, warnings, suggestions = check_schedule_conflicts(activities)

        # Should warn about tight transition
        assert len(warnings) >= 1
        assert warnings[0]['severity'] == 'warning'
        assert warnings[0]['gap_minutes'] < 30


class TestDurationParsing:
    """Test duration string parsing"""

    def test_parse_hours(self):
        """Test parsing hours"""
        assert _parse_duration_to_hours('2 hours') == 2.0
        assert _parse_duration_to_hours('1.5 hours') == 1.5
        assert _parse_duration_to_hours('3 hour') == 3.0

    def test_parse_minutes(self):
        """Test parsing minutes"""
        assert _parse_duration_to_hours('90 minutes') == 1.5
        assert _parse_duration_to_hours('30 min') == 0.5
        assert _parse_duration_to_hours('120 minutes') == 2.0

    def test_parse_combined(self):
        """Test parsing combined hours and minutes"""
        assert _parse_duration_to_hours('2h 30m') == 2.5
        assert _parse_duration_to_hours('1h 15m') == 1.25

    def test_parse_short_format(self):
        """Test parsing short format"""
        assert _parse_duration_to_hours('2h') == 2.0
        assert _parse_duration_to_hours('3h') == 3.0

    def test_default_duration(self):
        """Test default duration for invalid input"""
        assert _parse_duration_to_hours('invalid') == 2.0
        assert _parse_duration_to_hours('') == 2.0
        assert _parse_duration_to_hours(None) == 2.0


class TestLocationExtraction:
    """Test location name extraction"""

    def test_dict_location(self):
        """Test extracting location from dict"""
        activity = {'location': {'name': 'Ritz-Carlton', 'address': '123 Beach St'}}
        assert _get_location_name(activity) == 'Ritz-Carlton'

    def test_string_location(self):
        """Test extracting location from string"""
        activity = {'location': 'Beach'}
        assert _get_location_name(activity) == 'Beach'

    def test_missing_location(self):
        """Test handling missing location"""
        activity = {}
        assert _get_location_name(activity) == ''

        activity = {'location': {}}
        assert _get_location_name(activity) == ''


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
