from flask import Flask, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_URL = os.environ.get("API_URL", "http://localhost:6000")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/readings")
def api_readings():
    try:
        res = requests.get(f"{API_URL}/api/readings", timeout=5)
        rows = res.json()
    except requests.exceptions.RequestException:
        rows = []

    def latest(sensor_id, default=0):
        for r in rows:
            if r["sensor_id"] == sensor_id:
                return r["value"]
        return default

    return jsonify({
        "pressure": latest("PRESS-01"),
        "temperature": latest("TEMP-02"),
        "flow": latest("FLOW-03"),
        "vibration": latest("VIB-04"),
        "rows": rows[:10],
    })


@app.route("/api/status")
def api_status():
    try:
        res = requests.get(f"{API_URL}/health", timeout=3)
        ok = res.status_code == 200
    except requests.exceptions.RequestException:
        ok = False

    return jsonify({
        "tunnel": "CONNECTED" if ok else "DISCONNECTED",
        "link": "AWS <> Azure",
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
