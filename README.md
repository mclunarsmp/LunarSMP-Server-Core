<p align="center">
  <img width="512px" height="auto" src="./assets/header.png" alt="LunarSMP Banner"/><br/>
  <i>Bí ý tưởng quá nên lấy Blue Archive</i>
</p>

<h1 align="center">🌙 LunarSMP Server Core</h1>

<p align="center">
  <strong>Repo chứa tất cả file config và nhân server của LunarSMP</strong><br/>
  <i>Server Minecraft Survival, SMP & RPG với cộng đồng vui vẻ!</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Minecraft-1.20+-brightgreen" alt="Minecraft Version"/>
  <img src="https://img.shields.io/badge/Server-Paper%2FSpigot-blue" alt="Server Type"/>
  <img src="https://img.shields.io/github/license/mclunarsmp/LunarSMP-Server-Core" alt="License"/>
  <img src="https://img.shields.io/github/stars/mclunarsmp/LunarSMP-Server-Core" alt="Stars"/>
</p>

---

## 📖 Giới thiệu

**LunarSMP** từng là một server sinh tồn với chế độ chơi **SMP và RPG**, nơi quy tụ cộng đồng vui vẻ, mod tích cực và đầy niềm vui! 
**README này được tạo bằng AI! Vui lòng kiểm tra thông tin trước khi chạy**

Repo này được tạo ra để **chia sẻ cấu hình và core server** cho những ai muốn:
- 🏠 Tự host server riêng cho bản thân hoặc nhóm bạn
- 🔧 Học hỏi cách setup và config một Minecraft server
- 🎮 Trải nghiệm gameplay tương tự LunarSMP

---

## ✨ Tính năng nổi bật

- ⚡ **Tối ưu hiệu suất** với Aikars Flags
- 🔌 **Plugin đầy đủ** cho trải nghiệm SMP/RPG hoàn chỉnh
- 🛠️ **Cấu hình sẵn sàng** - clone và chạy ngay
- 📦 **Dễ dàng tùy chỉnh** theo ý muốn
- 🌐 **Hỗ trợ cộng đồng** từ team LunarSMP

---

## 📁 Cấu trúc thư mục

```
LunarSMP-Server-Core/
├── 📄 server.jar                 # File nhân server (Paper/Spigot)
├── 📄 eula.txt                   # End User License Agreement
├── 📄 server.properties          # Cấu hình server chính
├── 📄 bukkit.yml                 # Cấu hình Bukkit
├── 📄 spigot.yml                 # Cấu hình Spigot
├── 📄 paper.yml                  # Cấu hình Paper (nếu dùng Paper)
├── 📄 start.sh                   # Script khởi động (Linux/macOS)
├── 📄 start.bat                  # Script khởi động (Windows)
├── 📄 README.md                  # File này
├── 📄 LICENSE                    # Giấy phép
│
├── 📂 plugins/                   # Thư mục chứa plugins
│   ├── EssentialsX.jar
│   ├── Vault.jar
│   ├── LuckPerms.jar
│   ├── WorldEdit.jar
│   ├── WorldGuard.jar
│   └── ...
│
├── 📂 world/                     # Thế giới chính (Overworld)
│   ├── data/
│   ├── region/
│   ├── playerdata/
│   └── level.dat
│
├── 📂 world_nether/              # Thế giới Nether
│   └── ...
│
├── 📂 world_the_end/             # Thế giới The End
│   └── ...
│
├── 📂 logs/                      # File log của server
│   └── latest.log
│
├── 📂 assets/                    # Tài nguyên (ảnh, banner, etc.)
│   └── header.png
│
└── 📂 config/                    # Cấu hình của các plugins
    ├── EssentialsX/
    ├── LuckPerms/
    ├── WorldGuard/
    └── ...
```

> **Lưu ý**: Các thư mục `world/`, `world_nether/`, `world_the_end/` sẽ được tạo tự động khi server chạy lần đầu.

---

## 📋 Yêu cầu hệ thống

Trước khi bắt đầu, hãy đảm bảo server của bạn đáp ứng:

| Thành phần | Yêu cầu tối thiểu | Khuyến nghị |
|------------|-------------------|-------------|
| **RAM** | 4GB | 6GB+ |
| **CPU** | 2 cores | 4+ cores |
| **Dung lượng** | 10GB | 20GB+ |
| **Java** | Java 17+ | Java 21 |
| **OS** | Linux/Windows | Linux (Ubuntu 20.04+) |

---

