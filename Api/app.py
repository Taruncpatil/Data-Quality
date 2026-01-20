from flask import Flask, request, jsonify
from Data_quality.evaluator import evaluate_data_quality

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest_data():
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    quality_result = evaluate_data_quality(data)

    if not quality_result["valid"]:
        return jsonify({
            "status": "rejected",
            "reason": quality_result["reason"]
        }), 400

    return jsonify({
        "status": "accepted",
        "message": "Data passed quality checks"
    }), 200



