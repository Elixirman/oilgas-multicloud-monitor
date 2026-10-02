from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory store for now — swap for PostgreSQL once DB is up
readings = []


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/ingest", methods=["POST"])
def ingest():
    data = request.get_json(force=True)

    required = ["sensor_id", "value", "unit"]
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400

    reading = {
        "sensor_id": data["sensor_id"],
        "value": data["value"],
        "unit": data["unit"],
        "recorded_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    readings.append(reading)
    del readings[:-100]  # keep last 100

    return jsonify({"status": "received", "reading": reading}), 201


@app.route("/api/readings")
def get_readings():
    return jsonify(list(reversed(readings[-20:])))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
