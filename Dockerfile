# Sử dụng image Python nhỏ gọn
FROM python:3.12-slim

# Thiết lập thư mục làm việc 
WORKDIR /app

# Copy requirement list và cài đặt trước để cache Docker layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào image
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Chạy Uvicorn server liên kết cổng 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
