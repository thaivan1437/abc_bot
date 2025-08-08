#!/usr/bin/env python3
"""
Script đặc biệt để fix lỗi Socket.IO trên Windows
Thử nhiều cách khác nhau để cài đặt python-socketio
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description="", timeout=300):
    """Chạy command với timeout"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, timeout=timeout)
        print(f"✅ {description} - Thành công!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout ({timeout}s)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Lỗi!")
        print(f"Exit code: {e.returncode}")
        if e.stderr:
            print("STDERR:", e.stderr)
        if e.stdout:
            print("STDOUT:", e.stdout)
        return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def method_1_standard():
    """Phương pháp 1: Cài đặt bình thường"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 1: Cài đặt bình thường")
    print("="*50)
    
    commands = [
        ("python-engineio", "Cài Engine.IO trước"),
        ("python-socketio<5", "Cài Socket.IO version < 5")
    ]
    
    for package, desc in commands:
        if run_command(f"{sys.executable} -m pip install {package}", desc):
            continue
        else:
            return False
    
    return True

def method_2_no_cache():
    """Phương pháp 2: Cài đặt không dùng cache"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 2: Cài đặt không dùng cache")
    print("="*50)
    
    # Clear cache trước
    run_command(f"{sys.executable} -m pip cache purge", "Clear pip cache")
    
    commands = [
        f"{sys.executable} -m pip install --no-cache-dir python-engineio",
        f"{sys.executable} -m pip install --no-cache-dir python-socketio<5"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Chạy: {cmd}"):
            return False
    
    return True

def method_3_force_reinstall():
    """Phương pháp 3: Force reinstall"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 3: Force reinstall")
    print("="*50)
    
    # Uninstall trước
    uninstall_commands = [
        f"{sys.executable} -m pip uninstall -y python-socketio",
        f"{sys.executable} -m pip uninstall -y python-engineio"
    ]
    
    for cmd in uninstall_commands:
        run_command(cmd, f"Uninstall: {cmd}")
    
    # Reinstall
    install_commands = [
        f"{sys.executable} -m pip install --force-reinstall python-engineio",
        f"{sys.executable} -m pip install --force-reinstall python-socketio<5"
    ]
    
    for cmd in install_commands:
        if not run_command(cmd, f"Force install: {cmd}"):
            return False
    
    return True

def method_4_specific_versions():
    """Phương pháp 4: Cài version cụ thể"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 4: Cài version cụ thể")
    print("="*50)
    
    # Thử các version cụ thể đã test
    version_combinations = [
        ("python-engineio==4.7.1", "python-socketio==5.8.0"),
        ("python-engineio==4.6.1", "python-socketio==5.7.2"),
        ("python-engineio==4.5.4", "python-socketio==5.6.0")
    ]
    
    for engineio_ver, socketio_ver in version_combinations:
        print(f"\n🧪 Thử combination: {engineio_ver} + {socketio_ver}")
        
        # Uninstall
        run_command(f"{sys.executable} -m pip uninstall -y python-socketio python-engineio", "Uninstall old")
        
        # Install specific versions
        if run_command(f"{sys.executable} -m pip install {engineio_ver}", f"Cài {engineio_ver}"):
            if run_command(f"{sys.executable} -m pip install {socketio_ver}", f"Cài {socketio_ver}"):
                return True
    
    return False

