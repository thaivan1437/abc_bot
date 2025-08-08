#!/usr/bin/env python3
"""
Script debug environment để kiểm tra socketio installation
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_info():
    """Kiểm tra thông tin Python"""
    print("🐍 PYTHON ENVIRONMENT INFO")
    print("=" * 50)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path[:3]}...")  # First 3 paths
    print(f"Current working directory: {os.getcwd()}")
    
def check_pip_info():
    """Kiểm tra pip info"""
    print("\n📦 PIP INFO")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        print(f"Pip version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Pip check failed: {e}")

def check_socketio_installation():
    """Kiểm tra socketio installation chi tiết"""
    print("\n🔌 SOCKET.IO INSTALLATION CHECK")
    print("=" * 50)
    
    # Test engineio
    try:
        import engineio
        print(f"✅ engineio version: {engineio.__version__}")
        print(f"   engineio location: {engineio.__file__}")
    except ImportError as e:
        print(f"❌ engineio import failed: {e}")
    except Exception as e:
        print(f"⚠️ engineio other error: {e}")
    
    # Test socketio
    try:
        import socketio
        print(f"✅ socketio version: {socketio.__version__}")
        print(f"   socketio location: {socketio.__file__}")
        
        # Test client creation
        client = socketio.Client()
        print("✅ socketio Client creation: OK")
    except ImportError as e:
        print(f"❌ socketio import failed: {e}")
    except Exception as e:
        print(f"⚠️ socketio other error: {e}")

def check_all_dependencies():
    """Kiểm tra tất cả dependencies"""
    print("\n📋 ALL DEPENDENCIES CHECK")
    print("=" * 50)
    
    dependencies = [
        "fire", "loguru", "tenacity", "schedule", "ratelimit", 
        "numpy", "httpx", "pyjwt", "arrow", "engineio", "socketio"
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'unknown')
            location = getattr(module, '__file__', 'unknown')
            print(f"✅ {dep}: {version} ({Path(location).parent.name if location != 'unknown' else 'unknown'})")
        except ImportError:
            print(f"❌ {dep}: NOT INSTALLED")
        except Exception as e:
            print(f"⚠️ {dep}: ERROR - {e}")

def check_pyinstaller():
    """Kiểm tra PyInstaller"""
    print("\n🔨 PYINSTALLER CHECK")
    print("=" * 50)
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller version: {PyInstaller.__version__}")
        print(f"   PyInstaller location: {PyInstaller.__file__}")
    except ImportError:
        print("❌ PyInstaller not installed")
    except Exception as e:
        print(f"⚠️ PyInstaller error: {e}")

def test_socketio_functionality():
    """Test socketio functionality"""
    print("\n🧪 SOCKET.IO FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        import socketio
        import engineio
        
        # Test basic client
        sio = socketio.Client()
        print("✅ Client creation: OK")
        
        # Test event handlers
        @sio.event
        def connect():
            print("Connected!")
        
        @sio.event  
        def disconnect():
            print("Disconnected!")
            
        print("✅ Event handlers: OK")
        
        # Test without actually connecting
        print("✅ Basic functionality: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def run_pip_list():
    """Chạy pip list để xem tất cả packages"""
    print("\n📋 INSTALLED PACKAGES (pip list)")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True)
        
        lines = result.stdout.strip().split('\n')
        relevant_packages = []
        
        for line in lines:
            if any(pkg in line.lower() for pkg in ['socket', 'engine', 'fire', 'loguru', 'pyinstaller', 'numpy', 'httpx']):
                relevant_packages.append(line)
        
        if relevant_packages:
            print("Relevant packages:")
            for pkg in relevant_packages:
                print(f"  {pkg}")
        else:
            print("No relevant packages found in pip list")
            
    except Exception as e:
        print(f"❌ pip list failed: {e}")

def suggest_fixes():
    """Đề xuất cách fix"""
    print("\n💡 SUGGESTED FIXES")
    print("=" * 50)
    
    print("Nếu socketio import OK nhưng build fail:")
    print("1. Thử reinstall trong same environment:")
    print(f"   {sys.executable} -m pip uninstall python-socketio python-engineio")
    print(f"   {sys.executable} -m pip install python-engineio python-socketio<5")
    
    print("\n2. Thử với exact versions:")
    print(f"   {sys.executable} -m pip install python-engineio==4.7.1 python-socketio==5.8.0")
    
    print("\n3. Check PyInstaller hidden imports:")
    print("   Thêm vào .spec file: 'socketio', 'engineio', 'socketio.client'")
    
    print("\n4. Sử dụng fallback nếu cần:")
    print("   import socketio_fallback  # before other imports")

def main():
    """Main function"""
    print("🔍 ENVIRONMENT DEBUG TOOL")
    print("=" * 60)
    print("This tool will help debug socketio installation issues")
    print("=" * 60)
    
    check_python_info()
    check_pip_info()
    check_socketio_installation()
    check_all_dependencies()
    check_pyinstaller()
    
    # Test functionality
    if test_socketio_functionality():
        print("\n🎉 SOCKET.IO FUNCTIONALITY: OK")
        print("If build still fails, it's likely a PyInstaller issue")
    else:
        print("\n❌ SOCKET.IO FUNCTIONALITY: FAILED")
        print("Need to reinstall socketio properly")
    
    run_pip_list()
    suggest_fixes()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("1. If socketio imports OK: Fix PyInstaller configuration")
    print("2. If socketio imports fail: Reinstall socketio")
    print("3. If all else fails: Use fallback solution")
    print("=" * 60)

if __name__ == "__main__":
    main()