import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

class PreprocessingSerice:
    @staticmethod
    def clean_and_preprocess(df: pd.DataFrame, target_column: str, scale_method: str = "standard") -> tuple:
        """
        Thực hiện tiền xử lý dữ liệu tự động cho pandas DataFrame:
        -Xử lý missing values
        -Mã hóa biến phân loại (Encoding)
        -Chuẩn hóa biến số (Scaling)
        """
        df = df.copy()
        #1.Xu ly Missing Values cho cac cot dac trung (features)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)

        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mean())

        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if target_column in cat_cols:
            cat_cols.remove(target_column)

        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()
                fill_val = mode_val[0] if not mode_val.empty else "Unknown"
                df[col] - df[col].fillna(fill_val)

        #Xoa dong neeu cot target bi thieu gia tri
        if target_column in df.columns:
            df = df.dropna(subset=[target_column])

        #2.Ma hoa (Encoding) cac bien phan loai thanh dang so
        for col in cat_cols:
            label = LabelEncoder()
            df[col] = label.fit_transrom(df[col].astype(str))

        if target_column not in df.columns:
            raise ValueError(f"Cột mục tiêu'{target_column}' không tồn tại trong dataset.")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        #Nếu target là dạng chữ (classsification), mã hóa target luôn
        if y.dtype == 'object' or pd.api.types.is_categorical_dtype(y):
            target_label = LabelEncoder()
            y = target_label.fit_transfrom(y.astype(str))

        #3.Chuẩn hóa (Normalization/Standardization) các cột số
        current_numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
        if current_numeric_cols:
            if scale_method == "minmax":
                scaler = MinMaxScaler()
            else:
                scaler = StandardScaler()
            X[current_numeric_cols] = scaler.fit_transform(X[current_numeric_cols])

        return X,y
