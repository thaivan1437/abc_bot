#!/usr/bin/env python3
"""
Script cài đặt dependencies cho Windows
Giải quyết các vấn đề phổ biến khi cài đặt trên Windows
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description=""):
    """Chạy command và hiển thị kết quả"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, timeout=300)
        print(f"✅ {description} - Thành công!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout (5 phút)")
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

def check_python():
    """Kiểm tra Python version"""
    print("🐍 Kiểm tra Python...")
    
    try:
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python version quá cũ. Cần Python 3.8+")
            return False
        
        print("✅ Python version OK")
        return True
    except Exception as e:
        print(f"❌ Lỗi kiểm tra Python: {str(e)}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n📦 Upgrading pip...")
    
    commands = [
        f"{sys.executable} -m pip install --upgrade pip",
        f"{sys.executable} -m pip install --upgrade setuptools wheel"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Chạy: {cmd}"):
            print("⚠️ Pip upgrade failed, continuing anyway...")
    
    return True

def install_basic_dependencies():
    """Cài đặt dependencies cơ bản"""
    print("\n📦 Cài đặt dependencies cơ bản...")
    
    basic_deps = [
        "pyinstaller>=5.0",
        "setuptools>=60.0",
        "wheel",
        "packaging"
    ]
    
    for dep in basic_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Cài đặt {dep}"):
            print(f"⚠️ Failed to install {dep}")
            return False
    
    return True

def install_project_dependencies():
    """Cài đặt dependencies của project"""
    print("\n📦 Cài đặt project dependencies...")
    
    # Dependencies theo đúng version trong Pipfile
    dependencies = [
        "fire==0.5.*",
        "loguru==0.7.*", 
        "tenacity==8.2.*",
        "schedule==1.2.*",
        "ratelimit==2.2.*",
        "arrow==1.2.*",
        "pyjwt==2.7.*"
    ]
    
    # Dependencies có thể có vấn đề trên Windows
    complex_deps = [
        ("numpy==1.24.*", "NumPy - numerical computing"),
        ("httpx[http2]==0.24.*", "HTTPX - HTTP client"),
        ("python-socketio<5", "Socket.IO client"),
        ("python-engineio", "Engine.IO client")
    ]
    
    # Cài đặt dependencies đơn giản trước
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Cài đặt {dep}"):
            print(f"❌ Failed to install {dep}")
            return False
    
    # Cài đặt dependencies phức tạp
    for dep, desc in complex_deps:
        print(f"\n📦 Cài đặt {desc}...")
        
        # Thử cài đặt bình thường trước
        if run_command(f"{sys.executable} -m pip install {dep}", f"Cài đặt {dep}"):
            continue
        
        # Nếu fail, thử với --no-cache-dir
        print("⚠️ Thử lại với --no-cache-dir...")
        if run_command(f"{sys.executable} -m pip install --no-cache-dir {dep}", f"Cài đặt {dep} (no cache)"):
            continue
        
        # Nếu vẫn fail, thử với --force-reinstall
        print("⚠️ Thử lại với --force-reinstall...")
        if run_command(f"{sys.executable} -m pip install --force-reinstall {dep}", f"Cài đặt {dep} (force)"):
            continue
        
        print(f"❌ Không thể cài đặt {desc}")
        return False
    
    return True

def install_special_dependencies():
    """Cài đặt dependencies đặc biệt cho project này"""
    print("\n📦 Cài đặt special dependencies...")
    
    # python-engineio version cụ thể từ git (nếu cần)
    git_deps = [
        # Có thể cần cài từ git nếu PyPI version không work
        # "git+https://github.com/hldh214/python-engineio-3-for-lokbot@v3.14.3"
    ]
    
    for dep in git_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Cài đặt {dep}"):
            print(f"⚠️ Failed to install {dep}, trying alternative...")
    
    return True

def verify_installation():
    """Kiểm tra installation"""
    print("\n🔍 Kiểm tra installation...")
    
    test_imports = [
        ("fire", "Fire CLI framework"),
        ("loguru", "Loguru logging"),
        ("numpy", "NumPy"),
        ("httpx", "HTTPX"),
        ("socketio", "Socket.IO"),
        ("engineio", "Engine.IO"),
        ("PyInstaller", "PyInstaller")
    ]
    
    all_good = True
    for module, desc in test_imports:
        try:
            __import__(module)
            print(f"✅ {desc} - OK")
        except ImportError as e:
            print(f"❌ {desc} - FAILED: {str(e)}")
            all_good = False
    
    return all_good

def create_requirements_file():
    """Tạo requirements.txt file"""
    print("\n📝 Tạo requirements.txt...")
    
    requirements = """# LokBot Dependencies
fire==0.5.*
loguru==0.7.*
tenacity==8.2.*
schedule==1.2.*
ratelimit==2.2.*
arrow==1.2.*
numpy==1.24.*
httpx[http2]==0.24.*
pyjwt==2.7.*
python-socketio<5
python-engineio
pyinstaller>=5.0
setuptools>=60.0
wheel
packaging
"""
    
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        print("✅ Đã tạo requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo requirements.txt: {str(e)}")
        return False

def main():
    """Main function"""
    print("🪟 LokBot Dependencies Installer for Windows")
    print("=" * 60)
    
    # Kiểm tra OS
    if platform.system() != "Windows":
        print(f"⚠️ Script này được thiết kế cho Windows. OS hiện tại: {platform.system()}")
        print("Vẫn có thể hoạt động nhưng có thể có issues...")
    
    # Các bước cài đặt
    steps = [
        (check_python, "Kiểm tra Python"),
        (upgrade_pip, "Upgrade pip"),
        (install_basic_dependencies, "Cài đặt basic dependencies"),
        (install_project_dependencies, "Cài đặt project dependencies"),
        (install_special_dependencies, "Cài đặt special dependencies"),
        (verify_installation, "Kiểm tra installation"),
        (create_requirements_file, "Tạo requirements.txt")
    ]
    
    failed_steps = []
    
    for step_func, step_name in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if not step_func():
                print(f"❌ Lỗi tại bước: {step_name}")
                failed_steps.append(step_name)
                
                # Hỏi có muốn tiếp tục không
                if step_name not in ["Kiểm tra installation"]:
                    response = input(f"\n⚠️ Bước '{step_name}' failed. Tiếp tục? (y/N): ").lower()
                    if response != 'y':
                        print("❌ Dừng installation")
                        sys.exit(1)
        except KeyboardInterrupt:
            print("\n❌ Người dùng hủy installation")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Exception tại bước {step_name}: {str(e)}")
            failed_steps.append(step_name)
    
    # Kết quả
    print("\n" + "="*60)
    if failed_steps:
        print("⚠️ INSTALLATION HOÀN THÀNH VỚI MỘT SỐ LỖI")
        print(f"Các bước failed: {', '.join(failed_steps)}")
        print("\n💡 Có thể thử:")
        print("1. Chạy lại script này")
        print("2. Cài thủ công: pip install -r requirements.txt")
        print("3. Sử dụng conda thay vì pip")
        print("4. Kiểm tra firewall/antivirus")
    else:
        print("🎉 INSTALLATION HOÀN THÀNH THÀNH CÔNG!")
        print("✅ Tất cả dependencies đã được cài đặt")
        print("\n🚀 Bước tiếp theo:")
        print("   python build_windows.py")
    
    print("\n📋 Troubleshooting:")
    print("- Nếu có lỗi 'Microsoft Visual C++ 14.0 is required':")
    print("  Download và cài Visual Studio Build Tools")
    print("- Nếu có lỗi network: Kiểm tra proxy/firewall")
    print("- Nếu có lỗi permission: Chạy CMD as Administrator")

if __name__ == "__main__":
    main()