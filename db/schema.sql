CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    value NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);
 
CREATE INDEX IF NOT EXISTS idx_readings_sensor_id ON readings(sensor_id);
CREATE INDEX IF NOT EXISTS idx_readings_recorded_at ON readings(recorded_at DESC);
