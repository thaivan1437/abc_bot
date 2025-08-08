#!/usr/bin/env python3
"""
Script build chuyên biệt cho Windows
Tạo file .exe với tất cả dependencies cần thiết
"""

import os
import sys
import subprocess
import shutil
import platform
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

def check_windows():
    """Kiểm tra có phải Windows không"""
    if platform.system() != "Windows":
        print("⚠️  Script này được thiết kế cho Windows")
        print(f"Hệ điều hành hiện tại: {platform.system()}")
        print("Vẫn có thể hoạt động nhưng file output sẽ không có extension .exe")
        return False
    return True

def install_dependencies():
    """Cài đặt tất cả dependencies cần thiết"""
    print("\n📦 Cài đặt dependencies...")
    
    # Dependencies cơ bản (ít có vấn đề)
    basic_dependencies = [
        "pyinstaller>=5.0",
        "fire==0.5.*", 
        "loguru==0.7.*",
        "tenacity==8.2.*",
        "schedule==1.2.*",
        "ratelimit==2.2.*",
        "pyjwt==2.7.*",
        "arrow==1.2.*"
    ]
    
    # Dependencies phức tạp (có thể có vấn đề)
    complex_dependencies = [
        "numpy==1.24.*",
        "httpx[http2]==0.24.*"
    ]
    
    # Socket.IO dependencies (thường có vấn đề nhất)
    socketio_dependencies = [
        "python-engineio",
        "python-socketio<5"
    ]
    
    # Cài basic dependencies
    print("🔧 Cài đặt basic dependencies...")
    for dep in basic_dependencies:
        if not run_command(f"pip install {dep}", f"Cài đặt {dep}"):
            print(f"❌ Failed to install {dep}")
            return False
    
    # Cài complex dependencies
    print("🔧 Cài đặt complex dependencies...")
    for dep in complex_dependencies:
        if not run_command(f"pip install {dep}", f"Cài đặt {dep}"):
            print(f"⚠️ Failed to install {dep}, trying alternative...")
            # Thử cách khác
            if not run_command(f"pip install --no-cache-dir {dep}", f"Cài đặt {dep} (no cache)"):
                print(f"❌ Cannot install {dep}")
                return False
    
    # Cài Socket.IO dependencies (có thể skip nếu fail)
    print("🔧 Cài đặt Socket.IO dependencies...")
    socketio_success = True
    for dep in socketio_dependencies:
        if not run_command(f"pip install {dep}", f"Cài đặt {dep}"):
            print(f"⚠️ Failed to install {dep}")
            socketio_success = False
    
    if not socketio_success:
        print("❌ Socket.IO installation failed!")
        print("💡 Chạy script đặc biệt để fix:")
        print("   python fix_socketio.py")
        print("💡 Hoặc tiếp tục với mock socketio (một số tính năng sẽ bị disabled)")
        
        response = input("Tiếp tục build với mock socketio? (y/N): ").lower()
        if response != 'y':
            return False
        
        # Copy fallback file
        try:
            import shutil
            if os.path.exists("socketio_fallback.py"):
                print("✅ Sử dụng socketio fallback")
            else:
                print("❌ Không tìm thấy socketio_fallback.py")
                return False
        except Exception as e:
            print(f"❌ Lỗi setup fallback: {str(e)}")
            return False
    
    return True

def create_windows_spec():
    """Tạo .spec files cho Windows với cấu hình đầy đủ"""
    
    # CLI spec
    cli_spec = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lokbot/__main__.py'],
    pathex=[],
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
        'fire',
        'loguru',
        'tenacity',
        'schedule',
        'ratelimit',
        'numpy',
        'httpx',
        'pyjwt',
        'arrow',
        'socketio',
        'engineio',
        'socketio.client',
        'engineio.client',
        'socketio.async_client',
        'engineio.async_client',
        'engineio.async_drivers.aiohttp',
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
    icon=None,
)
'''

    # GUI spec
    gui_spec = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lokbot/gui_main.py'],
    pathex=[],
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
        'fire',
        'loguru',
        'tenacity',
        'schedule',
        'ratelimit',
        'numpy',
        'httpx',
        'pyjwt',
        'arrow',
        'socketio',
        'engineio',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'socketio.client',
        'engineio.client',
        'socketio.async_client',
        'engineio.async_client',
        'engineio.async_drivers.aiohttp',
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
    
    with open("lokbot-windows.spec", "w", encoding="utf-8") as f:
        f.write(cli_spec)
    
    with open("lokbot-gui-windows.spec", "w", encoding="utf-8") as f:
        f.write(gui_spec)
    
    print("✅ Đã tạo Windows spec files")
    return True

def build_executables():
    """Build executables cho Windows"""
    print("\n🔨 Building executables...")
    
    # Tạo thư mục
    os.makedirs("dist", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    
    # Build CLI
    print("📦 Building CLI version...")
    if not run_command("pyinstaller --clean lokbot-windows.spec", "Build CLI"):
        return False
    
    # Build GUI  
    print("📦 Building GUI version...")
    if not run_command("pyinstaller --clean lokbot-gui-windows.spec", "Build GUI"):
        return False
    
    return True

def create_batch_files():
    """Tạo batch files cho Windows"""
    
    cli_bat = '''@echo off
