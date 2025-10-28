"""
TripDataManager - Safe, atomic file operations with automatic backups

This module handles all trip data I/O with safety guarantees:
- Atomic writes (no partial writes that corrupt data)
- Automatic backups before every write
- Recovery from corrupted files
- Audit trail of all changes
"""

import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path


class TripDataManager:
    """Handles all trip data I/O with safety guarantees"""

    DATA_FILE = 'data/trip_data.json'
    BACKUP_DIR = 'data/backups'
    MAX_BACKUPS = 20  # Keep last 20 backups

    @classmethod
    def load(cls):
        """Load trip data with error recovery

        Returns:
            dict: Trip data

        Raises:
            Exception: If data is unrecoverable
        """
        try:
            with open(cls.DATA_FILE, 'r') as f:
                data = json.load(f)
            return data

        except json.JSONDecodeError as e:
            print(f"❌ CRITICAL: {cls.DATA_FILE} is corrupted!")
            print(f"Error: {e}")

            # Try to recover from most recent backup
            backup = cls._get_most_recent_backup()
            if backup:
                print(f"🔄 Attempting recovery from backup: {backup}")
                with open(backup, 'r') as f:
                    data = json.load(f)
                print(f"✅ Successfully recovered from backup!")

                # Save recovered data
                cls.save(data, reason="Recovered from corrupted file")
                return data
            else:
                raise Exception("No backups available. Data unrecoverable.")

        except FileNotFoundError:
            print(f"⚠️ {cls.DATA_FILE} not found. Creating new file.")
            default_data = cls._create_default_data()
            cls.save(default_data, reason="Created new data file")
            return default_data

    @classmethod
    def save(cls, data, reason=""):
        """Save trip data atomically with automatic backup

        Args:
            data (dict): Trip data to save
            reason (str): Reason for this save (for audit trail)
        """

        # 1. Ensure backup directory exists
        Path(cls.BACKUP_DIR).mkdir(parents=True, exist_ok=True)

        # 2. Create backup of current file BEFORE writing
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if os.path.exists(cls.DATA_FILE):
            backup_path = f'{cls.BACKUP_DIR}/trip_data_{timestamp}.json'
            shutil.copy2(cls.DATA_FILE, backup_path)
            print(f"💾 Backup created: {backup_path}")

        # 3. Write to temporary file first (safer than direct write)
        temp_fd, temp_path = tempfile.mkstemp(
            suffix='.json',
            prefix='trip_data_tmp_',
            dir='data',
            text=True
        )

        try:
            # Write data to temp file
            with os.fdopen(temp_fd, 'w') as temp_file:
                json.dump(data, temp_file, indent=2)
                temp_file.flush()
                os.fsync(temp_file.fileno())  # Force write to disk (prevents corruption)

            # 4. Atomic rename (this operation is atomic on Unix/Linux/Mac)
            # If system crashes during rename, either old or new file exists - never half-written
            shutil.move(temp_path, cls.DATA_FILE)

            # 5. Log the change for audit trail
            cls._log_change(reason, timestamp)

            # 6. Cleanup old backups (keep only last N)
            cls._cleanup_old_backups()

            print(f"✅ Data saved successfully. Reason: {reason or 'No reason specified'}")

        except Exception as e:
            # If anything fails, clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    @classmethod
    def _cleanup_old_backups(cls):
        """Keep only last N backups, delete older ones"""
        backups = sorted(Path(cls.BACKUP_DIR).glob('trip_data_*.json'))

        if len(backups) > cls.MAX_BACKUPS:
            for old_backup in backups[:-cls.MAX_BACKUPS]:
                old_backup.unlink()
                print(f"🗑️ Deleted old backup: {old_backup.name}")

    @classmethod
    def _get_most_recent_backup(cls):
        """Get path to most recent backup file

        Returns:
            Path or None: Most recent backup path
        """
        backups = sorted(Path(cls.BACKUP_DIR).glob('trip_data_*.json'))
        return backups[-1] if backups else None

    @classmethod
    def _log_change(cls, reason, timestamp):
        """Log data changes for audit trail

        Args:
            reason (str): Reason for change
            timestamp (str): Timestamp of change
        """
        log_file = 'data/change_log.txt'
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} | {reason}\n")

    @classmethod
    def _create_default_data(cls):
        """Create default data structure if file doesn't exist

        Returns:
            dict: Default data structure
        """
        return {
            "meal_proposals": {},
            "activity_proposals": {},
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

    @classmethod
    def list_backups(cls):
        """List all available backups with timestamps

        Returns:
            list: List of backup info dicts
        """
        backups = sorted(Path(cls.BACKUP_DIR).glob('trip_data_*.json'))
        return [
            {
                'path': str(backup),
                'filename': backup.name,
                'timestamp': backup.stem.replace('trip_data_', ''),
                'size': backup.stat().st_size,
                'size_mb': round(backup.stat().st_size / 1024 / 1024, 2)
            }
            for backup in backups
        ]

    @classmethod
    def restore_from_backup(cls, backup_path):
        """Restore data from specific backup

        Args:
            backup_path (str): Path to backup file

        Raises:
            FileNotFoundError: If backup doesn't exist
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Create backup of current state before restoring
        current_data = cls.load()
        cls.save(current_data, reason="Pre-restoration backup")

        # Copy backup to main file
        shutil.copy2(backup_path, cls.DATA_FILE)
        print(f"✅ Restored from backup: {backup_path}")

        # Verify restored data is valid JSON
        restored_data = cls.load()
        return restored_data
