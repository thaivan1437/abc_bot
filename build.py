#!/usr/bin/env python3
"""
Script tự động build LokBot thành file .exe
Sử dụng PyInstaller để đóng gói ứng dụng Python thành executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Chạy command và hiển thị kết quả"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - Thành công!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} - Lỗi!")
        print(result.stderr)
        return False
    return True

def check_pyinstaller():
    """Kiểm tra và cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã được cài đặt")
        return True
    except ImportError:
        print("📦 Đang cài đặt PyInstaller...")
        return run_command("pip install pyinstaller", "Cài đặt PyInstaller")

def create_requirements_txt():
    """Tạo requirements.txt từ Pipfile.lock"""
    print("\n📝 Tạo requirements.txt từ Pipfile...")
    
    try:
        # Đọc từ Pipfile
        pipfile_content = """arrow==1.2.*
fire==0.5.*
loguru==0.7.*
tenacity==8.2.*
schedule==1.2.*
ratelimit==2.2.*
python-socketio<5
numpy==1.24.*
httpx[http2]==0.24.*
pyjwt==2.7.*
pyinstaller>=5.0
"""
        
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(pipfile_content)
        
        print("✅ Đã tạo requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo requirements.txt: {str(e)}")
        return False

def create_spec_file():
    """Tạo file .spec cho PyInstaller với cấu hình tối ưu"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lokbot/__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('lokbot/assets', 'lokbot/assets'),
        ('config.example.json', '.'),
    ],
    hiddenimports=[
        'lokbot',
        'lokbot.app',
        'lokbot.client',
        'lokbot.farmer',
        'lokbot.async_farmer',
        'lokbot.async_client',
        'lokbot.captcha_solver',
        'lokbot.util',
        'lokbot.enum',
        'lokbot.exceptions',
        'engineio.async_drivers.aiohttp',
        'socketio.async_client',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='lokbot',
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
'''
    
    # Tạo spec file cho GUI version
    gui_spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lokbot/gui_main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('lokbot/assets', 'lokbot/assets'),
        ('config.example.json', '.'),
    ],
    hiddenimports=[
        'lokbot',
        'lokbot.app',
        'lokbot.client',
        'lokbot.farmer',
        'lokbot.async_farmer',
        'lokbot.async_client',
        'lokbot.captcha_solver',
        'lokbot.util',
        'lokbot.enum',
        'lokbot.exceptions',
        'lokbot.gui',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'engineio.async_drivers.aiohttp',
        'socketio.async_client',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='lokbot-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open("lokbot.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    with open("lokbot-gui.spec", "w", encoding="utf-8") as f:
        f.write(gui_spec_content)
    
    print("✅ Đã tạo lokbot.spec và lokbot-gui.spec")
    return True

def build_exe():
    """Build file .exe"""
    print("\n🔨 Bắt đầu build file .exe...")
    
    # Tạo thư mục build nếu chưa có
    os.makedirs("build", exist_ok=True)
    os.makedirs("dist", exist_ok=True)
    
    # Build CLI version
    print("📦 Building CLI version...")
    cmd = "pyinstaller --clean lokbot.spec"
    if not run_command(cmd, "Build CLI version"):
        return False
    
    # Build GUI version
    print("📦 Building GUI version...")
    cmd = "pyinstaller --clean lokbot-gui.spec"
    if not run_command(cmd, "Build GUI version"):
        return False
    
    # Kiểm tra files đã được tạo (macOS không có .exe extension)
    import platform
    ext = ".exe" if platform.system() == "Windows" else ""
    
    cli_exe = Path(f"dist/lokbot{ext}")
    gui_exe = Path(f"dist/lokbot-gui{ext}")
    
    success = True
    if cli_exe.exists():
        print(f"🎉 CLI Build thành công! File tại: {cli_exe.absolute()}")
        print(f"📊 Kích thước CLI: {cli_exe.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print(f"❌ Không tìm thấy lokbot{ext} sau khi build")
        success = False
    
    if gui_exe.exists():
        print(f"🎉 GUI Build thành công! File tại: {gui_exe.absolute()}")
        print(f"📊 Kích thước GUI: {gui_exe.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print(f"❌ Không tìm thấy lokbot-gui{ext} sau khi build")
        success = False
    
    return success

def create_batch_file():
    """Tạo file .bat để chạy dễ dàng hơn"""
    # CLI batch file
    cli_batch_content = '''@echo off
echo ========================================
echo       LokBot CLI - League of Kingdoms Bot
echo ========================================
echo.
echo Cach su dung: lokbot.exe [YOUR_TOKEN]
echo.
if "%1"=="" (
    echo Loi: Ban chua nhap token!
    echo Vi du: lokbot.exe your_x_access_token_here
    pause
    exit /b 1
)

lokbot.exe %1
pause
'''
    
    # GUI batch file
    gui_batch_content = '''@echo off
echo ========================================
echo       LokBot GUI - League of Kingdoms Bot
echo ========================================
echo.
echo Starting GUI application...
echo.

lokbot-gui.exe
'''
    
    with open("dist/run_lokbot_cli.bat", "w", encoding="utf-8") as f:
        f.write(cli_batch_content)
    
    with open("dist/run_lokbot_gui.bat", "w", encoding="utf-8") as f:
        f.write(gui_batch_content)
    
    print("✅ Đã tạo file run_lokbot_cli.bat và run_lokbot_gui.bat")
    return True

def main():
    """Hàm main để build"""
    print("🤖 LokBot Build Script")
    print("=" * 50)
    
    # Kiểm tra môi trường
    if not Path("lokbot/__main__.py").exists():
        print("❌ Không tìm thấy lokbot/__main__.py. Hãy chạy script trong thư mục gốc của dự án.")
        sys.exit(1)
    
    # Các bước build
    steps = [
        (check_pyinstaller, "Kiểm tra PyInstaller"),
        (create_requirements_txt, "Tạo requirements.txt"),
        (create_spec_file, "Tạo file cấu hình .spec"),
        (build_exe, "Build file .exe"),
        (create_batch_file, "Tạo file batch helper")
    ]
    
    for step_func, step_name in steps:
        try:
            if not step_func():
                print(f"❌ Lỗi tại bước: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Lỗi tại bước {step_name}: {str(e)}")
            sys.exit(1)
    
    print("\n🎉 BUILD HOÀN THÀNH!")
    print("=" * 50)
    print("📁 Files được tạo:")
    print("   • CLI Version: dist/lokbot.exe")
    print("   • GUI Version: dist/lokbot-gui.exe")
    print("\n🚀 Cách sử dụng:")
    print("   CLI: lokbot.exe YOUR_X_ACCESS_TOKEN")
    print("   GUI: lokbot-gui.exe (hoặc double-click)")
    print("\n📋 Helper files:")
    print("   • run_lokbot_cli.bat - Chạy CLI version")
    print("   • run_lokbot_gui.bat - Chạy GUI version")
    print("\n💡 Lưu ý:")
    print("   - Files .exe có thể chạy độc lập mà không cần Python")
    print("   - GUI version cho phép quản lý nhiều token và config")
    print("   - Có thể copy sang máy khác để chạy")
    print("   - Kích thước file có thể khá lớn do chứa Python runtime")

if __name__ == "__main__":
    main()