from flask import Flask, request, jsonify
from Data_quality.evaluator import evaluate_data_quality
from storage.influx_client import write_telemetry


app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest_data():
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    quality_result = evaluate_data_quality(data)

    write_telemetry(data, quality_result)

    if not quality_result["valid"]:
        return jsonify({
            "status": "rejected",
            "quality_status": quality_result["quality_status"],
            "quality_reason": quality_result["quality_reason"]
        }), 400

    return jsonify({
        "status": "accepted",
        "quality_status": quality_result["quality_status"],
        "quality_reason": quality_result["quality_reason"]
    }), 200




