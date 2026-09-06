import psutil


def check_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "username", "exe", "status"]
    ):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes


def find_suspicious_processes(processes):
    suspicious = []

    suspicious_locations = [
        "\\temp\\",
        "\\tmp\\"
    ]

    for process in processes:
        exe_path = process.get("exe")

        if exe_path:
            exe_path = exe_path.lower()

            for location in suspicious_locations:
                if location in exe_path:
                    suspicious.append(process)
                    break

    return suspicious

def check_listening_ports():
    connections = psutil.net_connections(kind="inet")

    listening_ports = []

    for connection in connections:
        if connection.status == psutil.CONN_LISTEN:
            process_name = None

            if connection.pid:
                try:
                    process_name = psutil.Process(connection.pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    process_name = "Unknown"
            listening_ports.append({
                "ip": connection.laddr.ip,
                "port": connection.laddr.port,
                "pid": connection.pid,
                "process_name": process_name
            })

    return listening_ports


def analyze_listening_ports(listening_ports):
    ports_to_review = {
        21: {
            "service": "FTP",
            "severity": "MEDIUM",
            "reason": "FTP may transmit credentials and data without encryption.",
            "recommendation": "Verify FTP is required and prefer SFTP or FTPS."
        },
        23: {
            "service": "Telnet",
            "severity": "HIGH",
            "reason": "Telnet transmits traffic without encryption.",
            "recommendation": "Disable Telnet and use SSH instead."
        },
        139: {
            "service": "NetBIOS",
            "severity": "MEDIUM",
            "reason": "NetBIOS exposes Windows file-sharing related services.",
            "recommendation": "Verify file sharing is required and restrict network exposure."
        },
        445: {
            "service": "SMB",
            "severity": "MEDIUM",
            "reason": "SMB is a commonly targeted Windows network service.",
            "recommendation": "Verify SMB is required and restrict access with firewall rules."
        },
        3389: {
            "service": "RDP",
            "severity": "HIGH",
            "reason": "RDP exposes remote desktop access.",
            "recommendation": "Restrict RDP access and require strong authentication."
        }
    }

    findings = []

    for connection in listening_ports:
        port = connection["port"]

        if port in ports_to_review:
            rule = ports_to_review[port]

            findings.append({
                "port": port,
                "service": rule["service"],
                "severity": rule["severity"],
                "reason": rule["reason"],
                "recommendation": rule["recommendation"],
                "process_name": connection["process_name"],
                "pid": connection["pid"],
                "ip": connection["ip"]
            })

    return findings

if __name__ == "__main__":
    process_data = check_processes()
    suspicious_processes = find_suspicious_processes(process_data)

    print("Suspicious processes:")
    for process in suspicious_processes:
        print(process)

    listening_ports = check_listening_ports()

    print("\nListening ports:")
    for port in listening_ports:
        print(port)

    port_findings = analyze_listening_ports(listening_ports)

    print("\nPorts requiring review:")
    for finding in port_findings:
        print(finding)