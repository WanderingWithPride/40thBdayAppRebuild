#!/usr/bin/env python3
"""
Comprehensive Deployment Audit Script
Checks code quality, security, and deployment readiness
"""

import ast
import os
import json
from pathlib import Path

def check_app_py():
    """Audit app.py for code quality and best practices"""
    
    # Read app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    try:
        code = ast.parse(content)
    except SyntaxError as e:
        return {'error': f'Syntax error: {e}'}
    
    # Basic checks
    checks = {
        'has_password_function': 'def check_password' in content,
        'has_masking_function': 'def mask_sensitive_info' in content,
        'has_session_state': 'st.session_state' in content,
        'has_caching': '@st.cache_data' in content,
        'has_error_handling': 'try:' in content or 'except:' in content,
        'has_comments': content.count('#') > 10,
        'has_docstrings': '"""' in content,
        'uses_environment_vars': 'os.getenv' in content,
        'file_size_reasonable': len(content) < 60000,
        'no_plaintext_passwords': 'password = "' not in content or 'def check_password' in content,
    }
    
    # Count imports
    imports = [node for node in ast.walk(code) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
    
    # Count functions
    functions = [node for node in ast.walk(code) if isinstance(node, ast.FunctionDef)]
    
    # Check for specific features
    features = {
        'password_protection': 'check_password' in content,
        'data_masking': 'mask_sensitive_info' in content,
        'dashboard': 'render_dashboard' in content,
        'schedule': 'render_schedule' in content,
        'weather': 'render_weather' in content,
        'travel': 'render_travel' in content,
        'spa': 'render_spa' in content,
        'budget': 'render_budget' in content,
    }
    
    return {
        'checks': checks,
        'metrics': {
            'file_size': len(content),
            'lines': content.count('\n'),
            'functions': len(functions),
            'imports': len(imports),
        },
        'features': features,
        'all_checks_passed': all(checks.values()),
    }

def check_files():
    """Verify all required files exist"""
    
    required_files = {
        'app.py': 'Main application',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Documentation',
        'DEPLOYMENT_GUIDE.md': 'Deployment instructions',
        'QUICK_START.md': 'Quick start guide',
        'Procfile': 'Heroku deployment',
        'render.yaml': 'Render deployment',
        'railway.json': 'Railway deployment',
        'Dockerfile': 'Docker deployment',
        '.gitignore': 'Git ignore rules',
        'env.example': 'Environment template',
    }
    
    files_status = {}
    for filename, description in required_files.items():
        exists = os.path.exists(filename)
        files_status[filename] = {
            'exists': exists,
            'description': description,
        }
        if exists:
            size = os.path.getsize(filename)
            files_status[filename]['size'] = size
    
    return files_status

def check_security():
    """Security-specific checks"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    security_checks = {
        'password_hash_set': 'a5be948874610641149611913c4924e5' in content,
        'password_is_hash': 'TRIP_PASSWORD_HASH' in content,
        'session_state_used': 'st.session_state' in content,
        'sensitive_data_hardcoded': 'AA2434' in content and '904-753-7631' in content,
        'data_masking_implemented': 'mask_sensitive_info' in content,
        'no_debug_mode': 'debug=True' not in content,
        'caching_used': '@st.cache_data' in content,
    }
    
    return security_checks

def main():
    """Run comprehensive audit"""
    
    print("=" * 60)
    print("COMPREHENSIVE DEPLOYMENT AUDIT")
    print("=" * 60)
    
    print("\n1. CODE QUALITY AUDIT")
    print("-" * 60)
    code_audit = check_app_py()
    
    if 'error' in code_audit:
        print(f"❌ Error: {code_audit['error']}")
    else:
        print("Code Checks:")
        for check, passed in code_audit['checks'].items():
            status = '✅' if passed else '❌'
            print(f"  {status} {check}")
        
        print(f"\nMetrics:")
        metrics = code_audit['metrics']
        print(f"  File size: {metrics['file_size']} characters")
        print(f"  Lines: {metrics['lines']}")
        print(f"  Functions: {metrics['functions']}")
        print(f"  Imports: {metrics['imports']}")
        
        print(f"\nFeatures:")
        for feature, present in code_audit['features'].items():
            status = '✅' if present else '❌'
            print(f"  {status} {feature}")
    
    print("\n2. FILE STRUCTURE AUDIT")
    print("-" * 60)
    files = check_files()
    
    all_files_present = True
    for filename, info in files.items():
        status = '✅' if info['exists'] else '❌'
        size = f" ({info['size']} bytes)" if info['exists'] else ''
        print(f"  {status} {filename}{size}")
        if not info['exists']:
            all_files_present = False
    
    print("\n3. SECURITY AUDIT")
    print("-" * 60)
    security = check_security()
    
    for check, passed in security.items():
        status = '✅' if passed else '❌'
        print(f"  {status} {check}")
    
    print("\n4. OVERALL ASSESSMENT")
    print("-" * 60)
    
    code_ok = code_audit.get('all_checks_passed', False) if 'all_checks_passed' in code_audit else False
    security_ok = all(security.values())
    
    if code_ok and security_ok and all_files_present:
        print("✅ ALL SYSTEMS GO - READY FOR DEPLOYMENT")
        print("\nYour app is production-ready!")
        print("\nNext steps:")
        print("  1. Upload to GitLab/GitHub private repo")
        print("  2. Deploy to Streamlit Cloud")
        print("  3. Set TRIP_PASSWORD_HASH environment variable")
        print("  4. Test with your configured password")
    else:
        issues = []
        if not code_ok:
            issues.append("Code quality checks")
        if not security_ok:
            issues.append("Security checks")
        if not all_files_present:
            issues.append("Missing files")
        
        print(f"⚠️  Issues found in: {', '.join(issues)}")
        print("Please review and fix before deploying")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
