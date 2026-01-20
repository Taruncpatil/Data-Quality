seen_records = set()

def is_duplicate(device_id, timestamp):
    key = (device_id, timestamp)

    if key in seen_records:
        return True

    seen_records.add(key)
    return False