from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import os
 
app = Flask(__name__)
 
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("POSTGRES_DB", "oilgas")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "changeme")
 
 
def get_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
 
 
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
 
 
@app.route("/api/ingest", methods=["POST"])
def ingest():
    data = request.get_json(force=True)
    required = ["sensor_id", "value", "unit"]
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400
 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO readings (sensor_id, value, unit) VALUES (%s, %s, %s) RETURNING id, recorded_at",
        (data["sensor_id"], data["value"], data["unit"]),
    )
    row_id, recorded_at = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
 
    return jsonify({
        "status": "received",
        "reading": {
            "id": row_id,
            "sensor_id": data["sensor_id"],
            "value": data["value"],
            "unit": data["unit"],
            "recorded_at": recorded_at.isoformat(),
        },
    }), 201
 
 
@app.route("/api/readings")
def get_readings():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT sensor_id, value, unit, recorded_at FROM readings ORDER BY recorded_at DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close()
    conn.close()
 
    for r in rows:
        r["recorded_at"] = r["recorded_at"].isoformat()
 
    return jsonify(rows)
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)