echo ==========================================
echo    LokBot CLI - League of Kingdoms Bot
echo ==========================================
echo.
echo Usage: lokbot.exe [YOUR_X_ACCESS_TOKEN]
echo.
if "%1"=="" (
    echo Error: No token provided!
    echo Example: lokbot.exe your_x_access_token_here
    echo.
    pause
    exit /b 1
)

echo Starting LokBot with token: %1
echo.
lokbot.exe %1
pause
'''

    gui_bat = '''@echo off
echo ==========================================
echo    LokBot GUI - League of Kingdoms Bot  
echo ==========================================
echo.
echo Starting GUI application...
echo You can manage multiple tokens and configs in the GUI.
echo.

start lokbot-gui.exe
'''

    installer_bat = '''@echo off
echo ==========================================
echo       LokBot Windows Installer
echo ==========================================
echo.
echo This will copy LokBot files to Program Files
echo and create desktop shortcuts.
echo.
pause

if not exist "%ProgramFiles%\\LokBot" mkdir "%ProgramFiles%\\LokBot"

copy lokbot.exe "%ProgramFiles%\\LokBot\\"
copy lokbot-gui.exe "%ProgramFiles%\\LokBot\\"
copy *.bat "%ProgramFiles%\\LokBot\\"

echo.
echo Creating desktop shortcuts...
echo Set oWS = WScript.CreateObject("WScript.Shell") > temp.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\LokBot GUI.lnk" >> temp.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> temp.vbs
echo oLink.TargetPath = "%ProgramFiles%\\LokBot\\lokbot-gui.exe" >> temp.vbs
echo oLink.Save >> temp.vbs
cscript temp.vbs
del temp.vbs

echo.
echo ✅ Installation completed!
echo LokBot GUI shortcut created on Desktop
pause
'''
    
    with open("dist/run_lokbot_cli.bat", "w", encoding="utf-8") as f:
        f.write(cli_bat)
    
    with open("dist/run_lokbot_gui.bat", "w", encoding="utf-8") as f:
        f.write(gui_bat)
        
    with open("dist/install.bat", "w", encoding="utf-8") as f:
        f.write(installer_bat)
    
    print("✅ Đã tạo batch files")
    return True

def verify_build():
    """Kiểm tra kết quả build"""
    print("\n🔍 Kiểm tra kết quả build...")
    
    files_to_check = [
        "dist/lokbot.exe",
        "dist/lokbot-gui.exe", 
        "dist/run_lokbot_cli.bat",
        "dist/run_lokbot_gui.bat",
        "dist/install.bat"
    ]
    
    all_good = True
    for file_path in files_to_check:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} - {size/1024/1024:.1f} MB")
        else:
            print(f"❌ {file_path} - Không tìm thấy")
            all_good = False
    
    return all_good

def main():
    """Main function"""
    print("🪟 LokBot Windows Build Script")
    print("=" * 50)
    
    # Kiểm tra Windows
    is_windows = check_windows()
    
    # Kiểm tra entry point
    if not Path("lokbot/__main__.py").exists():
        print("❌ Không tìm thấy lokbot/__main__.py")
        print("Hãy chạy script trong thư mục gốc của dự án")
        sys.exit(1)
    
    # Các bước build
    steps = [
        (install_dependencies, "Cài đặt dependencies"),
        (create_windows_spec, "Tạo Windows spec files"),
        (build_executables, "Build executables"),
        (create_batch_files, "Tạo batch files"),
        (verify_build, "Kiểm tra kết quả")
    ]
    
    for step_func, step_name in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if not step_func():
                print(f"❌ Lỗi tại bước: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Exception tại bước {step_name}: {str(e)}")
            sys.exit(1)
    
    # Kết quả
    print("\n" + "="*60)
    print("🎉 BUILD WINDOWS HOÀN THÀNH!")
    print("="*60)
    print("📁 Files được tạo trong thư mục dist/:")
    print("   • lokbot.exe           - CLI version")
    print("   • lokbot-gui.exe       - GUI version")
    print("   • run_lokbot_cli.bat   - CLI helper")
    print("   • run_lokbot_gui.bat   - GUI helper")
    print("   • install.bat          - Windows installer")
    
    print("\n🚀 Cách sử dụng:")
    print("   1. Copy toàn bộ thư mục dist/ sang Windows")
    print("   2. Double-click lokbot-gui.exe để mở GUI")
    print("   3. Hoặc chạy run_lokbot_cli.bat với token")
    print("   4. Chạy install.bat để cài đặt vào Program Files")
    
    print("\n💡 Lưu ý:")
    print("   - Files .exe chỉ chạy được trên Windows")
    print("   - GUI version không cần console window")
    print("   - Có thể bị Windows Defender block, thêm exception")
    print("   - Test trên máy sạch trước khi phân phối")

if __name__ == "__main__":
    main()