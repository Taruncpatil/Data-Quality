from datetime import datetime
from Data_quality.rules import (
    REQUIRED_FIELDS,
    TEMPERATURE_RANGE,
    HUMIDITY_RANGE
)
from datetime import datetime, timezone
from Data_quality.rules import MAX_ALLOWED_DELAY_SECONDS

def check_required_fields(data):
    missing = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            missing.append(field)

    if missing:
        return False, f"Missing fields: {missing}"

    return True, "All required fields present"

def check_timestamp(timestamp_str):
    try:
        datetime.fromisoformat(timestamp_str)
        return True, "Valid timestamp"
    except Exception:
        return False, "Invalid timestamp format"

def check_ranges(data):
    temp = data.get("temperature")
    humidity = data.get("humidity")

    if not (TEMPERATURE_RANGE[0] <= temp <= TEMPERATURE_RANGE[1]):
        return False, "Temperature out of range"

    if not (HUMIDITY_RANGE[0] <= humidity <= HUMIDITY_RANGE[1]):
        return False, "Humidity out of range"

    return True, "Values within range"

def evaluate_data_quality(data):
    checks = []

    checks.append(check_required_fields(data))

    if "timestamp" in data:
        checks.append(check_timestamp(data["timestamp"]))
        checks.append(check_late_arriving_data(data["timestamp"]))

    checks.append(check_ranges(data))

    for result, message in checks:
        if not result:
            return {
                "valid": False,
                "reason": message
            }

    return {
        "valid": True,
        "reason": "Data passed all quality checks"
    }


def check_late_arriving_data(timestamp_str):
    try:
        data_time = datetime.fromisoformat(timestamp_str)
        current_time = datetime.now(timezone.utc)

        delay_seconds = (current_time - data_time).total_seconds()

        if delay_seconds > MAX_ALLOWED_DELAY_SECONDS:
            return False, f"Data arrived late by {int(delay_seconds)} seconds"

        return True, "Data arrived on time"

    except Exception:
        return False, "Invalid timestamp format"



