from flask import Flask, jsonify, render_template_string
import psutil
import platform
import os

app = Flask(__name__)

# Basic System Info
def get_sys_info():
    return {
        "os": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "cpu_count": psutil.cpu_count(),
        "cpu_freq": f"{psutil.cpu_freq().max:.2f}MHz" if psutil.cpu_freq() else "N/A"
    }

@app.route('/api/stats')
def stats():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": int(psutil.boot_time())
    })

@app.route('/api/processes')
def processes():
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procs.append(proc.info)
        except:
            continue
    # Sort by CPU and get top 5
    top_procs = sorted(procs, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]
    return jsonify(top_procs)

@app.route('/')
def index():
    return render_template_string(open('index.html').read(), sys=get_sys_info())

if __name__ == '__main__':
    app.run(port=5005, debug=True)
