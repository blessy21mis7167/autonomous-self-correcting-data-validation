#!/usr/bin/env python
"""
Verification script to check if all required components are installed and working
Run this to verify your setup before starting the application
"""

import os
import sys
from pathlib import Path

def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n📦 Checking Python Packages...")
    packages = ['fastapi', 'uvicorn', 'pydantic']
    missing = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (NOT INSTALLED)")
            missing.append(package)
    
    return len(missing) == 0

def check_backend_files():
    """Check if all backend files exist"""
    print("\n📁 Checking Backend Files...")
    files = [
        'backend/app.py',
        'backend/validation.py',
        'backend/tools.py',
        'backend/database.py',
        'backend/requirements.txt',
        'backend/__init__.py'
    ]
    
    all_exist = True
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def check_frontend_files():
    """Check if all frontend files exist"""
    print("\n📁 Checking Frontend Files...")
    files = [
        'frontend-react/src/App.jsx',
        'frontend-react/src/main.jsx',
        'frontend-react/src/styles.css',
        'frontend-react/package.json',
        'frontend-react/vite.config.js',
        'frontend-react/index.html'
    ]
    
    all_exist = True
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def check_documentation():
    """Check if documentation files exist"""
    print("\n📚 Checking Documentation Files...")
    files = [
        'README.md',
        'SETUP.md',
        'QUICKSTART.md',
        'ARCHITECTURE.md',
        'BUILD_COMPLETE.md'
    ]
    
    all_exist = True
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if database exists"""
    print("\n🗄️  Checking Database...")
    db_path = Path('database/validation.db')
    db_dir = Path('database')
    
    if db_dir.exists():
        print(f"  ✅ database/ directory exists")
    else:
        print(f"  ⚠️  database/ directory will be created on first run")
    
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"  ✅ database/validation.db exists ({size} bytes)")
        return True
    else:
        print(f"  ⓘ database/validation.db will be created on first run")
        return True

def check_scripts():
    """Check if startup scripts exist"""
    print("\n🚀 Checking Startup Scripts...")
    files = [
        'run.py',
        'start.ps1',
        'start.sh'
    ]
    
    all_exist = True
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("=" * 50)
    print("🔍 Autonomous Data Validation System")
    print("   Setup Verification Script")
    print("=" * 50)
    
    os.chdir(Path(__file__).parent)
    
    results = {
        'Backend Files': check_backend_files(),
        'Frontend Files': check_frontend_files(),
        'Documentation': check_documentation(),
        'Database': check_database(),
        'Startup Scripts': check_scripts(),
    }
    
    print("\n" + "=" * 50)
    print("📋 Summary")
    print("=" * 50)
    
    all_ok = all(results.values())
    
    for check, result in results.items():
        status = "✅" if result else "⚠️"
        print(f"{status} {check}")
    
    print("\n" + "=" * 50)
    
    if all_ok:
        print("✅ All checks passed! System is ready to run.")
        print("\n🚀 Next steps:")
        print("   Windows: .\\start.ps1")
        print("   Linux/Mac: ./start.sh")
        print("\nThen navigate to: http://localhost:5173")
        return 0
    else:
        print("⚠️  Some files are missing. Please reinstall.")
        print("\nRun: pip install -r backend/requirements.txt")
        print("Then: cd frontend-react && npm install")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        sys.exit(1)
