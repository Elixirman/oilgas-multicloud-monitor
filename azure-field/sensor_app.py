import requests
import random
import time
import os

# Point this at the API's address.
# For now (local test): http://localhost:6000
# Later (real deployment): the API's private IP through the VPN tunnel
API_URL = os.environ.get("API_URL", "http://localhost:6000/api/ingest")

SENSORS = [
    {"sensor_id": "PRESS-01", "unit": "psi", "min": 1400, "max": 1800},
    {"sensor_id": "TEMP-02", "unit": "°C", "min": 55, "max": 75},
    {"sensor_id": "FLOW-03", "unit": "bbl/hr", "min": 250, "max": 400},
    {"sensor_id": "VIB-04", "unit": "mm/s", "min": 1, "max": 5},
]


def generate_and_send():
    for sensor in SENSORS:
        value = round(random.uniform(sensor["min"], sensor["max"]), 2)
        payload = {
            "sensor_id": sensor["sensor_id"],
            "value": value,
            "unit": sensor["unit"],
        }
        try:
            res = requests.post(API_URL, json=payload, timeout=5)
            print(f"Sent {payload} -> {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send {payload}: {e}")


if __name__ == "__main__":
    while True:
        generate_and_send()
        time.sleep(5)
