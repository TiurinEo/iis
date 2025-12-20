import requests
import json
import time
import random
from typing import Dict, Any

def generate_random_patient_data() -> Dict[str, Any]:
    """Генерирует случайные данные пациента для тестирования"""
    return {
        "age": random.uniform(29, 77),
        "sex": random.randint(0, 1),
        "cp": random.randint(0, 3),
        "trestbps": random.uniform(94, 200),
        "chol": random.uniform(126, 564),
        "fbs": random.randint(0, 1),
        "restecg": random.randint(0, 2),
        "thalach": random.uniform(71, 202),
        "exang": random.randint(0, 1),
        "oldpeak": random.uniform(0, 6.2),
        "slope": random.randint(0, 2),
        "ca": random.randint(0, 4),
        "thal": random.randint(0, 3)
    }

def send_prediction_request(base_url: str, item_id: int, patient_data: Dict[str, Any]) -> None:
    """Отправляет запрос на предсказание"""
    try:
        url = f"{base_url}/api/prediction"
        params = {"item_id": item_id}
        
        response = requests.post(url, params=params, json=patient_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Request {item_id}: Prediction = {result.get('predict', 'N/A')}")
        else:
            print(f"✗ Request {item_id}: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request {item_id}: Error - {str(e)}")

def main():
    base_url = "http://ml-prediction-service:8000"
    request_id = 1
    
    print("🚀 Starting prediction service testing...")
    print(f"Target URL: {base_url}")
    print("-" * 50)
    
    try:
        while True:
            patient_data = generate_random_patient_data()
            send_prediction_request(base_url, request_id, patient_data)
            
            request_id += 1
            sleep_time = random.uniform(0, 5)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\n🛑 Testing stopped by user")

if __name__ == "__main__":
    main()