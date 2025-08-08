#!/usr/bin/env python3
"""
Quick fix cho vấn đề socketio sau khi fix_socketio.py thành công
nhưng build_windows.py vẫn fail
"""

import sys
import subprocess
import os

def run_cmd(cmd, description=""):
    """Run command và return success/failure"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        if e.stderr:
            print("Error:", e.stderr)
        return False

def test_socketio():
    """Test socketio import"""
    test_code = """
try:
    import socketio
    import engineio
    print("✅ socketio version:", socketio.__version__)
    print("✅ engineio version:", engineio.__version__)
    
    # Test client creation
    client = socketio.Client()
    print("✅ Client creation: OK")
    exit(0)
except ImportError as e:
    print("❌ Import failed:", str(e))
    exit(1)
except Exception as e:
    print("❌ Other error:", str(e))
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True)
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def force_reinstall_socketio():
    """Force reinstall socketio với exact versions"""
    print("\n🔧 FORCE REINSTALL SOCKET.IO")
    print("=" * 40)
    
    # Uninstall completely
    uninstall_cmds = [
        f"{sys.executable} -m pip uninstall -y python-socketio",
        f"{sys.executable} -m pip uninstall -y python-engineio", 
        f"{sys.executable} -m pip uninstall -y socketio",
        f"{sys.executable} -m pip uninstall -y engineio"
    ]
    
    for cmd in uninstall_cmds:
        run_cmd(cmd, f"Uninstall: {cmd.split()[-1]}")
    
    # Clear cache
    run_cmd(f"{sys.executable} -m pip cache purge", "Clear pip cache")
    
    # Install exact versions that work
    install_cmds = [
        f"{sys.executable} -m pip install python-engineio==4.7.1",
        f"{sys.executable} -m pip install python-socketio==5.8.0"
    ]
    
    for cmd in install_cmds:
        if not run_cmd(cmd, f"Install: {cmd.split('==')[0].split()[-1]}"):
            return False
    
    return True

def fix_pyinstaller_imports():
    """Fix PyInstaller imports trong spec files"""
    print("\n🔧 FIX PYINSTALLER IMPORTS")
    print("=" * 40)
    
    spec_files = ["lokbot-windows.spec", "lokbot-gui-windows.spec"]
    
    # Socketio imports cần thiết
    socketio_imports = [
        "'socketio'",
        "'socketio.client'", 
        "'socketio.namespace'",
        "'engineio'",
        "'engineio.client'",
        "'engineio.socket'",
        "'simple_websocket'",
        "'wsproto'",
        "'bidict'"
    ]
    
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            print(f"📝 Updating {spec_file}...")
            
            try:
                with open(spec_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find hiddenimports section và add socketio imports
                if 'hiddenimports=[' in content:
                    # Add socketio imports
                    for imp in socketio_imports:
                        if imp not in content:
                            content = content.replace(
                                'hiddenimports=[',
                                f'hiddenimports=[\n        {imp},'
                            )
                
                with open(spec_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Updated {spec_file}")
                
            except Exception as e:
                print(f"❌ Error updating {spec_file}: {e}")
        else:
            print(f"⚠️ {spec_file} not found")

def create_test_build():
    """Tạo test build nhỏ để verify socketio"""
    print("\n🧪 CREATE TEST BUILD")
    print("=" * 40)
    
    test_script = """
import socketio
import engineio

print("Testing socketio imports...")
print(f"socketio version: {socketio.__version__}")
print(f"engineio version: {engineio.__version__}")

# Test client creation
try:
    client = socketio.Client()
    print("✅ Client creation successful")
except Exception as e:
    print(f"❌ Client creation failed: {e}")

print("Test completed successfully!")
"""
    
    # Write test script
    with open("test_socketio.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    # Create simple spec
    spec_content = f"""
import sys
sys.path.insert(0, '.')

a = Analysis(
    ['test_socketio.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'socketio',
        'socketio.client',
        'engineio', 
        'engineio.client',
        'simple_websocket',
        'wsproto',
        'bidict'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='test_socketio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    with open("test_socketio.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # Build test
    if run_cmd("pyinstaller --clean test_socketio.spec", "Build test socketio"):
        # Test the built executable
        test_exe = "dist/test_socketio.exe" if os.name == 'nt' else "dist/test_socketio"
        if os.path.exists(test_exe):
            print(f"✅ Test executable created: {test_exe}")
            
            # Run test
            try:
                result = subprocess.run([test_exe], capture_output=True, text=True, timeout=30)
                print("Test output:")
                print(result.stdout)
                if result.returncode == 0:
                    print("✅ Test build successful!")
                    return True
                else:
                    print("❌ Test build failed")
                    print(result.stderr)
                    return False
            except Exception as e:
                print(f"❌ Error running test: {e}")
                return False
        else:
            print("❌ Test executable not found")
            return False
    else:
        return False

def main():
    """Main function"""
    print("🚀 QUICK FIX FOR SOCKETIO BUILD ISSUE")
    print("=" * 50)
    print("This script fixes socketio issues after fix_socketio.py reports success")
    print("but build_windows.py still fails")
    print("=" * 50)
    
    # Step 1: Test current socketio
    print("\n📋 STEP 1: Test current socketio installation")
    if test_socketio():
        print("✅ Socketio is working in current environment")
        print("The issue is likely with PyInstaller configuration")
        
        # Fix PyInstaller imports
        fix_pyinstaller_imports()
        
        # Test build
        print("\n📋 STEP 2: Test build with socketio")
        if create_test_build():
            print("\n🎉 SUCCESS! Socketio build is working")
            print("You can now run: python build_windows.py")
            
            # Cleanup test files
            for f in ["test_socketio.py", "test_socketio.spec"]:
                if os.path.exists(f):
                    os.remove(f)
            
        else:
            print("\n❌ Test build failed. Trying reinstall...")
            if force_reinstall_socketio():
                print("✅ Reinstall completed. Try build_windows.py again")
            else:
                print("❌ Reinstall failed. Use fallback solution.")
    else:
        print("❌ Socketio is NOT working in current environment")
        print("Need to reinstall socketio properly")
        
        if force_reinstall_socketio():
            print("✅ Reinstall completed")
            
            if test_socketio():
                print("✅ Socketio now working! Try build_windows.py")
            else:
                print("❌ Still not working. May need fallback solution")
        else:
            print("❌ Reinstall failed")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. If successful: run python build_windows.py")
    print("2. If still failing: run python debug_environment.py") 
    print("3. As last resort: use fallback with socketio_fallback.py")
    print("=" * 50)

if __name__ == "__main__":
    main()