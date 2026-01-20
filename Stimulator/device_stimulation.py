from datetime import datetime,timezone
import json
import time
import random
import requests
from stimulator.simulation_config import DEVICE_IDS, API_ENDPOINT, SEND_INTERVAL_SECONDS

def generate_data(device_id):
    data = {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(20, 40), 2),
        "humidity": round(random.uniform(30, 80), 2)
    }
    return data

def send_data_to_api(data):
    try:
        response = requests.post(API_ENDPOINT, json=data)
        print(f"Sent data: {data} | Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")
        
if __name__ == "__main__":
    print("Starting device simulator...")

    while True:
        for device_id in DEVICE_IDS:
            sensor_data = generate_data(device_id)
            send_data_to_api(sensor_data)

        time.sleep(SEND_INTERVAL_SECONDS)


    
    
    