## 🚀 Cách cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/mclunarsmp/LunarSMP-Server-Core.git
cd LunarSMP-Server-Core
```

### Bước 2: Cài đặt Java (nếu chưa có)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openjdk-21-jdk
```

**Windows:**  
Tải Java 21 từ [Adoptium](https://adoptium.net/)

### Bước 3: Chạy server

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```batch
start.bat
```

**Hoặc chạy thủ công với lệnh tối ưu:**
```bash
java -Xms4096M -Xmx4096M \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar server.jar --nogui
```

### Bước 4: Chấp nhận EULA

Lần chạy đầu tiên, server sẽ tạo file `eula.txt`. Mở file này và đổi:
```
eula=false
```
thành:
```
eula=true
```

Sau đó chạy lại server.

---

## ⚙️ Cấu hình

### Điều chỉnh RAM

Thay đổi giá trị `-Xms` (RAM tối thiểu) và `-Xmx` (RAM tối đa):
- **4GB RAM**: `-Xms4096M -Xmx4096M`
- **8GB RAM**: `-Xms8192M -Xmx8192M`
- **16GB RAM**: `-Xms16384M -Xmx16384M`

### Cấu hình server

- **server.properties**: Cấu hình cơ bản (port, gamemode, difficulty, etc.)
- **spigot.yml**: Cấu hình Spigot
- **bukkit.yml**: Cấu hình Bukkit
- **paper.yml**: Cấu hình Paper (nếu dùng Paper)
- **plugins/**: Thư mục chứa các plugin

### Port mặc định

Server mặc định chạy trên port **25565**. Để thay đổi, chỉnh sửa trong `server.properties`:
```properties
server-port=25565
```

---

## 🔌 Plugins đi kèm

Repo này bao gồm các plugin thiết yếu cho trải nghiệm LunarSMP:

- **EssentialsX**: Lệnh cơ bản và tiện ích
- **Vault**: API cho economy và permissions
- **LuckPerms**: Quản lý quyền hạn
- **WorldEdit/WorldGuard**: Chỉnh sửa và bảo vệ thế giới
- *(và nhiều plugin khác - xem trong thư mục plugins/)*

> **Lưu ý**: Kiểm tra tương thích phiên bản plugin với Minecraft server của bạn.

---

## 🛠️ Troubleshooting

### Server không khởi động được

**Vấn đề**: Thiếu Java hoặc phiên bản không tương thích
```bash
# Kiểm tra Java version
java -version
```

**Giải pháp**: Cài đặt Java 17 trở lên

### Lỗi "Cannot bind to port"

**Vấn đề**: Port 25565 đã được sử dụng

**Giải pháp**: 
- Đóng các server Minecraft khác
- Hoặc đổi port trong `server.properties`

### RAM không đủ

**Vấn đề**: Server lag hoặc crash

**Giải pháp**:
- Tăng RAM được cấp phát
- Tối ưu plugins (tắt plugin không cần thiết)
- Giảm view-distance trong `server.properties`

---

## 📚 Tài liệu tham khảo

- [Paper Documentation](https://docs.papermc.io/)
- [Spigot Wiki](https://www.spigotmc.org/wiki/)
- [Aikar's Flags Explained](https://docs.papermc.io/paper/aikars-flags)
- [Server Optimization Guide](https://github.com/YouHaveTrouble/minecraft-optimization)

---

## 🤝 Đóng góp

Chúng tôi luôn chào đón mọi đóng góp! Nếu bạn muốn:

1. 🍴 Fork repo này
2. 🌿 Tạo branch mới (`git checkout -b feature/TinhNangMoi`)
3. 💾 Commit thay đổi (`git commit -m 'Thêm tính năng mới'`)
4. 📤 Push lên branch (`git push origin feature/TinhNangMoi`)
5. 🔀 Tạo Pull Request

### Contributors

Cảm ơn những người đã đóng góp vào project này! ❤️

<a href="https://github.com/mclunarsmp/LunarSMP-Server-Core/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mclunarsmp/LunarSMP-Server-Core" alt="Contributors"/>
</a>

---

## 📜 License

Project này được phát hành dưới [MIT License](LICENSE).

---

## ⚠️ Disclaimer

- Repo này được chia sẻ với mục đích **học tập và giải trí**
- Vui lòng **tôn trọng quyền tác giả** của các plugin đi kèm
- Chúng tôi **không chịu trách nhiệm** về việc sử dụng code này cho mục đích thương mại hoặc vi phạm

---

<p align="center">
  <strong>⭐ Nếu thấy hữu ích, hãy cho chúng tôi một star nhé! ⭐</strong><br/>
  Made with ❤️ by LunarSMP Team
</p>
