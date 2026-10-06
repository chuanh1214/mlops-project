import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from app.config import get_database

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

class AutoMLService:
    @staticmethod
    async def train_model(filename: str, target_column: str) -> dict:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            return {"error:" "Không tìm thấy file dữ liệu trên hệ thống!"}

        #Đọc dữ liệu bằng Pandas
        try:
            df = pd.read_csv(file_path, encoding = 'utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding = 'latin1')

        if target_column not in df.columns:
            return {"error": f"Cột mục tiêu '{target_column}' không tồn tại trong dataset!"}

        #Tiền xử lý cơ bản: Xóa các dòng thiếu giá trị ở cột target, chọn các cột số (numeric) làm feature
        df = df.dropna(subset = [target_column])
        X = df.select_dtypes(include=['number']).drop(columns=[target_column], errors='ignore')
        y = df[target_column]

        if X.empty:
            return {"error": "Không tìm thấy cột dữ liệu dạng số (numeric features) phù hợp để huấn luyện!"}

        #Chia train/test split (80/20)
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=42)

        #Tự động nhận diện bài toán (Classification hay Regression) dựa trên kiểu dữ liệu của y
        is_classification = y.nunique() < 20 or y.dtype == 'object' or pd.api.types.is_categorical_dtype(y)

        if is_classification:
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            metric_name = "Accuracy"
        else:
            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = mean_squared_error(y_test, y_pred)
            metric_name = "MSE"

        #Lưu kết quả huấn luyện vào MongoDB
        db = get_database()
        train_result = {
            "filename": filename,
            "target_column": target_column,
            "task_type": "Classification" if is_classification else "Regression",
            "metric_name": metric_name,
            "score": float(score),
            "feartures_used": list(X.columns)
        }

        await db["training_history"].insert_one(train_result)
        #Loại bỏ _id để trả về JSON an toàn
        train_result.pop("_id", None)

        return{
            "message": "Huấn luyện mô hình AutoML thành công!",
            "details": train_result
        }