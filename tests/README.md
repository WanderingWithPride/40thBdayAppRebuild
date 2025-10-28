# Test Suite

Comprehensive test coverage for the 40th Birthday Trip Planner.

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_data_manager.py -v
```

### Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Files

### test_data_manager.py
Tests for atomic file operations, backups, and data persistence:
- Atomic writes (no partial writes)
- Backup creation before saves
- Recovery from corrupted files
- Backup cleanup (keeping last 20)
- JSON validation

### test_schedule_checker.py
Tests for schedule conflict detection:
- Overlap detection (hard conflicts)
- Tight transition warnings
- Good buffer suggestions
- Duration string parsing
- Location extraction

### test_data_validator.py
Tests for data validation system:
- Activity structure validation
- Required field checking
- Date/time format validation
- Meal proposal validation
- Activity proposal validation
- Validation report generation

### test_exports.py
Tests for export functionality:
- iCalendar (.ics) file creation
- iCal structure and content
- Text schedule generation
- Emergency contacts inclusion
- Date grouping
- Meal integration

### test_weather_alerts.py
Tests for weather alert system:
- Rain alerts (>30% chance)
- UV index warnings (≥8)
- Wind alerts for water activities (>15 mph)
- Heat advisories (>85°F)
- Activity classification (outdoor/water/extended)
- Daily weather briefing

## Coverage Goals

Target: 80%+ code coverage

Current coverage areas:
- ✅ Data management (atomic writes, backups)
- ✅ Schedule conflict detection
- ✅ Data validation
- ✅ Export functionality
- ✅ Weather alerts

## Adding New Tests

When adding new features, add corresponding tests:

1. Create test file: `tests/test_<feature>.py`
2. Import pytest: `import pytest`
3. Create test class: `class Test<Feature>:`
4. Write test methods: `def test_<scenario>(self):`
5. Use assertions: `assert actual == expected`
6. Run tests: `pytest tests/ -v`

## Test Best Practices

- **Arrange-Act-Assert**: Set up data, execute function, verify result
- **Test one thing**: Each test should verify one specific behavior
- **Use fixtures**: For repeated setup (see `@pytest.fixture`)
- **Meaningful names**: `test_overlap_detected` not `test_1`
- **Edge cases**: Test boundary conditions and error cases
- **Clean up**: Remove temp files, reset state

## Example Test

```python
def test_conflict_detection():
    """Test that overlapping activities are detected"""
    # Arrange
    activities = [
        {'activity': 'Massage', 'date': '2025-11-09', 'time': '10:00 AM', 'duration': '2 hours'},
        {'activity': 'Lunch', 'date': '2025-11-09', 'time': '11:30 AM', 'duration': '1 hour'}
    ]

    # Act
    conflicts, warnings, suggestions = check_schedule_conflicts(activities)

    # Assert
    assert len(conflicts) == 1
    assert conflicts[0]['severity'] == 'critical'
```

## Continuous Integration

These tests can be integrated with CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

## Troubleshooting

**Import errors:**
```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

**Fixture errors:**
- Check that fixtures are properly decorated with `@pytest.fixture`
- Verify fixture is in same file or in `conftest.py`

**Test discovery:**
- Files must start with `test_`
- Functions must start with `test_`
- Classes must start with `Test`
