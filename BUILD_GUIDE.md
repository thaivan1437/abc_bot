# Hướng dẫn Build LokBot thành file .exe

## 🚀 Cách build tự động (Khuyến nghị)

### Bước 1: Chạy script build

```bash
python build.py
```

Script sẽ tự động:

- ✅ Kiểm tra và cài PyInstaller
- ✅ Tạo file cấu hình cần thiết
- ✅ Build file .exe
- ✅ Tạo file helper để chạy dễ dàng

### Bước 2: Sử dụng file .exe

```bash
# Chạy trực tiếp
./dist/lokbot.exe YOUR_X_ACCESS_TOKEN

# Hoặc dùng file batch (Windows)
./dist/run_lokbot.bat YOUR_X_ACCESS_TOKEN
```

---

## 🛠️ Cách build thủ công

### Bước 1: Cài đặt PyInstaller

```bash
pip install pyinstaller
```

### Bước 2: Build với cấu hình cơ bản

```bash
pyinstaller --onefile --console lokbot/__main__.py --name lokbot
```

### Bước 3: Build với cấu hình nâng cao (bao gồm assets)

```bash
pyinstaller --onefile --console \
  --add-data "lokbot/assets:lokbot/assets" \
  --add-data "config.example.json:." \
  --hidden-import lokbot.app \
  --hidden-import lokbot.client \
  --hidden-import lokbot.farmer \
  --hidden-import lokbot.async_farmer \
  --hidden-import engineio.async_drivers.aiohttp \
  --hidden-import socketio.async_client \
  lokbot/__main__.py \
  --name lokbot
```

---

## 📋 Yêu cầu hệ thống

### Để build:

- Python 3.10+
- PyInstaller 5.0+
- Tất cả dependencies trong Pipfile

### Để chạy file .exe:

- Windows 10+ (không cần Python)
- Hoặc Linux/macOS với Wine (nếu build trên Windows)

---

## 🔧 Troubleshooting

### Lỗi thiếu module:

```bash
# Thêm hidden-import khi build
pyinstaller --hidden-import tên_module lokbot.spec
```

### Lỗi thiếu file assets:

```bash
# Thêm data files
pyinstaller --add-data "source_path:dest_path" lokbot.spec
```

### File .exe quá lớn:

```bash
# Sử dụng UPX để nén
pip install upx-python
pyinstaller --upx-dir /path/to/upx lokbot.spec
```

### Lỗi antivirus:

- File .exe có thể bị Windows Defender chặn
- Thêm exception hoặc upload lên VirusTotal để kiểm tra

---

## 📦 Kết quả sau khi build

```
dist/
├── lokbot.exe          # File executable chính
└── run_lokbot.bat      # Helper script để chạy dễ dàng

build/                  # Thư mục build tạm (có thể xóa)
lokbot.spec            # File cấu hình PyInstaller
requirements.txt       # Dependencies list
```

---

## 💡 Tips

1. **Tối ưu kích thước**: Sử dụng `--exclude-module` để loại bỏ modules không cần thiết
2. **Debug**: Dùng `--debug all` để debug khi có lỗi
3. **Cross-platform**: Build trên từng OS để có file executable tương ứng
4. **Testing**: Test file .exe trên máy sạch (không có Python) để đảm bảo hoạt động

---

## 🎯 Sử dụng sau khi build

```bash
# Cách 1: Chạy trực tiếp
lokbot.exe your_x_access_token_here

# Cách 2: Với config file
lokbot.exe your_token --captcha_solver_config config.json

# Cách 3: Dùng batch file (Windows)
run_lokbot.bat your_token
```

File .exe có thể:

- ✅ Chạy độc lập không cần Python
- ✅ Copy sang máy khác để sử dụng
- ✅ Phân phối dễ dàng cho người dùng cuối
- ✅ Giữ nguyên tất cả tính năng của bot
