from datetime import datetime
from data_quality.rules import (
    REQUIRED_FIELDS,
    TEMPERATURE_RANGE,
    HUMIDITY_RANGE
)
from datetime import datetime, timezone
from data_quality.rules import MAX_ALLOWED_DELAY_SECONDS
from utils.duplicate_tracker import is_duplicate


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

    checks.append(("missing", check_required_fields(data)))

    if "timestamp" in data:
        checks.append(("timestamp", check_timestamp(data["timestamp"])))
        checks.append(("late", check_late_arriving_data(data["timestamp"])))

    checks.append(("duplicate", check_duplicate(data)))
    checks.append(("range", check_ranges(data)))

    for status, (result, message) in checks:
        if not result:
            return {
                "valid": False,
                "quality_status": status,
                "quality_reason": message
            }

    return {
        "valid": True,
        "quality_status": "valid",
        "quality_reason": "Data passed all quality checks"
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
    
def check_duplicate(data):
    device_id = data.get("device_id")
    timestamp = data.get("timestamp")

    if is_duplicate(device_id, timestamp):
        return False, "Duplicate data detected"

    return True, "Not a duplicate"




