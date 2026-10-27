
# Python Endpoint Health & Security Monitor

A Python-based endpoint monitoring and security automation project featuring a command-line monitoring system (V1) and a Flask-powered web dashboard (V2).

The application collects system health metrics, inspects running processes and listening network ports, identifies potential security findings using rule-based checks, compares port activity against a saved baseline, and generates structured TXT and JSON reports.

## Project Versions

### V1 — Command-Line Monitor
The original implementation provides system health checks, process and port inspection, configurable monitoring intervals, event logging, and automated report generation.

### V2 — Web Dashboard
V2 builds on the original monitoring engine with a browser-based interface, live health metric updates, searchable process information, security findings, and one-click TXT/JSON report generation.

The V2 application can also be packaged as a standalone Windows executable using PyInstaller.



## Features

### V1 — Core Monitoring Engine

- CPU, memory, and disk usage monitoring
- Network connectivity and system uptime checks
- Running process enumeration
- Rule-based suspicious process detection
- Listening TCP port inspection
- Port risk analysis
- Persistent listening-port baseline comparison
- Detection of newly opened and removed ports
- Security event logging using JSONL
- TXT and JSON report generation
- Configurable monitoring intervals and thresholds
- Automated recurring scans
- Configuration validation and graceful shutdown handling

### V2 — Web Dashboard

- Flask-powered local web interface
- Dark-themed dashboard with custom CSS
- CPU, memory, and disk health cards
- Periodic health metric updates using a JSON API
- Searchable running-process table
- Suspicious process monitoring summary
- Listening port and security findings tables
- One-click TXT and JSON report generation
- Reusable monitoring data collection
- Windows executable packaging using PyInstaller



## Project Structure

```text
Python-IT-automation/
│
├── dashboard.py               # Flask web application
├── system_health.py           # CPU, memory, disk, network, uptime
├── security_checks.py         # Process and port inspection
├── baseline_manager.py        # Listening-port baseline comparison
├── event_logger.py            # JSONL security event logging
├── report_generator.py        # TXT report generation
├── json_report_generator.py   # JSON report generation
├── scheduler.py               # Automated recurring scans
├── config_manager.py          # Configuration management
├── config.json                # Monitoring settings
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── templates/
│   └── dashboard.html         # Flask dashboard template
│
├── static/
│   └── style.css              # Dashboard styling
│
├── reports/                   # Generated TXT/JSON reports
├── baseline.json              # Runtime port baseline
└── events.jsonl               # Runtime security events
```




## Requirements

- Python 3.11 or later
- Windows 10/11 (tested environment)
- Python dependencies listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/akp02/python-endpoint-security-monitor.git
cd python-endpoint-security-monitor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The application uses `psutil` for system monitoring and Flask for the web dashboard.

PyInstaller is used separately to create a Windows executable.



## Usage

### V2 — Launch the Web Dashboard

Start the Flask application:

```bash
python dashboard.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

The dashboard provides:

- CPU, memory, and disk health metrics
- System uptime and network information
- Searchable running-process information
- Suspicious process findings
- Listening ports and port security findings
- Periodically refreshed system health metrics

### Generate Reports

Click the **Generate TXT & JSON Reports** button at the top of the dashboard.

The application collects monitoring data and generates two reports:

- A human-readable `.txt` report
- A structured `.json` report

Generated reports are saved in the application's `reports/` directory.

### V1 — Run a Single Endpoint Scan

Execute:

```bash
python system_health.py
```

This runs the original command-line monitoring workflow.

### V1 — Run Scheduled Monitoring

Execute:

```bash
python scheduler.py
```

The scheduler performs recurring scans based on the interval configured in `config.json`.

Stop the scheduler using `Ctrl+C`.

### V2 — Windows Executable

V2 can also run as a packaged Windows application.

Launch `EndpointMonitorV2.exe` from the PyInstaller distribution folder, then open:

```text
http://127.0.0.1:5000
```

The executable runs the monitoring dashboard locally without requiring a separate Python installation.

Keep the executable and its bundled support files together.


## Configuration

The monitoring engine uses `config.json` to manage settings for automated scans.

Configuration options include:

- CPU, memory, and disk usage thresholds
- Monitoring interval
- Report output paths
- Security event logging paths

The scheduler reads these settings to determine how frequently monitoring scans should execute.

Configuration validation helps detect missing or invalid settings before monitoring begins.

**Note:** The Flask dashboard currently runs locally at `127.0.0.1:5000`. Its health metrics are collected independently of the scheduler's monitoring interval.



## Output and Reports

The application generates timestamped TXT and JSON monitoring reports.

Example filenames:

```text
reports/
├── system_health_20261026-192200.txt
└── system_health_20261026-192200.json
```

Reports contain system health information and security monitoring results, including:

- CPU, memory, and disk metrics
- Network and uptime information
- Running process information
- Suspicious process findings
- Listening network ports
- Port security findings
- Changes detected against the saved port baseline

TXT reports provide a human-readable summary.

JSON reports provide structured data suitable for further analysis, scripting, or integration with other tools.

In V2, reports can be generated directly from the dashboard using the **Generate TXT & JSON Reports** button.



## Security Monitoring

The Endpoint Security Monitor performs rule-based security checks to identify potentially suspicious system activity.

### Process Monitoring
- Enumerates running processes and their process IDs (PIDs).
- Evaluates processes using predefined suspicious-process rules.
- Displays process information in the V2 dashboard.
- Provides a searchable process table for investigation.

### Network Port Monitoring
- Identifies active listening TCP ports.
- Records associated IP addresses, ports, and process information when available.
- Evaluates listening ports against predefined security review rules.
- Compares current listening ports against a previously saved baseline.
- Identifies newly opened and removed listening ports.

### Security Findings
- Displays suspicious-process summaries and port security findings.
- Records security events using structured JSONL logs.
- Includes security inspection results in generated TXT and JSON reports.

### Detection Limitations
Security findings are heuristic indicators that may require further investigation. A flagged process or port does not necessarily indicate malicious activity.


## Current Limitations

- The dashboard monitors the local machine rather than remote endpoints.
- Security findings use rule-based checks and do not constitute comprehensive malware detection.
- Dashboard health metrics refresh periodically, while other monitoring sections are populated when the page loads.
- The application is intended for local monitoring, learning, and demonstration rather than production endpoint protection.

## Future Development

Potential improvements for future versions include:

- Historical monitoring data and interactive charts
- Configurable security alerts and notifications
- Persistent monitoring history using SQLite
- Remote endpoint monitoring
- Additional Windows security event analysis
- More advanced security detection rules

## Project Status

**V1:** Completed — Command-line monitoring engine and automated scanning.

**V2:** Implemented and locally tested — Flask dashboard, live health metric updates, TXT/JSON report generation, and Windows executable packaging.


