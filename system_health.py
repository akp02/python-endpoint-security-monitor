from baseline_manager import (
    save_baseline,
    load_baseline,
    compare_listening_ports
)

from event_logger import log_event
from json_report_generator import generate_json_report
from report_generator import generate_text_report

import platform
import socket
import shutil
import psutil

from security_checks import (
    check_processes,
    find_suspicious_processes,
    check_listening_ports,
    analyze_listening_ports,

)     

from datetime import datetime
bytes_per_gb = 1024 ** 3

# Computer name
hostname = socket.gethostname()


# Operating System
os_name = platform.system()
os_version = platform.release()


# CPU
def check_cpu():
    cpu = platform.processor()
    cpu_usage = psutil.cpu_percent(interval=1)
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    warning = None


# CPU Usage
    if cpu_usage > 85:
        print("WARNING: High CPU usage")

    return {
        "cpu_name": cpu,
        "cpu_usage_percent": cpu_usage,
        "physical_cores": physical_cores,
        "logical_cores": logical_cores,
        "warning": warning
    }

# RAM usage
def check_memory():
    memory = psutil.virtual_memory()

    warning = None

    if memory.percent > 85:
        warning = "High Ram Usage"


    return {
        "total_ram_gb": memory.total / bytes_per_gb,
        "used_ram_gb": memory.used / bytes_per_gb,
        "available_ram_gb": memory.available / bytes_per_gb,
        "ram_usage_percent": memory.percent,
        "warning": warning
    }

# Disk usage
def check_disk():
    total, used, free = shutil.disk_usage("C:\\")

    disk_percent = (used / total) * 100

    warning = None

    if disk_percent > 90:
        print("WARNING: Disk space critically low")
    elif disk_percent > 80:
        print("WARNING: Disk space getting low")

    return {
        "total_disk_gb": total / bytes_per_gb,
        "used_disk_gb": used / bytes_per_gb,
        "available_disk_gb": free / bytes_per_gb,
        "disk_percent": disk_percent,
        "warning": warning
    }

# Network Information
def check_network():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    connectivity = "UNKNOWN"

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        connectivity = "ONLINE"

    except OSError:
        connectivity = "OFFLINE"

    return {
        "ip_address": ip_address,
        "connectivity": connectivity,
    }

# System uptime
def check_uptime():
    boot_time = psutil.boot_time()
    boot_datetime = datetime.fromtimestamp(boot_time)

    current_time = datetime.now()
    uptime = current_time - boot_datetime

    return {
        "last_boot_time": boot_datetime,
        "system_uptime": uptime,
    }

def main():
    print("=== SYSTEM HEALTH REPORT ===")
    print(f"Hostname: {hostname}")
    print(f"Operating System: {os_name}")
    print(f"OS Version: {os_version}")


    cpu_data = check_cpu()
    print(f"CPU: {cpu_data['cpu_name']}")
    print(f"CPU Usage: {cpu_data['cpu_usage_percent']:.1f}%")
    print(f"Physical Cores: {cpu_data['physical_cores']}")
    print(f"Logical Cores: {cpu_data['logical_cores']}")

    if cpu_data["warning"]:
        print(cpu_data["warning"])

    memory_data = check_memory()
    print(f"Total Ram: {memory_data['total_ram_gb']:.2f} GB")
    print(f"Used Ram: {memory_data['used_ram_gb']:.2f} GB")
    print(f"Available Ram: {memory_data['available_ram_gb']:.2f} GB")
    print(f"RAM Usage: {memory_data['ram_usage_percent']}%")

    if memory_data["warning"]:
        print(memory_data["warning"])

    disk_data = check_disk()
    print(f"Total Disk Space: {disk_data['total_disk_gb']:.2f} GB")
    print(f"Used Disk Space: {disk_data['used_disk_gb']:.2f} GB")
    print(f"Available Disk Space: {disk_data['available_disk_gb']:.2f} GB")
    print(f"Disk Usage: {disk_data['disk_percent']:.1f}%")

    network_data = check_network()
    print(f"IPv4 Address: {network_data['ip_address']}")
    print(f"Internet Connectivity: {network_data['connectivity']}")

    uptime_data = check_uptime()
    print(f"Last Boot Time: {uptime_data['last_boot_time']}")
    print(f"System Uptime: {uptime_data['system_uptime']}")

    print("============================")


    process_data = check_processes()
    suspicious_processes = find_suspicious_processes(process_data)

    listening_ports = check_listening_ports()
    port_findings = analyze_listening_ports(listening_ports)

    baseline_data = load_baseline()

    if baseline_data is None:
        print("\nNo baseline found. Creating initial baseline...")

        save_baseline({
            "listening_ports": listening_ports
        })

        port_changes = {
            "new_ports": [],
            "removed_ports": []
        }

    else:
        port_changes = compare_listening_ports(
            baseline_data["listening_ports"],
            listening_ports
        )

        print("\n=== BASELINE CHANGES ===")
        print(f"New Listening Ports: {len(port_changes['new_ports'])}")
        print(f"Removed Listening Ports: {len(port_changes['removed_ports'])}")

        for port in port_changes["new_ports"]:
            print(f"[NEW] IP: {port[0]} | Port: {port[1]} | Process: {port[2]}")

        for port in port_changes["removed_ports"]:
            print(f"[REMOVED] IP: {port[0]} | Port: {port[1]} | Process: {port[2]}")

    for port in port_changes["new_ports"]:
        message = (
            f"New listening port detected: "
            f"{port[0]}:{port[1]} owned by {port[2]}"
        )

        print(f"[ALERT] {message}")

        log_event(
            event_type="NEW_LISTENING_PORT",
            severity="MEDIUM",
            message=message,
            details={
                "ip": port[0],
                "port": port[1],
                "process_name": port[2]
            }
        )


    for port in port_changes["removed_ports"]:
        message = (
            f"Listening port removed: "
            f"{port[0]}:{port[1]} owned by {port[2]}"
        )

        print(f"[INFO] {message}")

        log_event(
            event_type="REMOVED_LISTENING_PORT",
            severity="INFO",
            message=message,
            details={
                "ip": port[0],
                "port": port[1],
                "process_name": port[2]
            }
        )

        for finding in port_findings:
            log_event(
                event_type="PORT_REQUIRES_REVIEW",
                severity=finding["severity"],
                message=(
                    f"{finding['service']} detected on port "
                    f"{finding['port']}"
                ),
                details=finding
            )

        for process in suspicious_processes:
            log_event(
                event_type="SUSPICIOUS_PROCESS",
                severity="HIGH",
                message=f"Suspicious process detected: {process['name']}",
                details=process
            )

    print("\n=== SECURITY CHECKS ===")

    print(f"Running Processes: {len(process_data)}")
    print(f"Suspicious Processes: {len(suspicious_processes)}")
    print(f"Listening Ports: {len(listening_ports)}")
    print(f"Ports Requiring Review: {len(port_findings)}")


    generate_text_report(
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
    )

    generate_json_report(
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
    )

if __name__ == "__main__":
    main()
