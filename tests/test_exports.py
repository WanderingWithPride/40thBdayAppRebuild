"""
Tests for export functionality (iCal, PDF, text)
"""

import pytest
import os
import tempfile
from datetime import datetime
from utils.exports import (
    export_to_ical,
    _parse_duration,
    create_simple_text_schedule
)


class TestiCalExport:
    """Test iCalendar export functionality"""

    def test_ical_file_creation(self):
        """Test that iCal file is created"""
        activities = []
        meals = {}

        with tempfile.NamedTemporaryFile(suffix='.ics', delete=False) as f:
            filename = f.name

        try:
            result = export_to_ical(activities, meals, filename=filename)

            # Verify file was created
            assert os.path.exists(filename)
            assert result == filename

            # Verify file has content
            assert os.path.getsize(filename) > 0

        finally:
            # Cleanup
            if os.path.exists(filename):
                os.remove(filename)

    def test_ical_content_structure(self):
        """Test that iCal file has proper structure"""
        activities = [{
            'activity': 'Test Activity',
            'date': '2025-11-09',
            'time': '10:00 AM',
            'duration': '2 hours',
            'status': 'Confirmed',
            'location': {'name': 'Test Location'}
        }]
        meals = {}

        with tempfile.NamedTemporaryFile(suffix='.ics', delete=False) as f:
            filename = f.name

        try:
            export_to_ical(activities, meals, filename=filename)

            # Read file content
            with open(filename, 'rb') as f:
                content = f.read().decode('utf-8')

            # Verify iCal structure
            assert 'BEGIN:VCALENDAR' in content
            assert 'END:VCALENDAR' in content
            assert 'PRODID' in content
            assert 'VERSION:2.0' in content

            # Verify event was added
            assert 'BEGIN:VEVENT' in content
            assert 'Test Activity' in content

        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_parse_duration(self):
        """Test duration parsing for iCal"""
        assert _parse_duration('2 hours') == 2.0
        assert _parse_duration('1.5 hours') == 1.5
        assert _parse_duration('2h 30m') == 2.5
        assert _parse_duration('90 minutes') == 1.5
        assert _parse_duration('') == 2.0  # Default


class TestTextExport:
    """Test text schedule export"""

    def test_text_schedule_creation(self):
        """Test creation of text schedule"""
        activities = [{
            'activity': 'Test Activity',
            'date': '2025-11-09',
            'time': '10:00 AM',
            'location': {'name': 'Test Location', 'phone': '555-1234'}
        }]
        meals = {}

        text = create_simple_text_schedule(activities, meals)

        # Verify structure
        assert '40TH BIRTHDAY TRIP SCHEDULE' in text
        assert 'Florida' in text
        assert 'November 7-12, 2025' in text

        # Verify activity is included
        assert 'Test Activity' in text
        assert '10:00 AM' in text

    def test_text_schedule_emergency_contacts(self):
        """Test that emergency contacts are included"""
        activities = []
        meals = {}

        text = create_simple_text_schedule(activities, meals)

        # Verify emergency contacts section
        assert 'EMERGENCY CONTACTS' in text
        assert 'Ritz-Carlton' in text

    def test_text_schedule_grouping_by_date(self):
        """Test that activities are grouped by date"""
        activities = [
            {
                'activity': 'Morning Activity',
                'date': '2025-11-09',
                'time': '09:00 AM',
                'location': 'Test'
            },
            {
                'activity': 'Afternoon Activity',
                'date': '2025-11-09',
                'time': '02:00 PM',
                'location': 'Test'
            }
        ]
        meals = {}

        text = create_simple_text_schedule(activities, meals)

        # Verify both activities are grouped under same date
        assert 'SUNDAY, NOV 9' in text
        assert 'Morning Activity' in text
        assert 'Afternoon Activity' in text


class TestExportIntegration:
    """Integration tests for export functionality"""

    def test_export_with_meals(self):
        """Test export including meal proposals"""
        activities = []
        meals = {
            'sat_lunch': {
                'status': 'confirmed',
                'final_choice': 'Restaurant A',
                'meal_time': '12:30 PM'
            }
        }

        with tempfile.NamedTemporaryFile(suffix='.ics', delete=False) as f:
            filename = f.name

        try:
            export_to_ical(activities, meals, filename=filename)

            # Verify meal was added to calendar
            with open(filename, 'rb') as f:
                content = f.read().decode('utf-8')

            assert 'Restaurant A' in content or 'Lunch' in content

        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
