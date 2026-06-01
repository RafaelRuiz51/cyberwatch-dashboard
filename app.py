from flask import Flask, render_template, jsonify
import psutil
import datetime
import random

app = Flask(__name__)

fake_logs = [
    {"dot": "red", "msg": "FAILED password root", "ip": "192.168.1.104"},
    {"dot": "amber", "msg": "Invalid user admin", "ip": "45.33.32.156"},
    {"dot": "green", "msg": "Accepted publickey", "ip": "10.0.0.5"},
    {"dot": "red", "msg": "FAILED su root", "ip": "172.16.0.99"},
    {"dot": "blue", "msg": "Disconnected by user", "ip": "10.0.0.8"},
    {"dot": "red", "msg": "Connection refused", "ip": "198.51.100.2"},
    {"dot": "green", "msg": "Session opened for root", "ip": "10.0.0.1"},
    {"dot": "amber", "msg": "Invalid user deploy", "ip": "203.0.113.42"},
]

blocked_ips = [
    "192.168.1.104", "45.33.32.156", "172.16.0.99",
    "198.51.100.2", "203.0.113.42", "185.220.101.5",
    "91.108.4.0", "107.189.10.143"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    net = psutil.net_io_counters()
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = str(datetime.datetime.now() - boot).split(".")[0]
    log = random.choice(fake_logs)
    log["time"] = datetime.datetime.now().strftime("%H:%M:%S")
    return jsonify({
        "cpu": cpu,
        "ram": round(ram.percent, 1),
        "ram_used": round(ram.used / (1024**3), 1),
        "ram_total": round(ram.total / (1024**3), 1),
        "uptime": uptime,
        "bytes_sent": round(net.bytes_sent / (1024**2), 1),
        "bytes_recv": round(net.bytes_recv / (1024**2), 1),
        "blocked_count": len(blocked_ips),
        "log": log
    })

@app.route("/api/blocked")
def blocked():
    return jsonify({"ips": blocked_ips})

if __name__ == "__main__":
    app.run(debug=True)