# 🧋 Casso AI Bot - Trợ Lý Ảo Tiệm Trà Sữa Tự Động Hóa Đa Kênh

Kính gửi Ban Giám Khảo Casso, đây là dự án AI Agent đóng vai "Cô chủ quán Trà sữa" giao tiếp tự nhiên với khách hàng qua Telegram.

Dự án có sự kết hợp hoàn hảo giữa **OpenAI (GPT-4o)** để xử lý ngôn ngữ tự nhiên, hệ thống sinh mã QR thanh toán tĩnh/động từ **PayOS / VietQR**, và lưu trữ dữ liệu thông qua **PostgreSQL (Neon.tech)**. Kèm theo đó là một trang **Web Admin Panel (Dashboard)** phục vụ cho chủ quán quản lý đơn hàng. Toàn bộ hệ thống được đóng gói theo chuẩn Production bằng **Docker**.

---

## 🌟 Demo Phục Vụ Giám Khảo Testing

Dự án đã được deploy trọn vẹn lên server đám mây. Mời BGK trực tiếp trải nghiệm hệ thống theo đường link sau:

- 🤖 **Telegram Bot**: `[Chèn_Link_Bot_Của_Bạn_Vào_Đây]` *(Ví dụ: https://t.me/ten_bot)*
- 🖥️ **Web Admin Dashboard**: `[Chèn_Link_Web_Deploy_Vào_Đây/dashboard]` *(Ví dụ: https://my-bot-casso.onrender.com/dashboard)*

### 📝 Kịch Bản Test Khuyến Nghị
Để trải nghiệm chu trình của một giao dịch thực tế trọn vẹn nhất, BGK vui lòng thực hiện tuần tự:

1. **Bước 1 (Giao tiếp & Đặt món)**: Nhắn tin cho Bot Telegram bắt kỳ câu nào để gọi món (VD: *"Cho con 2 cốc trà sữa trân châu ít đường ít đá mang về địa chỉ Tòa nhà Lotte nhé"*). Quán sẽ hiểu, phản hồi tự nhiên và móc ra danh sách món để tính tiền tổng cộng.
2. **Bước 2 (Thanh toán API)**: Bot sẽ sinh ngay tại trận một ảnh mã **VietQR** chuẩn xác kèm đường link PayOS Checkout. Bạn có thể sử dụng App Ngân hàng (hoặc tính năng thanh toán Sandbox của hệ thống nếu đang test local) để giả lập thanh toán.
3. **Bước 3 (Nhận biến động số dư)**: Sau khi giao dịch chuyển tiền thành công, truy cập vào đường link **Web Admin Dashboard**. Hãy theo dõi hóa đơn ngay lập tức chuyển trạng thái sang **Đã Thu Tiền** (màu xanh).
4. **Bước 4 (Vận chuyển logistics)**: Trong vai cô Chủ quán ở màn hình Dashboard, BGK hãy bấm vào nút Tên lửa **"🚀 Giao Hàng"**.
5. **Bước 5 (Trigger Tin nhắn chăm sóc)**: Sau khi bấm nút tại Dashboard, mở ứng dụng Telegram ra, bạn sẽ thấy con Bot tự động nhắn tin thông báo *"Ting ting, cô đã làm xong trà sữa, con lấy điện thoại ra nhận đồ nhé!"*. Toàn bộ kịch bản E-Commerce được tự động hóa.

---

## 🛠 Công Nghệ Sử Dụng (Tech Stack)

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (ORM), Uvicorn.
- **Frontend Dashboard**: Jinja2 Templates, TailwindCSS v3.
- **AI Processing**: OpenAI API.
- **Ngân Hàng Mở**: Cổng thanh toán mã nguồn mở PayOS, sinh ảnh từ `img.vietqr.io`.
- **Hạ tầng Container**: Docker, PostgreSQL Serverless (Neon.tech), Cloud Rendering (Render).

---

## 💻 Hướng Dẫn Deploy Cho Nhà Phát Triển (Tự Chạy Local)

Nếu bạn muốn clone dự án này về thử nghiệm chạy máy ảo localhost:

1. **Cài Đặt Thư Viện**:
```bash
pip install -r requirements.txt
```

2. **Cấu hình Biến Môi Trường (`.env`)**:
Tạo tệp `.env` với các Keys bắt buộc sau:
```env
TELEGRAM_TOKEN="BOT_TOKEN_CỦA_BẠN"
OPENAI_API_KEY="KEY_API_OPENAI"
PAYOS_CLIENT_ID="MA_PAYOS_CLIENT_ID"
PAYOS_API_KEY="MA_PAYOS_API_KEY"
PAYOS_CHECKSUM_KEY="MA_PAYOS_CHECKSUM_KEY"

# Mặc định sử dụng SQLite cho Local Testing
DATABASE_URL="sqlite:///./orders.db"
```

3. **Khởi Chạy Máy Chủ**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Sau đó truy cập **http://localhost:8000/dashboard** để xem màn hình quản trị.

---

## 🚀 Hướng Dẫn Kéo Lên Server Đám Mây (Render)

Hệ thống được thiết kế theo cấu trúc Containerize nên việc đưa lên bất kỳ hãng Cloud nào cũng rất đơn giản:

1. Thiết lập CSDL thực tế: Đăng ký [Neon.tech](https://neon.tech), tạo kho dữ liệu Postgres và lấy dải Connection thay vào `DATABASE_URL` trong biến môi trường (Lưu ý luôn nối thêm `?sslmode=require` ở đuôi).
2. Tải toàn bộ Source code này lên 1 kho chứa GitHub.
3. Vào dịch vụ [Render](https://render.com), khởi tạo **New Web Service**, kết nối với GitHub. Ở mục `Runtime` buộc phải chọn là **Docker**.
4. Truy cập Web Render, gắn lại các tham số `.env` vào phần Variables. Chờ màn hình Deploy báo `Live`!
5. **Gắn Webhook**: Lấy đường Domain mà Render vừa cấp phát để nạp lại vào cài đặt Webhook của *Telegram BotFather* (Endpoint: `/webhook/telegram`) và Cài đặt *Dashboard PayOS* (Endpoint: `/webhook/payos`).

✨ _Chúc bạn một ngày tràn đầy năng lượng cùng Casso AI Bot!_
