import os
import pandas as pd
from fastapi import UploadFile

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

        return {
            "filename": file.filename,
            "file_path": file_path,
            "message":"Upload file thành công!",
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