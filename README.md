# Linux System Monitor

A Linux system monitor built with Python and psutil to track CPU, memory, disk, network activity, running processes, and overall system health.

## Features

- CPU usage monitoring
- Memory usage monitoring
- Disk usage monitoring
- Network throughput monitoring
- System information and uptime
- Top processes by CPU usage
- System health checks with warning and critical thresholds
- Configurable warning and critical thresholds
- Continuous monitoring mode
- System health logging
- Graceful shutdown with `Ctrl+C`
- Automated tests with pytest
- Command-line interface

## Technologies

- Python 3
- Linux / Ubuntu
- WSL2
- psutil
- argparse
- pytest
- uv (dependency and environment management)
- Make (development task automation)
- Git & GitHub
- GitHub Actions (continuous integration)

## Project Structure

```text
linux-system-monitor/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_monitor.py
├── .gitignore
├── Makefile
├── monitor.py
├── pyproject.toml
├── uv.lock
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ossyanth/linux-system-monitor.git
cd linux-system-monitor
```

### 2. Set up the project

```bash
make setup
```

This uses uv to create the virtual environment and install the project dependencies.

The project is now ready to run.

## Usage

### Run a single monitoring check

```bash
make run
```

### Continuously monitor the system

```bash
uv run python monitor.py --watch
```

The dashboard refreshes every 5 seconds.

### Custom warning and critical thresholds

```bash
uv run python monitor.py --warning 70 --critical 90
```

For example:

- Resources at or above 70% generate a warning.
- Resources at or above 90% generate a critical alert.

### Combine continuous monitoring with custom thresholds

```bash
uv run python monitor.py --watch --warning 70 --critical 90
```

### View available command-line options

```bash
uv run python monitor.py --help
```

### Stop continuous monitoring

Press:

```text
Ctrl+C
```

The monitor will exit cleanly with:

```text
Monitoring stopped.
```

## Example Output

```text
============================================================
                 LINUX SYSTEM MONITOR
============================================================

SYSTEM
------------------------------------------------------------
Hostname:     ossy
OS:           Linux
OS Version:   6.6.114.1-microsoft-standard-WSL2
Architecture: x86_64
Uptime:       8 hours, 30 minutes

RESOURCES
------------------------------------------------------------
CPU Usage:    1.3%
Memory Usage: 26.2%
Disk Usage:   0.2%
Network Sent: 0.00 MB/s
Network Received: 0.00 MB/s

SYSTEM HEALTH
------------------------------------------------------------
Status: HEALTHY

TOP PROCESSES
------------------------------------------------------------
PID: 1 | CPU: 0.0% | Memory: 0.4% | Name: systemd
PID: 2 | CPU: 0.0% | Memory: 0.1% | Name: init-systemd(Ub
PID: 6 | CPU: 0.0% | Memory: 0.1% | Name: init
PID: 46 | CPU: 0.0% | Memory: 0.4% | Name: systemd-journald
PID: 81 | CPU: 0.0% | Memory: 0.4% | Name: systemd-resolved
```

## Testing

Run the test suite with:

```bash
make test
```

Expected result:

```text
6 passed
```

## What I Learned

- Working with Linux system information using Python and psutil
- Monitoring CPU, memory, disk, and network usage
- Working with Linux processes and handling process-related exceptions
- Building command-line tools with argparse
- Implementing configurable health checks and thresholds
- Writing logs for system health events
- Writing automated tests with pytest
- Using Git and GitHub to manage and document a project
- Managing Python dependencies and virtual environments with uv
- Automating common development tasks with Make
- Implementing continuous integration with GitHub Actions

## Future Improvements

- Add configurable monitoring intervals
- Improve network throughput display
- Add more detailed process monitoring
- Add CPU temperature monitoring where supported
- Improve terminal output formatting
- Containerize the application with Docker
- Add support for exporting monitoring data