"""
Tests for data validation system
"""

import pytest
from utils.data_validator import (
    validate_activities,
    validate_meal_proposals,
    validate_activity_proposals,
    validate_trip_data,
    generate_validation_report
)


class TestActivityValidation:
    """Test activity data validation"""

    def test_valid_activity(self):
        """Test validation of properly structured activity"""
        activities = [{
            'activity': 'Spa Treatment',
            'date': '2025-11-09',
            'time': '10:00 AM',
            'duration': '2 hours',
            'location': {'name': 'Ritz Spa'},
            'category': 'Spa',
            'status': 'Confirmed',
            'cost': 200
        }]

        errors, warnings = validate_activities(activities)

        assert len(errors) == 0

    def test_missing_required_fields(self):
        """Test detection of missing required fields"""
        activities = [{
            'activity': 'Incomplete Activity'
            # Missing: date, time, duration, location, category, status
        }]

        errors, warnings = validate_activities(activities)

        # Should have errors for missing fields
        assert len(errors) > 0
        assert any(e['type'] == 'missing_field' for e in errors)

    def test_invalid_date_format(self):
        """Test detection of invalid date format"""
        activities = [{
            'activity': 'Test',
            'date': '11/09/2025',  # Wrong format
            'time': '10:00 AM',
            'duration': '2 hours',
            'location': 'Spa',
            'category': 'Spa',
            'status': 'Confirmed'
        }]

        errors, warnings = validate_activities(activities)

        # Should have error for invalid date
        assert any(e['type'] == 'invalid_date' for e in errors)

    def test_invalid_time_format(self):
        """Test detection of invalid time format"""
        activities = [{
            'activity': 'Test',
            'date': '2025-11-09',
            'time': '10:00',  # Missing AM/PM
            'duration': '2 hours',
            'location': 'Spa',
            'category': 'Spa',
            'status': 'Confirmed'
        }]

        errors, warnings = validate_activities(activities)

        # Should have error for invalid time
        assert any(e['type'] == 'invalid_time' for e in errors)

    def test_location_validation(self):
        """Test location structure validation"""
        # Missing location name
        activities = [{
            'activity': 'Test',
            'date': '2025-11-09',
            'time': '10:00 AM',
            'duration': '2 hours',
            'location': {'address': '123 Main St'},  # No name
            'category': 'Spa',
            'status': 'Confirmed'
        }]

        errors, warnings = validate_activities(activities)

        # Should have warning for incomplete location
        assert any(w['type'] == 'incomplete_location' for w in warnings)


class TestMealProposalValidation:
    """Test meal proposal validation"""

    def test_valid_meal_proposal(self):
        """Test validation of properly structured meal proposal"""
        proposals = {
            'sat_lunch': {
                'restaurant_options': [
                    {'name': 'Restaurant A', 'cuisine': 'Italian'},
                    {'name': 'Restaurant B', 'cuisine': 'Seafood'}
                ],
                'meal_time': '12:30 PM',
                'status': 'proposed'
            }
        }

        errors, warnings = validate_meal_proposals(proposals)

        assert len(errors) == 0

    def test_missing_proposal_fields(self):
        """Test detection of missing proposal fields"""
        proposals = {
            'sat_lunch': {
                'restaurant_options': []
                # Missing: meal_time, status
            }
        }

        errors, warnings = validate_meal_proposals(proposals)

        # Should have errors for missing fields
        assert len(errors) > 0

    def test_empty_restaurant_options(self):
        """Test warning for empty restaurant options"""
        proposals = {
            'sat_lunch': {
                'restaurant_options': [],
                'meal_time': '12:30 PM',
                'status': 'proposed'
            }
        }

        errors, warnings = validate_meal_proposals(proposals)

        # Should have warning for empty options
        assert any(w['type'] == 'empty_options' for w in warnings)

    def test_confirmed_without_final_choice(self):
        """Test warning for confirmed meal without final choice"""
        proposals = {
            'sat_lunch': {
                'restaurant_options': [
                    {'name': 'Restaurant A'}
                ],
                'meal_time': '12:30 PM',
                'status': 'confirmed'
                # Missing: final_choice
            }
        }

        errors, warnings = validate_meal_proposals(proposals)

        # Should have warning for missing final_choice
        assert any(w['type'] == 'missing_final_choice' for w in warnings)


class TestValidationReport:
    """Test validation report generation"""

    def test_all_valid_report(self):
        """Test report generation when everything is valid"""
        is_valid = True
        errors = []
        warnings = []

        report = generate_validation_report(is_valid, errors, warnings)

        assert "✅ ALL CHECKS PASSED" in report

    def test_errors_report(self):
        """Test report with errors"""
        is_valid = False
        errors = [
            {
                'message': 'Test error',
                'fix': 'Fix this way'
            }
        ]
        warnings = []

        report = generate_validation_report(is_valid, errors, warnings)

        assert "⛔ ERRORS" in report
        assert "Test error" in report
        assert "Fix this way" in report

    def test_warnings_report(self):
        """Test report with warnings"""
        is_valid = True
        errors = []
        warnings = [
            {
                'message': 'Test warning',
                'fix': 'Suggestion here'
            }
        ]

        report = generate_validation_report(is_valid, errors, warnings)

        assert "⚠️  WARNINGS" in report
        assert "Test warning" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
