# 🧋 Casso AI Bot - Trợ Lý Ảo Tiệm Trà Sữa Tự Động Hóa (Production Ready)

Dự án này là một **AI Agent** đóng vai "Cô chủ quán" trên Telegram, tích hợp cổng thanh toán trực tuyến và hệ thống quản trị đơn hàng thời gian thực. Giải pháp được thiết kế hướng tới sự chuyên nghiệp, ổn định với khả năng triển khai tức thì trên nền tảng đám mây.

---

## 🕵️ Hướng Dẫn Testing Cho Ban Giám Khảo (Trải Nghiệm 100% Tự Động)

Để đánh giá trọn vẹn sức mạnh của hệ thống, BGK vui lòng thực hiện chu trình kiểm thử sau:

1. **Bước 1 (Giao Tiếp AI)**: Truy cập Bot Telegram @trasuadee_bot và nhắn tin gọi món bằng ngôn ngữ tự nhiên theo kịch bản:

> **Khách hàng:** Cho con gọi món
> 
> **Thư Ký Trà Sữa:** Chào con! 🥰 Cô rất vui khi con muốn đặt hàng tại quán trà sữa của cô! Con thích món gì nào? Cô có menu đây:
> - Trà Sữa Trân Châu Đen (ID: TS01) - Giá M: 35,000 VND, Giá L: 45,000 VND
> - *(... Danh sách món ...)*
> Con hãy cho cô biết món nào, size (M hoặc L), và số lượng nhé! Cô cũng cần tên con, số điện thoại và địa chỉ nhận hàng nữa nhé! 💖
> 
> **Khách hàng:** cho con 2 ly đá xay matcha size M, tên là <Tên của bạn>, <Số điện thoại>, <Địa chỉ nhận hàng>
> 
> **Thư Ký Trà Sữa:** Cảm ơn con! 🥰 Cô đã ghi nhận đơn hàng của con... Con cho cô hỏi là đơn hàng này đã đúng chưa để cô chốt nhé? 🌟
> 
> **Khách hàng:** Đúng rồi ạ
> 
> **Thư Ký Trà Sữa:** Cảm ơn con! 🎉 Cô sẽ chốt đơn hàng của con... Con đợi cô một chút nhé, cô sẽ gửi mã QR cho con ngay bây giờ! 🥳

2. **Bước 2 (Thanh Toán QR)**: Hệ thống AI lập tức sinh ra một **Ảnh mã VietQR** đính kèm đường link thanh toán PayOS trực tiếp vào Telegram:
   > **Thư Ký Trà Sữa:** 🖼 Mã thanh toán đơn hàng đây nha. Bấm vào nút dưới hoặc link sau để thanh toán 76,000 VNĐ nhé! 👉 `https://pay.payos.vn/web/0befd98...`
3. **Bước 3 (Giám Sát Bếp)**: Truy cập trang [Admin Dashboard](https://casso-ai-bot.onrender.com/dashboard).
   *   Mọi đơn hàng vừa tạo sẽ xuất hiện ngay lập tức với trạng thái màu vàng **"Chờ Thanh Toán"**.
4. **Bước 4 (Webhook Real-time)**: Khi thanh toán thành công, trang Dashboard sẽ tự động chuyển sang màu xanh **"Đã Thu Tiền"**. Đồng thời Bot sẽ phản hồi:
   > **Thư Ký Trà Sữa:** ✅ Ting ting! Cô đã nhận được tiền hoá đơn 535283042 của con rồi nhé. Cô đang pha chế rồi, con đợi lát nhé!
5. **Bước 5 (Giao Hàng & Phản Hồi)**: Tại Dashboard, nhấn nút **"🚀 Giao Hàng"**.
   > **Thư Ký Trà Sữa:** 🛵 Alo con ơi! Đơn hàng #535283042 của con đã làm xong và đang được giao nhé! Cầm điện thoại ra lấy đồ uống nha!

---

## 📂 Kiến Trúc Thư Mục (Project Structure)

Dự án được tổ chức theo cấu trúc **Clean Architecture** giúp dễ dàng bảo trì và mở rộng:

```text
casso_ai_bot/
├── app/
│   ├── api/                # Chứa các Endpoint xử lý Request
│   │   ├── dashboard.py    # Logic giao diện quản trị Web
│   │   └── webhooks.py     # Xử lý tín hiệu từ Telegram & PayOS
│   ├── core/               # Cấu hình tập trung (Env, Settings)
│   ├── db/                 # Kết nối CSDL SQLAlchemy
│   ├── models/             # Định nghĩa bảng dữ liệu (PostgreSQL)
│   ├── services/           # Nghiệp vụ lõi (AI, Bot, Payment)
│   │   ├── ai_service.py   # Phân tích ngôn ngữ tự nhiên (OpenAI)
│   │   ├── bot_service.py  # Giao tiếp API Telegram
│   │   └── payment_service.py # Tích hợp SDK PayOS & VietQR
│   ├── templates/          # Giao diện Web Dashboard (HTML/Tailwind)
│   └── main.py             # File khởi chạy ứng dụng chính
├── Dockerfile              # Đóng gói Container sẵn sàng cho Server
├── requirements.txt        # Danh sách thư viện phụ thuộc
└── README.md               # Tài liệu hướng dẫn sử dụng
```

---

## 🚀 Hướng Dẫn Triển Khai (Deployment)

Dự án được cấu hình tối ưu để chạy trên **Render** kết hợp với **PostgreSQL (Neon.tech)**.

### 1. Cấu hình Biến Môi Trường (Environment Variables)
Trên Render, hãy thiết lập các biến sau trong phần **Environment**:
*   `TELEGRAM_TOKEN`: Token lấy từ @BotFather.
*   `OPENAI_API_KEY`: API Key xử lý trí tuệ nhân tạo.
*   `PAYOS_CLIENT_ID`, `PAYOS_API_KEY`, `PAYOS_CHECKSUM_KEY`: Thông số kết nối cổng thanh toán.
*   `DATABASE_URL`: Link kết nối Postgres (Neon.tech). *VD: postgresql://user:pass@ep-xxx...*

### 2. Triển Khai Docker
Kết nối Repository Github với Render và chọn Runtime là **Docker**. Hệ thống sẽ tự động build image và chạy server tại cổng 8000.

### 3. Thiết Lập Webhook
Sau khi Deploy xong, hãy gán URL theo định dạng sau:
*   **Telegram**: `https://api.telegram.org/bot<TOKEN>/setWebhook?url=<URL_RENDER>/webhook/telegram`
*   **PayOS**: Truy cập trang My PayOS và điền Webhook: `<URL_RENDER>/webhook/payos`

---

## 🔨 Công Nghệ Sử Dụng
*   **FastAPI**: Framework hiệu năng cao xử lý API bất đồng bộ (Async).
*   **OpenAI GPT-4o**: Phân tích ngữ nghĩa khách hàng chuyên sâu.
*   **PayOS SDK**: Tích hợp thanh toán ngân hàng mở (VietQR).
*   **PostgreSQL**: Cơ sở dữ liệu quan hệ bảo đảm toàn vẹn dữ liệu.
*   **Docker**: Đảm bảo ứng dụng chạy đồng nhất trên mọi môi trường server.

---
**Ứng viên thực hiện:** Nguyễn Phan Việt Anh
