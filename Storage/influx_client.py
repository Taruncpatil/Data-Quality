from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "8zzPFueALGRhTaMcDaHK9OUoJDuSY1hXS4-PkBH6qP6yG8ixZZeT2IJWr4jC_D21zwIqJPdFfiG5SYwm8k2BAg=="
INFLUX_ORG = "project"
INFLUX_BUCKET = "quality"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def write_telemetry(data, quality_result):
    point = (
        Point("telemetry")
        .tag("device_id", data["device_id"])
        .tag("quality_status", quality_result["quality_status"])
        .field("temperature", data.get("temperature"))
        .field("humidity", data.get("humidity"))
        .field("quality_reason", quality_result["quality_reason"])
        .time(data["timestamp"])
    )

    write_api.write(
        bucket=INFLUX_BUCKET,
        org=INFLUX_ORG,
        record=point
    )
