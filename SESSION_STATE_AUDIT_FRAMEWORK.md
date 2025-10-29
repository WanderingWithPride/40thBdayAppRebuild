# Session State Audit Framework
**Created:** 2025-10-29
**Purpose:** Systematically identify and fix all session state access issues

## Audit Methodology

### Phase 1: Detection
1. **Find all session state access**: `st.session_state.X`
2. **Categorize access patterns**:
   - Direct access (unsafe): `st.session_state.notes`
   - Safe access with get: `st.session_state.get('notes', [])`
   - Checked access: `if 'notes' in st.session_state:`
3. **Identify initialization points**
4. **Map dependencies**

### Phase 2: Classification
**Risk Levels:**
- 🔴 **CRITICAL**: Direct access without initialization check
- 🟡 **WARNING**: Initialized but could fail on edge cases
- 🟢 **SAFE**: Properly initialized with fallbacks

### Phase 3: Remediation
**Required Patterns:**
1. **Initialization in `init_session_state()`**
2. **Defensive access with `.get()`**
3. **Type validation**
4. **Graceful degradation**

### Phase 4: Prevention
**Enforcement:**
1. Linting rules
2. Code review checklist
3. Automated testing
4. Documentation

---

## Session State Requirements

### Must-Have Patterns

#### Pattern 1: Initialization
```python
def init_session_state():
    """Initialize ALL session state variables"""
    if 'notes' not in st.session_state:
        st.session_state.notes = []
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = load_data_from_github()
    # etc.
```

#### Pattern 2: Defensive Access
```python
# ❌ NEVER DO THIS
reflections = [n for n in st.session_state.notes if n['type'] == 'reflection']

# ✅ ALWAYS DO THIS
reflections = [n for n in st.session_state.get('notes', []) if n.get('type') == 'reflection']
```

#### Pattern 3: Type Validation
```python
# ✅ Validate types
notes = st.session_state.get('notes', [])
if not isinstance(notes, list):
    notes = []
```

---

## Audit Checklist

### Critical Session State Variables
- [ ] `trip_data` - Main data store
- [ ] `notes` - User notes
- [ ] `notifications` - App notifications
- [ ] `packing_progress` - Packing checklist
- [ ] `completed_activities` - Activity tracking
- [ ] `custom_activities` - User-added activities
- [ ] `alcohol_requests` - Alcohol shopping list
- [ ] User preferences
- [ ] Authentication state
- [ ] UI state variables

### Page-by-Page Audit
- [ ] Main page (`app.py` main function)
- [ ] Birthday page (`render_birthday_page()`)
- [ ] Bookings page (`pages/bookings.py`)
- [ ] Schedule/Timeline view
- [ ] Activities section
- [ ] Meals section
- [ ] Packing section
- [ ] Notes section
- [ ] Any modal/expander content

### Common Failure Points
- [ ] List comprehensions on session state
- [ ] Dictionary access without `.get()`
- [ ] Assumptions about data structure
- [ ] Missing initialization on new features
- [ ] Race conditions on data loading

---

## Error Handling Standards

### Minimum Requirements
1. **No exposed AttributeErrors**
2. **No exposed KeyErrors**
3. **Graceful fallbacks**
4. **User-friendly error messages**
5. **Logging for debugging**

### Error Message Template
```python
try:
    # risky operation
except Exception as e:
    # Log technical details
    logger.error(f"Error in function_name: {e}")
    # Show user-friendly message
    st.error("We encountered an issue loading this content. Please refresh the page.")
    # Provide fallback
    return safe_default_value
```

---

## Testing Protocol

### Manual Testing
- [ ] Test each page in clean session
- [ ] Test each page after data operations
- [ ] Test with missing data files
- [ ] Test with corrupted data
- [ ] Test with empty session state

### Automated Testing
```python
def test_session_state_resilience():
    """Test that pages don't crash with empty session state"""
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Try to render each page
    # Should not raise AttributeError or KeyError
```

---

## Findings Template

### Issue Format
```markdown
**Issue ID:** SSA-001
**Severity:** 🔴 CRITICAL
**Location:** app.py:9863
**Code:**
```python
reflections = [n for n in st.session_state.notes if n['type'] == 'reflection']
```
**Problem:** Direct access to `st.session_state.notes` without checking existence
**Impact:** AttributeError crashes birthday page
**Fix:**
```python
reflections = [n for n in st.session_state.get('notes', []) if n.get('type') == 'reflection']
```
**Status:** ❌ Not Fixed
```

---

## Implementation Plan

### Immediate (P0 - Critical)
1. Fix birthday page AttributeError
2. Audit all direct session state access
3. Add defensive patterns to all critical paths

### Short-term (P1 - High)
1. Comprehensive initialization review
2. Add error boundaries around major sections
3. Test all pages

### Medium-term (P2 - Medium)
1. Automated session state validation
2. Linting rules
3. Developer documentation

### Long-term (P3 - Nice to have)
1. Session state management library
2. Type hints and validation
3. Comprehensive test suite
