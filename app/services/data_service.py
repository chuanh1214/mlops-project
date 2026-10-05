import os
import pandas as pd
from pathlib import Path
from fastapi import UploadFile
from app.config import get_database

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DataService:
    @staticmethod
    async def save_and_process_csv(file: UploadFile) -> dict:
        """Lưu file CSV được upload và dùng Pandas đọc metadata nhanh"""
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        #Đọc dữ liệu từ file upload và ghi xuống ổ đĩa
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        #Dùng Pandas đọc file để lấy thông tin dòng/cột
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin1')

        #Chuẩn bị metadata & mẫu dữ liệu (5 dòng đầu)
        db = get_database()
        records = df.head(10).to_dict(orient="records")

        document={
            "filename": file.filename,
            "file_path": str(file_path),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "sample_data": records
        }

        #Lưu metadata vào MongoDB
        await db["datasets"].update_one(
            {"filename": file.filename},
            {"$set": document},
            upsert=True
        )

        return {
            "filename": file.filename,
            "file_path": file_path,
            "message":"Upload file và lưu và MongoDB thành công!",
            "total_rows": len(df),
            "columns": list(df.columns)
        }

    @staticmethod
    def get_uploaded_files() -> dict:
        #Quét thư mục uploads/ và trả về thông tin các file CSV đã có
        files = []
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path) and filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    files.append({
                        "filename": filename,
                        "size_bytes": os.path.getsize(file_path),
                        "total_rows": len(df),
                        "columns": list(df.columns)
                    })

        return {
            "total_files": len(files),
            "files": files
        }
    @staticmethod
    async def get_dataset_details(filename: str) -> dict:
        """Lấy thông tin dữ liệu đã lưu trong MongoDB theo tên file"""
        db = get_database()
        dataset = await db["datasets"].find_one({"filename": filename}, {"_id": 0})
        return dataset