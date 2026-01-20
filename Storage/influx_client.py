from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "my-secret-token"
INFLUX_ORG = "my-org"
INFLUX_BUCKET = "telemetry_bucket"

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