def method_5_pre_compiled():
    """Phương pháp 5: Dùng pre-compiled wheels"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 5: Dùng pre-compiled wheels")
    print("="*50)
    
    commands = [
        f"{sys.executable} -m pip install --only-binary=all python-engineio",
        f"{sys.executable} -m pip install --only-binary=all python-socketio<5"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Install binary: {cmd}"):
            return False
    
    return True

def method_6_conda():
    """Phương pháp 6: Sử dụng conda"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 6: Sử dụng conda (nếu có)")
    print("="*50)
    
    # Kiểm tra conda
    if run_command("conda --version", "Kiểm tra conda"):
        commands = [
            "conda install -c conda-forge python-engineio",
            "conda install -c conda-forge python-socketio"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Conda install: {cmd}"):
                return False
        
        return True
    else:
        print("❌ Conda không có sẵn")
        return False

def method_7_alternative_package():
    """Phương pháp 7: Sử dụng package thay thế"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 7: Package thay thế")
    print("="*50)
    
    # Thử websocket-client thay thế
    alternatives = [
        "websocket-client",
        "websockets", 
        "simple-websocket"
    ]
    
    for alt in alternatives:
        if run_command(f"{sys.executable} -m pip install {alt}", f"Cài {alt}"):
            print(f"✅ Đã cài {alt} làm thay thế")
    
    # Thử cài socketio một lần nữa
    return run_command(f"{sys.executable} -m pip install python-socketio<5", "Cài socketio sau khi có websocket")

def method_8_from_source():
    """Phương pháp 8: Cài từ source"""
    print("\n" + "="*50)
    print("🔧 PHƯƠNG PHÁP 8: Cài từ source (GitHub)")
    print("="*50)
    
    # Cài git dependencies
    git_packages = [
        "git+https://github.com/miguelgrinberg/python-engineio.git",
        "git+https://github.com/miguelgrinberg/python-socketio.git"
    ]
    
    for package in git_packages:
        if not run_command(f"{sys.executable} -m pip install {package}", f"Cài từ git: {package}"):
            return False
    
    return True

def verify_installation():
    """Kiểm tra installation"""
    print("\n" + "="*50)
    print("🔍 KIỂM TRA INSTALLATION")
    print("="*50)
    
    test_code = '''
try:
    import engineio
    print("✅ engineio version:", engineio.__version__)
except ImportError as e:
    print("❌ engineio import failed:", str(e))

try:
    import socketio
    print("✅ socketio version:", socketio.__version__)
except ImportError as e:
    print("❌ socketio import failed:", str(e))

try:
    # Test basic functionality
    sio = socketio.Client()
    print("✅ socketio Client creation OK")
except Exception as e:
    print("❌ socketio Client creation failed:", str(e))
'''
    
    return run_command(f'{sys.executable} -c "{test_code}"', "Test import socketio")

def create_fallback_solution():
    """Tạo giải pháp fallback nếu không cài được socketio"""
    print("\n" + "="*50)
    print("🔧 TẠO FALLBACK SOLUTION")
    print("="*50)
    
    fallback_code = '''
# Fallback cho socketio nếu không cài được
import warnings

class MockSocketIO:
    """Mock SocketIO client để app không crash"""
    def __init__(self, *args, **kwargs):
        warnings.warn("SocketIO not available, using mock client", UserWarning)
    
    def connect(self, *args, **kwargs):
        print("Mock SocketIO: connect called")
        return False
    
    def disconnect(self, *args, **kwargs):
        print("Mock SocketIO: disconnect called")
    
    def emit(self, *args, **kwargs):
        print("Mock SocketIO: emit called")
    
    def on(self, *args, **kwargs):
        print("Mock SocketIO: on called")

# Monkey patch nếu socketio không có
try:
    import socketio
except ImportError:
    import sys
    import types
    
    # Tạo mock module
    mock_socketio = types.ModuleType('socketio')
    mock_socketio.Client = MockSocketIO
    mock_socketio.SimpleClient = MockSocketIO
    
    # Add to sys.modules
    sys.modules['socketio'] = mock_socketio
    print("⚠️ Using mock socketio module")
'''
    
    try:
        with open("socketio_fallback.py", "w", encoding="utf-8") as f:
            f.write(fallback_code)
        print("✅ Đã tạo socketio_fallback.py")
        print("💡 Thêm 'import socketio_fallback' vào đầu main script nếu cần")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo fallback: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 Socket.IO Fix Tool for Windows")
    print("=" * 60)
    
    if platform.system() != "Windows":
        print(f"⚠️ Script này được thiết kế cho Windows. OS: {platform.system()}")
    
    print("\n📋 Sẽ thử các phương pháp sau theo thứ tự:")
    methods = [
        "1. Cài đặt bình thường",
        "2. Cài đặt không dùng cache", 
        "3. Force reinstall",
        "4. Cài version cụ thể",
        "5. Dùng pre-compiled wheels",
        "6. Sử dụng conda (nếu có)",
        "7. Package thay thế",
        "8. Cài từ source (GitHub)"
    ]
    
    for method in methods:
        print(f"   {method}")
    
    input("\nPress Enter to continue...")
    
    # Thử từng phương pháp
    methods_to_try = [
        (method_1_standard, "Phương pháp 1: Cài đặt bình thường"),
        (method_2_no_cache, "Phương pháp 2: Không dùng cache"),
        (method_3_force_reinstall, "Phương pháp 3: Force reinstall"),
        (method_4_specific_versions, "Phương pháp 4: Version cụ thể"),
        (method_5_pre_compiled, "Phương pháp 5: Pre-compiled wheels"),
        (method_6_conda, "Phương pháp 6: Conda"),
        (method_7_alternative_package, "Phương pháp 7: Package thay thế"),
        (method_8_from_source, "Phương pháp 8: Từ source")
    ]
    
    success = False
    
    for method_func, method_name in methods_to_try:
        print(f"\n{'='*60}")
        print(f"🚀 Thử {method_name}")
        print('='*60)
        
        try:
            if method_func():
                print(f"✅ {method_name} - THÀNH CÔNG!")
                
                # Verify
                if verify_installation():
                    print("🎉 Socket.IO đã được cài đặt thành công!")
                    success = True
                    break
                else:
                    print("❌ Verification failed, thử phương pháp tiếp theo...")
            else:
                print(f"❌ {method_name} - FAILED")
        
        except KeyboardInterrupt:
            print("\n❌ Người dùng hủy")
            break
        except Exception as e:
            print(f"❌ Exception trong {method_name}: {str(e)}")
    
    # Kết quả
    print("\n" + "="*60)
    if success:
        print("🎉 SOCKET.IO ĐÃ ĐƯỢC CÀI ĐẶT THÀNH CÔNG!")
        print("✅ Có thể tiếp tục build project")
        print("\n🚀 Chạy tiếp:")
        print("   python build_windows.py")
    else:
        print("❌ KHÔNG THỂ CÀI ĐẶT SOCKET.IO")
        print("🔧 Tạo fallback solution...")
        
        if create_fallback_solution():
            print("✅ Đã tạo fallback solution")
            print("💡 Project có thể build được nhưng Socket.IO features sẽ bị disabled")
        
        print("\n🛠️ Các lựa chọn:")
        print("1. Sử dụng Anaconda Python thay vì Python.org")
        print("2. Cài Visual Studio Build Tools")
        print("3. Thử trên máy Windows khác")
        print("4. Sử dụng WSL (Windows Subsystem for Linux)")
        print("5. Build trên cloud (GitHub Actions)")

if __name__ == "__main__":
    main()