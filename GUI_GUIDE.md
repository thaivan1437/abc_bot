# 🤖 LokBot GUI - Hướng dẫn sử dụng

## 📖 Tổng quan

LokBot GUI là giao diện đồ họa cho phép bạn:

- ✅ Quản lý nhiều token (profiles) cùng lúc
- ✅ Chỉnh sửa config cho từng profile riêng biệt
- ✅ Chạy/dừng bot cho từng token độc lập
- ✅ Theo dõi logs realtime
- ✅ Lưu/load cấu hình dễ dàng

---

## 🚀 Cách chạy GUI

### Từ source code:

```bash
python lokbot/gui_main.py
```

### Từ file .exe (sau khi build):

```bash
# Chạy trực tiếp
./dist/lokbot-gui.exe

# Hoặc dùng batch file
./dist/run_lokbot_gui.bat
```

---

## 📋 Giao diện chính

### Tab 1: Token Management

Quản lý profiles và tokens:

#### 🔧 Chức năng chính:

- **New**: Tạo profile mới
- **Delete**: Xóa profile đã chọn
- **Clone**: Sao chép profile (với config giống nhau)
- **Save Profile**: Lưu thông tin profile
- **▶ Start Bot**: Chạy bot cho profile được chọn
- **⏹ Stop Bot**: Dừng bot đang chạy

#### 📝 Thông tin profile:

- **Profile Name**: Tên profile (để phân biệt)
- **X-Access-Token**: Token của tài khoản
- **Status**: Trạng thái bot (Running/Stopped)

#### 💡 Tips:

- Có thể show/hide token bằng checkbox "Show Token"
- Mỗi profile chạy độc lập với config riêng
- Status sẽ tự động cập nhật khi bot chạy/dừng

### Tab 2: Config Editor

Chỉnh sửa cấu hình JSON:

#### 🔧 Chức năng:

- **Load Default**: Load config mặc định
- **Save Config**: Lưu config cho profile được chọn
- **JSON Editor**: Chỉnh sửa config trực tiếp

#### ⚙️ Cấu hình mặc định bao gồm:

- **Alliance Farmer**: Claim gifts, help alliance, research donate
- **Building Farmer**: Auto upgrade buildings
- **Academy Farmer**: Auto research
- **Field Farming**: Tìm và farm crystal mines, goblins

#### 📝 Ví dụ config:

```json
{
  "main": {
    "jobs": [
      {
        "name": "alliance_farmer",
        "enabled": true,
        "kwargs": {
          "gift_claim": true,
          "help_all": true,
          "research_donate": true,
          "shop_auto_buy_item_code_list": [10101008]
        },
        "interval": { "start": 120, "end": 200 }
      }
    ],
    "threads": [
      {
        "name": "building_farmer_thread",
        "enabled": true,
        "kwargs": { "speedup": true }
      }
    ]
  }
}
```

### Tab 3: Logs

Theo dõi hoạt động realtime:

#### 🔧 Chức năng:

- **Clear Logs**: Xóa tất cả logs
- **Save Logs**: Lưu logs ra file .txt
- **Auto Scroll**: Tự động cuộn xuống log mới

#### 🎨 Color coding:

- 🔵 **BLUE**: Bot output messages
- 🔴 **RED**: Error messages
- 🟠 **ORANGE**: Warning messages
- ⚫ **BLACK**: Info messages

---

## 💾 Quản lý Profiles

### Cách tạo profile mới:

1. Click **"New"** trong Token Management
2. Nhập tên profile
3. Nhập X-Access-Token
4. Click **"Save Profile"**

### Cách chỉnh config cho profile:

1. Chọn profile trong Config Editor tab
2. Chỉnh sửa JSON config
3. Click **"Save Config"**

### Cách chạy bot:

1. Chọn profile trong Token Management
2. Click **"▶ Start Bot"**
3. Theo dõi logs trong Logs tab

---

## 🗂️ File lưu trữ

### `profiles.json`

Lưu tất cả thông tin profiles:

```json
{
  "Profile1": {
    "token": "your_token_here",
    "config": {...},
    "status": "Stopped"
  },
  "Profile2": {
    "token": "another_token",
    "config": {...},
    "status": "Running"
  }
}
```

### `config_ProfileName.json`

Config tạm thời cho từng profile khi chạy bot.

---

## ⚠️ Lưu ý quan trọng

### Bảo mật:

- ✅ Tokens được ẩn bằng dấu `*`
- ✅ Profiles.json lưu local, không upload đâu
- ⚠️ **Không chia sẻ file profiles.json** (chứa tokens)

### Performance:

- ✅ Có thể chạy nhiều bot cùng lúc
- ✅ Mỗi bot chạy process riêng
- ⚠️ **RAM usage tăng** khi chạy nhiều bot

### Troubleshooting:

- ❌ **Bot không start**: Kiểm tra token có đúng không
- ❌ **Config lỗi**: Kiểm tra JSON syntax
- ❌ **GUI không mở**: Kiểm tra tkinter đã cài đặt

---

## 🛠️ Advanced Usage

### Chạy nhiều instance:

```bash
# Instance 1: Farm account chính
lokbot-gui.exe

# Instance 2: Farm alt accounts (chạy file khác)
lokbot-gui.exe --config alt_profiles.json
```

### Backup profiles:

```bash
# Backup
copy profiles.json profiles_backup.json

# Restore
copy profiles_backup.json profiles.json
```

### Custom config templates:

Tạo template config cho các loại account khác nhau:

- `config_main_account.json` - Account chính với full features
- `config_farm_account.json` - Alt account chỉ farm resources
- `config_pvp_account.json` - Account PvP với focus troops

---

## 🎯 Best Practices

1. **Đặt tên profile có ý nghĩa**: "Main_Account", "Farm_Alt_1", etc.
2. **Backup profiles thường xuyên** trước khi thay đổi lớn
3. **Test config trên 1 account** trước khi áp dụng cho nhiều account
4. **Monitor logs** để đảm bảo bot hoạt động đúng
5. **Không chạy quá nhiều bot** cùng lúc để tránh lag

---

## 🆘 Support

Nếu gặp vấn đề:

1. Kiểm tra logs trong GUI
2. Thử chạy CLI version để debug
3. Kiểm tra config JSON syntax
4. Restart GUI application

**Happy Botting!** 🤖✨
