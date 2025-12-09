import pickle
import shutil
from pathlib import Path

def download_model():
    """Копирует модель из MLflow artifacts в текущую директорию"""
    try:
        # Путь к артефактам MLflow
        current_dir = Path(__file__).parent
        eda_dir = current_dir.parent.parent.parent
        
        # Путь к сохраненной модели в MLflow
        mlflow_model_path = eda_dir / "mlflow" / "mlruns" / "1" / "128bd4a48b8e4f38a8a1c186094d85bf" / "artifacts" / "model" / "model.pkl"
        
        print(f"Looking for model at: {mlflow_model_path}")
        print(f"Model exists: {mlflow_model_path.exists()}")
        
        if mlflow_model_path.exists():
            # Копируем файл модели
            shutil.copy2(mlflow_model_path, "model.pkl")
            print("Model successfully copied as model.pkl")
            
            # Проверяем, что модель загружается
            with open("model.pkl", "rb") as f:
                model = pickle.load(f)
            print(f"Model type: {type(model)}")
            
        else:
            print("Model file not found. Checking directory contents:")
            artifacts_dir = mlflow_model_path.parent
            if artifacts_dir.exists():
                print(f"Contents of {artifacts_dir}: {list(artifacts_dir.iterdir())}")
        
    except Exception as e:
        print(f"Error copying model: {e}")
        raise

if __name__ == "__main__":
    download_model()