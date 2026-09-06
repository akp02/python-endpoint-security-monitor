# Python Endpoint Health & Security Monitor

A Python-based endpoint monitoring and security automation tool that collects system health data, inspects running processes and listening ports, compares activity against a persistent baseline, logs security events, and generates structured TXT and JSON reports.

## Features

- CPU, memory, and disk monitoring
- Network and uptime checks
- Running process enumeration
- Suspicious process detection
- Listening port detection
- Port risk analysis
- Persistent port baseline
- New and removed listening-port detection
- Security event logging with JSONL
- TXT and JSON report generation
- Configurable scan intervals and thresholds
- Automatic recurring scans
- Graceful configuration and shutdown error handling

## Project Structure

```text
system_health.py
security_checks.py
scheduler.py
config_manager.py
config.json
baseline_manager.py
event_logger.py
report_generator.py
json_report_generator.py
baseline.json          # Runtime baseline state
events.jsonl           # Runtime security event log
reports/               # Generated TXT/JSON reports
requirements.txt
.gitignore
README.md


Requirements
Python 3
psutil 7.2.2

Install dependencies:

pip install -r requirements.txt

Usage
Run a single endpoint scan:

python system_health.py

Run continuous scheduled monitoring:
python scheduler.py
The scan interval is controlled through config.json.

Configuration
Example:
{
  "scan_interval_seconds": 900,
  "cpu_warning_percent": 85,
  "memory_warning_percent": 85,
  "disk_warning_percent": 85
}

Additional port-review rules can also be configured in config.json.

Output

The monitor generates:

Human-readable TXT reports
Structured JSON reports
JSONL security event logs
Persistent baseline data for detecting listening-port changes

Generated runtime files are excluded from version control.

Security Monitoring

The tool evaluates:

Suspicious processes
Listening services
Ports requiring review
Newly opened listening ports
Removed listening ports
Changes from a previously stored endpoint baseline
Error Handling


The application handles common operational failures, including:

Missing configuration files
Malformed JSON configuration
Process inspection failures
Graceful scheduler interruption using Ctrl+C
Purpose

This project was built as a practical exercise in Python automation, endpoint monitoring, system administration, and introductory security engineering. It demonstrates structured data collection, stateful comparison, reporting, configuration management, scheduling, and defensive programming.

Future Development

Potential V2 improvements may include:

Historical event storage and analysis
Alert noise reduction and filtering
Windows-specific telemetry
Visualization/dashboard support
Multi-endpoint monitoring

