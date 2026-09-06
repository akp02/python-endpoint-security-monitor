from datetime import datetime
from pathlib import Path
def generate_text_report(
    cpu_data,
    memory_data,
    disk_data,
    network_data,
    uptime_data,
    process_data,
    suspicious_processes,
    listening_ports,
    port_findings,
    port_changes
):

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = reports_folder / f"system_health_{timestamp}.txt"
    with open(file_path, "w") as report:
        report.write("=== System Health ===\n")
        report.write(f"CPU: {cpu_data['cpu_name']}\n")
        report.write(f"CPU Usage: {cpu_data['cpu_usage_percent']:.1f}%\n")
        report.write(f"Physical Cores: {cpu_data['physical_cores']}\n")
        report.write(f"Logical Cores: {cpu_data['logical_cores']}\n")
        report.write(f"Total RAM: {memory_data['total_ram_gb']:.2f} GB\n")
        report.write(f"Used RAM: {memory_data['used_ram_gb']:.2f} GB\n")
        report.write(f"Available RAM: {memory_data['available_ram_gb']:.2f} GB\n")
        report.write(f"RAM Usage: {memory_data['ram_usage_percent']:.1f}%\n")
        report.write(f"\n--- Disk ---\n")
        report.write(f"Total Disk Space: {disk_data['total_disk_gb']:.2f} GB\n")
        report.write(f"Used Disk Space: {disk_data['used_disk_gb']:.2f} GB\n")
        report.write(f"Available Disk Space: {disk_data['available_disk_gb']:.2f} GB\n")
        report.write(f"Disk Usage: {disk_data['disk_percent']:.1f}%\n")
        report.write(f"\n--- Network ---\n")
        report.write(f"IPv4 Address: {network_data['ip_address']}\n")
        report.write(f"Internet Connectivity: {network_data['connectivity']}\n")
        report.write(f"\n--- Uptime ---\n")
        report.write(f"Last Boot Time: {uptime_data['last_boot_time']}\n")
        report.write(f"System Uptime: {uptime_data['system_uptime']}\n")

        report.write("\n--- Baseline Changes ---\n")

        report.write(
            f"New Listening Ports: {len(port_changes['new_ports'])}\n"
        )

        report.write(
            f"Removed Listening Ports: {len(port_changes['removed_ports'])}\n"
        )

        if port_changes["new_ports"]:
            report.write("\nNew Listening Ports:\n")

            for port in port_changes["new_ports"]:
                report.write(
                    f"- IP: {port[0]} | "
                    f"Port: {port[1]} | "
                    f"Process: {port[2]}\n"
                )

        if port_changes["removed_ports"]:
            report.write("\nRemoved Listening Ports:\n")

            for port in port_changes["removed_ports"]:
                report.write(
                    f"- IP: {port[0]} | "
                    f"Port: {port[1]} | "
                    f"Process: {port[2]}\n"
                )

        report.write(f"\n--- Warnings ---\n")

        if cpu_data["warning"]:
            report.write(f"{cpu_data['warning']}\n")

        if memory_data["warning"]:
            report.write(f"{memory_data['warning']}\n")

        if disk_data["warning"]:
            report.write(f"{disk_data['warning']}\n")

        if not cpu_data["warning"] and not memory_data["warning"] and not disk_data["warning"]:
            report.write("No active warnings.\n")

        report.write("\n--- Security ---\n")
        report.write(f"Running Processes: {len(process_data)}\n")
        report.write(f"Suspicious Processes: {len(suspicious_processes)}\n")
        report.write(f"Listening Ports: {len(listening_ports)}\n")
        report.write(f"Ports Requiring Review: {len(port_findings)}\n")

        if suspicious_processes:
            report.write("\nSuspicious Process Findings:\n")

            for process in suspicious_processes:
                report.write(
                    f"- {process['name']} | "
                    f"PID: {process['pid']} | "
                    f"Path: {process['exe']}\n"
                )

        if port_findings:
            report.write("\nPort Findings:\n")

            for finding in port_findings:
                report.write(
                    f"- [{finding['severity']}] {finding['service']} | "
                    f"Port: {finding['port']} | "
                    f"Process: {finding['process_name']} | "
                    f"PID: {finding['pid']} | "
                    f"IP: {finding['ip']}\n"
                    f"  Reason: {finding['reason']}\n"
                    f"  Recommendation: {finding['recommendation']}\n"
                )
        print(f"TXT report generated: {file_path}")