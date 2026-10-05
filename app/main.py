from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "devops_demo_http_requests_total",
    "Total number of HTTP requests",
    ["endpoint"]
)

@app.get("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return jsonify({
        "message": "Hello from the DevOps Demo Project!",
        "status": "running",
        "version": "1.0.0"
    })

@app.get("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return jsonify({"status": "healthy"}), 200

@app.get("/metrics")
def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
