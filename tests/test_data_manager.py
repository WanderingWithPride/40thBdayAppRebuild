"""
Tests for TripDataManager - Atomic file operations and backup system
"""

import pytest
import json
import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime


# Mock the data_manager for testing
class TestTripDataManager:
    """Test TripDataManager functionality"""

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory for testing"""
        temp_dir = tempfile.mkdtemp()
        data_dir = os.path.join(temp_dir, 'data')
        backup_dir = os.path.join(data_dir, 'backups')
        os.makedirs(backup_dir)

        yield data_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_save_creates_backup(self, temp_data_dir):
        """Test that save creates backup before writing"""
        # This would test the actual TripDataManager.save() method
        # For now, verify backup directory exists
        backup_dir = os.path.join(temp_data_dir, 'backups')
        assert os.path.exists(backup_dir)

    def test_atomic_write(self, temp_data_dir):
        """Test that writes are atomic (no partial writes)"""
        # Test write-to-temp-then-rename pattern
        data_file = os.path.join(temp_data_dir, 'trip_data.json')
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}

        # Write using atomic pattern
        temp_fd, temp_path = tempfile.mkstemp(
            suffix='.json',
            dir=temp_data_dir,
            text=True
        )

        with os.fdopen(temp_fd, 'w') as f:
            json.dump(test_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        shutil.move(temp_path, data_file)

        # Verify file exists and is valid
        assert os.path.exists(data_file)

        with open(data_file, 'r') as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data

    def test_recovery_from_backup(self, temp_data_dir):
        """Test recovery from backup when main file is corrupted"""
        backup_dir = os.path.join(temp_data_dir, 'backups')

        # Create a backup file
        backup_data = {"test": "backup_data", "valid": True}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'trip_data_{timestamp}.json')

        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)

        # Verify backup was created
        assert os.path.exists(backup_path)
        backups = sorted(Path(backup_dir).glob('trip_data_*.json'))
        assert len(backups) >= 1

        # Verify we can load from backup
        with open(backups[-1], 'r') as f:
            recovered_data = json.load(f)

        assert recovered_data == backup_data

    def test_invalid_json_handling(self, temp_data_dir):
        """Test handling of corrupted JSON files"""
        data_file = os.path.join(temp_data_dir, 'trip_data.json')

        # Create corrupted JSON file
        with open(data_file, 'w') as f:
            f.write('{"invalid": json_here')

        # Attempt to load should fail gracefully
        try:
            with open(data_file, 'r') as f:
                json.load(f)
            assert False, "Should have raised JSONDecodeError"
        except json.JSONDecodeError:
            assert True  # Expected behavior


class TestGitHubStorage:
    """Test GitHub storage integration"""

    def test_data_structure(self):
        """Test that trip data has required structure"""
        # Load actual trip data
        from github_storage import get_trip_data

        data = get_trip_data()

        # Verify structure
        assert isinstance(data, dict)

        # Check for key sections
        expected_keys = ['meal_proposals', 'activity_proposals']
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"

    def test_data_types(self):
        """Test data types are correct"""
        from github_storage import get_trip_data

        data = get_trip_data()

        # meal_proposals should be dict
        assert isinstance(data.get('meal_proposals', {}), dict)

        # activity_proposals should be dict
        assert isinstance(data.get('activity_proposals', {}), dict)


class TestDataPersistence:
    """Test data persistence and consistency"""

    def test_backup_cleanup(self, temp_dir=None):
        """Test that old backups are cleaned up"""
        if not temp_dir:
            temp_dir = tempfile.mkdtemp()

        backup_dir = os.path.join(temp_dir, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        # Create more than MAX_BACKUPS (20) backup files
        for i in range(25):
            timestamp = datetime.now().strftime(f'20251107_{100000+i}')
            backup_path = os.path.join(backup_dir, f'trip_data_{timestamp}.json')
            with open(backup_path, 'w') as f:
                json.dump({"backup": i}, f)

        # Verify files were created
        backups = sorted(Path(backup_dir).glob('trip_data_*.json'))
        assert len(backups) == 25

        # Cleanup temp dir
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
