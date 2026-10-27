from flask import Flask, render_template, jsonify, redirect, url_for
app = Flask(__name__)

from system_health import check_cpu, check_memory, check_disk, check_network, check_uptime
from security_checks import check_processes, find_suspicious_processes, check_listening_ports, analyze_listening_ports
from json_report_generator import generate_json_report
from report_generator import generate_text_report
from baseline_manager import load_baseline, compare_listening_ports


@app.route("/api/health")
def api_health():
    cpu_data = check_cpu()
    memory_data = check_memory()
    disk_data = check_disk()

    return jsonify({
        "cpu": cpu_data,
        "memory": memory_data,
        "disk": disk_data
    })


def collect_monitoring_data():
    cpu_data = check_cpu()
    memory_data = check_memory()
    disk_data = check_disk()
    network_data = check_network()
    uptime_data = check_uptime()

    process_data = check_processes()
    suspicious_data = find_suspicious_processes(process_data)

    listening_ports = check_listening_ports()
    port_findings = analyze_listening_ports(listening_ports)

    baseline_data = load_baseline()

    if baseline_data is not None:
        previous_ports = baseline_data.get("listening_ports", [])
        port_changes = compare_listening_ports(
            previous_ports, listening_ports
        )
    else:
        port_changes = {
            "new_ports": [],
            "removed_ports": []
        }

    return {
        "cpu": cpu_data,
        "memory": memory_data,
        "disk": disk_data,
        "network": network_data,
        "uptime": uptime_data,
        "processes": process_data,
        "suspicious": suspicious_data,
        "ports": listening_ports,
        "port_findings": port_findings,
        "port_changes": port_changes
    }



@app.route("/")
def home():
    data = collect_monitoring_data()

    uptime_delta = data["uptime"]["system_uptime"]

    days = uptime_delta.days
    hours = uptime_delta.seconds // 3600
    minutes = (uptime_delta.seconds % 3600) // 60

    return render_template(
        "dashboard.html",
        cpu=data["cpu"],
        memory=data["memory"],
        disk=data["disk"],
        network=data["network"],
        uptime=data["uptime"],
        processes=data["processes"],
        suspicious=data["suspicious"],
        ports=data["ports"],
        port_findings=data["port_findings"],
        days=days,
        hours=hours,
        minutes=minutes
    )

@app.route("/generate-reports", methods=["POST"])
def generate_reports():
    data = collect_monitoring_data()

    generate_text_report(
        data["cpu"],
        data["memory"],
        data["disk"],
        data["network"],
        data["uptime"],
        data["processes"],
        data["suspicious"],
        data["ports"],
        data["port_findings"],
        data["port_changes"]
    )

    generate_json_report(
        data["cpu"],
        data["memory"],
        data["disk"],
        data["network"],
        data["uptime"],
        data["processes"],
        data["suspicious"],
        data["ports"],
        data["port_findings"],
        data["port_changes"]
    )

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )