import json
from datetime import datetime
from pathlib import Path

def generate_json_report(cpu_data, memory_data, disk_data, network_data, uptime_data, process_data, suspicious_processes, listening_ports, port_findings, port_changes):
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = reports_folder / f"system_health_{timestamp}.json"

    report_data = {
        "cpu": cpu_data,
        "memory": memory_data,
        "disk": disk_data,
        "network": network_data,
        "uptime": uptime_data,
        "security": {
            "running_processes": len(process_data),
            "suspicious_processes": len(suspicious_processes),
            "listening_ports": listening_ports,
            "ports_requiring_review": port_findings,
        },
        "baseline_changes": {
            "new_listening_ports": [
                {
                    "ip": port[0],
                    "port": port[1],
                    "process_name": port[2]
                }
                for port in port_changes["new_ports"]
            ],

            "removed_listening_ports": [
                {
                    "ip": port[0],
                    "port": port[1],
                    "process_name": port[2]
                }
                for port in port_changes["removed_ports"]
            ]
        }

    }

    report_data["uptime"]["last_boot_time"] = str(
        report_data["uptime"]["last_boot_time"]
    )

    report_data["uptime"]["system_uptime"] = str(
        report_data["uptime"]["system_uptime"]
    )

    report_data["memory"]["total_ram_gb"] = round(report_data["memory"]["total_ram_gb"], 2)
    report_data["memory"]["used_ram_gb"] = round(report_data["memory"]["used_ram_gb"], 2)
    report_data["memory"]["available_ram_gb"] = round(report_data["memory"]["available_ram_gb"], 2)
    report_data["memory"]["ram_usage_percent"] = round(report_data["memory"]["ram_usage_percent"], 1)

    report_data["disk"]["total_disk_gb"] = round(report_data["disk"]["total_disk_gb"], 2)
    report_data["disk"]["used_disk_gb"] = round(report_data["disk"]["used_disk_gb"], 2)
    report_data["disk"]["available_disk_gb"] = round(report_data["disk"]["available_disk_gb"], 2)
    report_data["disk"]["disk_percent"] = round(report_data["disk"]["disk_percent"], 1)

    report_data["cpu"]["cpu_usage_percent"] = round(report_data["cpu"]["cpu_usage_percent"], 1)



    with open(file_path, "w") as report:
        json.dump(report_data, report, indent=4)

        return file_path

