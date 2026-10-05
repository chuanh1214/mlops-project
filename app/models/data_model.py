from pydantic import BaseModel
from typing import List, Dict, Any

#Model tra ve khi upload file thanh cong
class FileUploadResponse(BaseModel):
    filename:str
    file_path: str
    message: str
    total_rows: int
    columns: List[str]

#Model tra ve danh sach cac file CSV da upload
class DataListResponse(BaseModel):
    total_files: int
    files: List[Dict[str, Any]]