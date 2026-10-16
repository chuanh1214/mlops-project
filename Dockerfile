# Sử dụng Python 3.10 chính thức làm base image
FROM python:3.10-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu cần cho pandas/scikit-learn)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép danh sách thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . .

# Tạo sẵn thư mục uploads để lưu file CSV
RUN mkdir -p uploads

# Mở cổng 8000 cho FastAPI
EXPOSE 8000

# Lệnh khởi chạy ứng dụng bằng Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]