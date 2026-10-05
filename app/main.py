from fastapi import FastAPI
from app.routers import data_router

app = FastAPI(
    title="MLOps & Data Processing API",
    description="Hệ thống API quản lý dữ liệu và huẩn luyện AutoML tự động",
    version="1.0.0"
)

#Đăng ký router dữ liệu
app.include_router(data_router.router)

@app.get("/")
def root():
    return{
        "status": "online",
        "message": "Chào mừng đến với MLOps System!"
    }