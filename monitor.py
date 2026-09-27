import psutil
import socket
import platform
import time
import logging
import argparse
import os

logging.basicConfig(
    filename="logs/monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    disk = psutil.disk_usage("/")
    return disk.percent


def get_network_usage(interval=1):
    network_before = psutil.net_io_counters()

    time.sleep(interval)

    network_after = psutil.net_io_counters()

    bytes_sent = network_after.bytes_sent - network_before.bytes_sent
    bytes_received = network_after.bytes_recv - network_before.bytes_recv

    return {
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received
    }


def get_hostname():
    return socket.gethostname()


def get_system_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.release(),
        "Architecture": platform.machine(),
        "CPU": platform.processor()
    }


def get_uptime():
    boot_time = psutil.boot_time()
    current_time = time.time()

    uptime_seconds = current_time - boot_time

    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    return hours, minutes


def get_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            processes.append(process.info)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"] or 0,
        reverse=True
    )

    return processes


def check_health(
    cpu_usage,
    memory_usage,
    disk_usage,
    warning_threshold,
    critical_threshold
):
    warnings = []

    resources = {
        "CPU": cpu_usage,
        "Memory": memory_usage,
        "Disk": disk_usage
    }

    for resource, usage in resources.items():

        if usage >= critical_threshold:
            warnings.append(
                f"CRITICAL: {resource} usage is {usage}%"
            )

        elif usage >= warning_threshold:
            warnings.append(
                f"WARNING: {resource} usage is {usage}%"
            )

    return warnings


def log_health_status(warnings):
    if warnings:
        for warning in warnings:
            logging.warning(warning)
    else:
        logging.info("System health: HEALTHY")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Linux System Monitoring Tool"
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Continuously monitor the system"
    )

    parser.add_argument(
        "--warning",
        type=float,
        default=80,
        help="Warning threshold for resource usage (default: 80%%)"
    )

    parser.add_argument(
        "--critical",
        type=float,
        default=90,
        help="Critical threshold for resource usage (default: 90%%)"
    )

    args = parser.parse_args()

    if not 0 <= args.warning <= 100:
        parser.error("Warning threshold must be between 0 and 100.")

    if not 0 <= args.critical <= 100:
        parser.error("Critical threshold must be between 0 and 100.")

    if args.warning >= args.critical:
        parser.error("Warning threshold must be lower than critical threshold.")

    return args
    

def clear_screen():
    os.system("clear")


def run_monitor(warning_threshold, critical_threshold):
    clear_screen()

    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    network_usage = get_network_usage()
    hostname = get_hostname()
    system_info = get_system_info()
    uptime_hours, uptime_minutes = get_uptime()
    processes = get_processes()

    warnings = check_health(
        cpu_usage,
        memory_usage,
        disk_usage,
        warning_threshold,
        critical_threshold
    )

    log_health_status(warnings)

    print("=" * 60)
    print("                 LINUX SYSTEM MONITOR")
    print("=" * 60)

    print("\nSYSTEM")
    print("-" * 60)
    print(f"Hostname:     {hostname}")
    print(f"OS:           {system_info['OS']}")
    print(f"OS Version:   {system_info['OS Version']}")
    print(f"Architecture: {system_info['Architecture']}")
    print(f"Uptime:       {uptime_hours} hours, {uptime_minutes} minutes")

    print("\nRESOURCES")
    print("-" * 60)
    print(f"CPU Usage:    {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Disk Usage:   {disk_usage}%")
    print(f"Network Sent: {network_usage['bytes_sent'] / (1024 ** 2):.2f} MB/s")
    print(f"Network Received: {network_usage['bytes_received'] / (1024 ** 2):.2f} MB/s")

    print("\nSYSTEM HEALTH")
    print("-" * 60)

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("Status: HEALTHY")

    print("\nTOP PROCESSES")
    print("-" * 60)

    for process in processes[:5]:
        print(
            f"PID: {process['pid']} | "
            f"CPU: {process['cpu_percent']}% | "
            f"Memory: {process['memory_percent']:.1f}% | "
            f"Name: {process['name']}"
        )


args = parse_arguments()

try:
    if args.watch:
        while True:
            run_monitor(args.warning, args.critical)
            time.sleep(5)
    else:
        run_monitor(args.warning, args.critical)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")