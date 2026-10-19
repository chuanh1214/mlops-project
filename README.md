# 🚀 MLOps FastAPI & AutoML Project

Dự án MLOps cá nhân được xây dựng bằng **FastAPI**, kết nối cơ sở dữ liệu NoSQL **MongoDB** (bất đồng bộ qua **Motor**), tích hợp pipeline **Tiền xử lý dữ liệu tự động** và luồng **AutoML Training** với **Scikit-learn**, toàn bộ được đóng gói và vận hành qua **Docker & Docker Compose**.

---

## 📌 1. Các tính năng chính (Key Features)

* **Data Management API**: Upload tệp CSV, xem danh sách file đã tải lên và truy xuất chi tiết Metadata cùng 10 dòng dữ liệu mẫu (Sample Preview).
* **MongoDB Integration**: Lưu trữ và đồng bộ Metadata của các tập dữ liệu, lịch sử huấn luyện mô hình một cách bất đồng bộ (`Motor`).
* **Automated Data Preprocessing**:
  * **Xử lý giá trị thiếu (Missing values)**: Điền giá trị trung bình (`mean`) cho cột số và giá trị xuất hiện nhiều nhất (`mode`) cho cột phân loại.
  * **Mã hóa (Encoding)**: Chuyển đổi các cột dữ liệu phân loại/dạng chữ sang dạng số (`LabelEncoder`).
  * **Chuẩn hóa (Normalization / Standardization)**: Đưa các đặc trưng số về cùng khoảng giá trị (`StandardScaler` / `MinMaxScaler`).
* **AutoML Training Workflow**:
  * Tự động nhận diện loại bài toán Machine Learning: **Phân loại (Classification)** hoặc **Hồi quy (Regression)** dựa trên thuộc tính của cột nhãn (`target_column`).
  * Tự động huấn luyện mô hình **Random Forest** (Classifier/Regressor) và đánh giá độ chính xác (`Accuracy` hoặc `MSE`).
  * Tự động ghi lại kết quả huấn luyện vào MongoDB collection `training_history`.
* **Dockerized Deployment**: Đóng gói hoàn chỉnh ứng dụng FastAPI và CSDL MongoDB thành các container độc lập, sẵn sàng triển khai.

---

## 📂 2. Cấu trúc thư mục (Directory Structure)

```text
mlops_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entrypoint chính của ứng dụng FastAPI
│   ├── config.py                # Cấu hình kết nối MongoDB (AsyncMotorClient)
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_model.py        # Các Pydantic Schema cho Request/Response
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── data_router.py       # API Router: Upload, List, Detail Data
│   │   └── automl_router.py     # API Router: AutoML Training
│   └── services/
│       ├── __init__.py
│       ├── data_service.py      # Logic lưu file local & sync MongoDB Metadata
│       ├── preprocessing_service.py # Pipeline làm sạch, mã hóa & chuẩn hóa dữ liệu
│       └── automl_service.py    # Logic huấn luyện mô hình ML tự động
├── uploads/                     # Thư mục lưu trữ các tệp CSV được upload
├── Dockerfile                   # File đóng gói Docker cho FastAPI App
├── docker-compose.yml           # Quản lý & khởi chạy đồng thời FastAPI App + MongoDB
├── requirements.txt             # Danh sách thư viện Python (đã ghim phiên bản)
└── .gitignore                   # Cấu hình bỏ qua pycache, venv và file rác