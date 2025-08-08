# 🪟 Hướng dẫn cài đặt LokBot trên Windows

## ❗ Giải quyết lỗi cài dependencies

### 🔧 **Bước 1: Chuẩn bị Windows**

```cmd
# 1. Cài Python 3.8+ từ python.org (QUAN TRỌNG: Check "Add to PATH")
# 2. Mở Command Prompt as Administrator
# 3. Kiểm tra Python
python --version
pip --version
```

### 🔧 **Bước 2: Sử dụng script cài dependencies**

```cmd
cd lok_bot_c7_tieu_la
python install_dependencies.py
```

Script này sẽ:

- ✅ Kiểm tra Python version
- ✅ Upgrade pip tự động
- ✅ Cài từng dependency một cách an toàn
- ✅ Retry nếu có lỗi
- ✅ Verify installation

---

## 🛠️ **Nếu vẫn gặp lỗi, thử các cách sau:**

### **Lỗi 1: "Microsoft Visual C++ 14.0 is required"**

```cmd
# Download và cài Visual Studio Build Tools:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Hoặc Visual Studio Community với C++ workload
```

### **Lỗi 2: "Failed building wheel for numpy"**

```cmd
# Cài numpy từ wheel pre-built
pip install --upgrade pip setuptools wheel
pip install --only-binary=all numpy==1.24.*
```

### **Lỗi 3: "SSL Certificate verify failed"**

```cmd
# Nếu có proxy/firewall
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package>

# Hoặc upgrade certificates
pip install --upgrade certifi
```

### **Lỗi 4: "Permission denied"**

```cmd
# Chạy CMD as Administrator
# Hoặc install cho user hiện tại
pip install --user <package>
```

### **Lỗi 5: "No module named '\_ctypes'"**

```cmd
# Reinstall Python với tất cả components
# Hoặc sử dụng Anaconda Python
```

---

## 🔄 **Cách cài thủ công từng bước:**

### **Bước 1: Cài basic tools**

```cmd
python -m pip install --upgrade pip setuptools wheel
```

### **Bước 2: Cài PyInstaller**

```cmd
pip install pyinstaller>=5.0
```

### **Bước 3: Cài dependencies đơn giản**

```cmd
pip install fire==0.5.*
pip install loguru==0.7.*
pip install tenacity==8.2.*
pip install schedule==1.2.*
pip install ratelimit==2.2.*
pip install arrow==1.2.*
pip install pyjwt==2.7.*
```

### **Bước 4: Cài dependencies phức tạp**

```cmd
# NumPy (có thể mất thời gian)
pip install numpy==1.24.*

# HTTPX
pip install httpx[http2]==0.24.*

# Socket.IO
pip install python-socketio<5
pip install python-engineio
```

### **Bước 5: Verify**

```cmd
python -c "import fire, loguru, numpy, httpx, socketio; print('All OK!')"
```

---

## 🚀 **Sau khi cài dependencies thành công:**

```cmd
# Build executables
python build_windows.py
```

---

## 🔧 **Alternative: Sử dụng Conda**

Nếu pip không work, thử Anaconda:

```cmd
# Download Anaconda/Miniconda
# Tạo environment mới
conda create -n lokbot python=3.10
conda activate lokbot

# Cài dependencies
conda install numpy
pip install fire loguru tenacity schedule ratelimit httpx pyjwt arrow python-socketio python-engineio pyinstaller

# Build
python build_windows.py
```

---

## 🔧 **Alternative: Sử dụng Virtual Environment**

```cmd
# Tạo virtual environment
python -m venv lokbot_env

# Activate
lokbot_env\Scripts\activate

# Cài dependencies
python install_dependencies.py

# Build
python build_windows.py
```

---

## 📋 **Troubleshooting chi tiết:**

### **Lỗi network/proxy:**

```cmd
# Set proxy nếu cần
set HTTP_PROXY=http://proxy:port
set HTTPS_PROXY=http://proxy:port

# Hoặc sử dụng corporate proxy
pip install --proxy http://user:pass@proxy:port <package>
```

### **Lỗi antivirus:**

- Tạm thời tắt real-time protection
- Thêm exception cho Python và pip
- Thêm exception cho thư mục project

### **Lỗi firewall:**

- Cho phép Python.exe và pip.exe qua firewall
- Hoặc sử dụng offline wheels

### **Lỗi disk space:**

- Dọn dẹp pip cache: `pip cache purge`
- Kiểm tra disk space: `dir C:\ /-c`

---

## 🎯 **Kết quả mong đợi:**

Sau khi thành công:

```
dist/
├── lokbot.exe              # CLI version
├── lokbot-gui.exe          # GUI version
├── run_lokbot_cli.bat      # Helper CLI
├── run_lokbot_gui.bat      # Helper GUI
└── install.bat             # Windows installer
```

---

## 💡 **Tips:**

1. **Luôn chạy CMD as Administrator** khi cài dependencies
2. **Kiểm tra Python PATH** - phải có trong system PATH
3. **Tắt antivirus tạm thời** khi build
4. **Sử dụng Python từ python.org** thay vì Microsoft Store
5. **Cài Visual Studio Build Tools** nếu cần compile C extensions

**Nếu vẫn gặp vấn đề, hãy copy paste error message cụ thể để được hỗ trợ!** 🛠️
