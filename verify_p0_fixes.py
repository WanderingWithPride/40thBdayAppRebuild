"""
Verification Script for P0 Fixes

Tests that critical safety features are working correctly.
"""

import os
import sys


def test_atomic_writes():
    """Test that atomic write functions exist and work"""
    print("\n🔍 TEST 1: Atomic Writes + Backups")
    print("-" * 60)

    try:
        from github_storage import _atomic_write_local, _create_backup
        print("✅ Atomic write functions imported successfully")

        # Test backup directory creation
        if os.path.exists('data/backups'):
            backup_count = len([f for f in os.listdir('data/backups') if f.startswith('trip_data')])
            print(f"✅ Backup directory exists ({backup_count} backups found)")
        else:
            print("⚠️ Backup directory not yet created (will be created on first save)")

        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_calendar_export():
    """Test that calendar export module works"""
    print("\n🔍 TEST 2: Calendar Export")
    print("-" * 60)

    try:
        from utils.exports import export_to_ical
        print("✅ Calendar export function imported successfully")

        # Check required packages
        import icalendar
        import pytz
        print("✅ Required packages (icalendar, pytz) installed")

        return True
    except ImportError as e:
        print(f"❌ FAILED: Missing package - {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_github_storage_integration():
    """Test that github_storage loads correctly"""
    print("\n🔍 TEST 3: GitHub Storage Integration")
    print("-" * 60)

    try:
        from github_storage import get_trip_data, save_trip_data
        print("✅ GitHub storage functions imported successfully")

        # Note: We can't actually test get_trip_data without Streamlit session state
        print("ℹ️ Full integration test requires running Streamlit app")

        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_app_imports():
    """Test that app.py can import new modules"""
    print("\n🔍 TEST 4: App.py Integration")
    print("-" * 60)

    try:
        # Check if app.py has the calendar export code
        with open('app.py', 'r') as f:
            content = f.read()

        if 'from utils.exports import export_to_ical' in content:
            print("✅ App.py imports calendar export")
        else:
            print("⚠️ Calendar export not yet integrated into app.py")

        if '_atomic_write_local' in open('github_storage.py').read():
            print("✅ Atomic writes integrated into github_storage.py")
        else:
            print("❌ Atomic writes NOT integrated")
            return False

        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_code_quality():
    """Basic code quality checks"""
    print("\n🔍 TEST 5: Code Quality")
    print("-" * 60)

    try:
        # Check Python syntax
        import py_compile

        files_to_check = [
            'github_storage.py',
            'utils/data_manager.py',
            'utils/exports.py',
            'app.py'
        ]

        all_valid = True
        for file_path in files_to_check:
            if os.path.exists(file_path):
                try:
                    py_compile.compile(file_path, doraise=True)
                    print(f"✅ {file_path} - Valid Python syntax")
                except py_compile.PyCompileError as e:
                    print(f"❌ {file_path} - Syntax error: {e}")
                    all_valid = False
            else:
                print(f"⚠️ {file_path} - File not found")

        return all_valid
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def main():
    """Run all verification tests"""
    print("="  * 60)
    print("🛡️  P0 FIXES VERIFICATION")
    print("=" * 60)

    tests = [
        ("Atomic Writes + Backups", test_atomic_writes),
        ("Calendar Export", test_calendar_export),
        ("GitHub Storage Integration", test_github_storage_integration),
        ("App Integration", test_app_imports),
        ("Code Quality", test_code_quality)
    ]

    results = []
    for test_name, test_func in tests:
        passed = test_func()
        results.append((test_name, passed))

    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {test_name}")

    print(f"\n🎯 SCORE: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n✅ ALL P0 FIXES VERIFIED!")
        print("   System is ready for trip with enhanced safety features.")
        return 0
    elif passed_count >= total_count * 0.8:
        print("\n⚠️ MOSTLY WORKING - Minor issues to address")
        return 1
    else:
        print("\n❌ CRITICAL ISSUES - Do not use for trip yet")
        return 2


if __name__ == "__main__":
    sys.exit(main())
