# 🪟 Hướng dẫn Build LokBot cho Windows

## 🎯 Mục tiêu

Tạo file `.exe` có thể chạy trên Windows mà không cần cài Python.

---

## 🔧 Phương pháp 1: Build trên Windows (Khuyến nghị)

### Bước 1: Chuẩn bị môi trường Windows

```cmd
# Cài Python 3.10+ từ python.org
# Hoặc dùng Microsoft Store

# Kiểm tra Python
python --version
```

### Bước 2: Clone/Copy source code

```cmd
# Copy toàn bộ thư mục lok_bot_c7_tieu_la sang Windows
# Hoặc clone từ git nếu có
```

### Bước 3: Cài dependencies

```cmd
cd lok_bot_c7_tieu_la

# Cài pipenv (nếu chưa có)
pip install pipenv

# Cài dependencies từ Pipfile
pipenv install

# Hoặc cài trực tiếp
pip install fire loguru tenacity schedule ratelimit numpy httpx pyjwt arrow python-socketio python-engineio pyinstaller
```

### Bước 4: Build

```cmd
# Chạy build script
python build.py
```

### Kết quả:

```
dist/
├── lokbot.exe          # CLI version
├── lokbot-gui.exe      # GUI version
├── run_lokbot_cli.bat  # Helper CLI
└── run_lokbot_gui.bat  # Helper GUI
```

---

## 🔧 Phương pháp 2: Cross-compile từ macOS/Linux

### Sử dụng Docker với Windows container:

```bash
# Tạo Dockerfile cho Windows build
cat > Dockerfile.windows << 'EOF'
# escape=`
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Install Python
ADD https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe C:\python-installer.exe
RUN C:\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

# Set working directory
WORKDIR C:\app

# Copy source code
COPY . .

# Install dependencies
RUN pip install fire loguru tenacity schedule ratelimit numpy httpx pyjwt arrow python-socketio python-engineio pyinstaller

# Build
RUN python build.py

# Copy output
CMD ["cmd"]
EOF

# Build Docker image
docker build -f Dockerfile.windows -t lokbot-windows-builder .

# Run container và copy files ra
docker run --rm -v ${PWD}/dist-windows:/output lokbot-windows-builder cmd /c "xcopy C:\app\dist\*.exe C:\output\ /Y"
```

---

## 🔧 Phương pháp 3: Sử dụng GitHub Actions (Tự động)

Tạo file `.github/workflows/build-windows.yml`:

```yaml
name: Build Windows Executables

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-windows:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install fire loguru tenacity schedule ratelimit numpy httpx pyjwt arrow python-socketio python-engineio pyinstaller

      - name: Build executables
        run: |
          python build.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-executables
          path: |
            dist/*.exe
            dist/*.bat
```

---

## 🔧 Phương pháp 4: Wine (Linux/macOS)

```bash
# Cài Wine
# macOS: brew install wine
# Ubuntu: sudo apt install wine

# Cài Python trong Wine
winetricks python310

# Build với Wine
wine python build.py
```

---

## 📋 Build Script được cập nhật

File `build.py` đã được cập nhật để:

- ✅ Detect Windows/macOS/Linux tự động
- ✅ Tạo đúng extension (.exe trên Windows)
- ✅ Build cả CLI và GUI version
- ✅ Tạo batch files helper

---

## 🚀 Cách sử dụng trên Windows

### CLI Version:

```cmd
# Chạy trực tiếp
lokbot.exe YOUR_X_ACCESS_TOKEN

# Hoặc dùng batch file
run_lokbot_cli.bat YOUR_TOKEN
```

### GUI Version:

```cmd
# Double-click lokbot-gui.exe
# Hoặc chạy từ command line
lokbot-gui.exe

# Hoặc dùng batch file
run_lokbot_gui.bat
```

---

## 🛠️ Troubleshooting Windows

### Lỗi "Missing DLL":

```cmd
# Cài Visual C++ Redistributable
# Download từ Microsoft
```

### Lỗi Windows Defender:

```cmd
# Thêm exception cho thư mục dist/
# Hoặc upload file lên VirusTotal để scan
```

### File quá lớn:

```cmd
# Sử dụng UPX để nén
pip install upx-python
# Hoặc download UPX binary
```

### Lỗi import modules:

- Đảm bảo tất cả dependencies đã được cài
- Kiểm tra hidden imports trong .spec file
- Thêm `--collect-all package_name` nếu cần

---

## 📦 Kết quả cuối cùng

Sau khi build thành công trên Windows:

```
dist/
├── lokbot.exe              # ~20MB - CLI version
├── lokbot-gui.exe          # ~22MB - GUI version
├── run_lokbot_cli.bat      # Helper script
└── run_lokbot_gui.bat      # Helper script
```

### Tính năng:

- ✅ Chạy độc lập không cần Python
- ✅ GUI quản lý multiple tokens
- ✅ Config editor cho từng profile
- ✅ Real-time logs
- ✅ Cross-platform compatible

---

## 💡 Tips

1. **Build trên Windows** để đảm bảo compatibility tốt nhất
2. **Test trên máy sạch** (không có Python) để verify
3. **Scan antivirus** trước khi phân phối
4. **Tạo installer** bằng NSIS hoặc Inno Setup nếu cần
5. **Digital signature** để tránh Windows SmartScreen

**Khuyến nghị: Sử dụng Phương pháp 1 (build trực tiếp trên Windows) để có kết quả tốt nhất!** 🪟✨
