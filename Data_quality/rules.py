from datetime import datetime

REQUIRED_FIELDS = ["device_id", "timestamp", "temperature", "humidity"]

TEMPERATURE_RANGE = (0, 60)   # Celsius
HUMIDITY_RANGE = (0, 100)

MAX_ALLOWED_DELAY_SECONDS = 120
