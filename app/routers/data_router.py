from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.data_model import DataListResponse, FileUploadResponse
from app.services.data_service import DataService

router = APIRouter(prefix="/api/v1/data", tags=["Data Management"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_csv_file(file: UploadFile = File(...)):
    """API Upload file CSV dữ liệu"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Định dạng file không hợp lệ! Vui lòng chọn file có đuôi .csv"
        )
            
    result = await DataService.save_and_process_csv(file)
    return result

@router.get("/list", response_model=DataListResponse)
def list_uploaded_data():
    """API lấy danh sách thông tin các file dữ liệu đã upload"""
    return DataService.get_uploaded_files()