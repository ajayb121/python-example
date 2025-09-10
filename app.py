from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/health")
def health():
    return "ok", 200

@app.get("/config-value")
def get_config_value():
    # Reads MY_CONFIG from environment variables
    value = os.getenv("MY_CONFIG", "default_value")
    return jsonify(config=value)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
