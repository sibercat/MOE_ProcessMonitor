import subprocess
import time
import logging
import json
from logging.handlers import RotatingFileHandler
from collections import defaultdict

# Configuration settings for the process monitor
CONFIG = {
    "log_file": "MOE_ProcessMonitor.log",        # Log file name
    "max_log_size": 10 * 1024 * 1024,            # Max log file size (10 MB)
    "log_backup_count": 5,                       # Number of backup logs to keep
    "check_interval": 120,                       # Time (in seconds) between checks
    "restart_delay": 20,                         # Delay (in seconds) before restarting a process
    "ports": {                                   # Port and corresponding batch file mappings
        "5011": "StartSceneServer_51199.bat",    # Check what ports are down and run specific .bat file that's associated with that port.
        "5012": "StartSceneServer_55862.bat",
        "5013": "StartSceneServer_56731.bat"
    },
    "max_restarts": 3,                           # Maximum number of restarts allowed within the time window
    "restart_window": 60,                       # Time window (in seconds) for tracking restarts
}

# Set up basic configuration for logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log file formatter configuration
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# File handler for logging (with rotation based on file size)
file_handler = RotatingFileHandler(CONFIG['log_file'], maxBytes=CONFIG['max_log_size'], backupCount=CONFIG['log_backup_count'])
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler for logging (to output logs to the console as well)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def is_port_open(port):
    """
    Check if a specified port is open on the local machine.
    
    Args:
    port (str): Port number to check.
    
    Returns:
    bool: True if the port is open, False otherwise.
    """
    try:
        output = subprocess.check_output(['netstat', '-an'], text=True)
        return f":{port} " in output
    except subprocess.CalledProcessError:
        logger.error(f"Failed to check port {port}")
        return False

def start_process(bat_file):
    """
    Starts a process by executing a batch file.
    
    Args:
    bat_file (str): Path to the batch file to execute.
    """
    try:
        subprocess.check_call([bat_file], shell=True)
        logger.info(f"Process {bat_file} started successfully.")
    except subprocess.CalledProcessError:
        logger.error(f"Failed to start process {bat_file}")

def monitor_processes():
    """
    Continuously monitor and maintain server processes running on specified ports.
    """
    restart_counts = defaultdict(int)
    restart_timestamps = defaultdict(list)

    while True:
        down_ports = []
        for port, bat_file in CONFIG['ports'].items():
            if not is_port_open(port):
                down_ports.append((port, bat_file))
            else:
                logger.info(f"Port {port} is running.")

        if down_ports:
            for port, bat_file in down_ports:
                current_time = time.time()
                restart_counts[port] += 1
                restart_timestamps[port].append(current_time)

                # Remove restart timestamps older than the restart window
                restart_timestamps[port] = [ts for ts in restart_timestamps[port] if current_time - ts <= CONFIG['restart_window']]

                if restart_counts[port] <= CONFIG['max_restarts']:
                    logger.warning(f"Port {port} is down. Attempting to restart... (Restart Count: {restart_counts[port]})")
                    start_process(bat_file)
                    time.sleep(CONFIG['restart_delay'])
                else:
                    logger.critical(f"Port {port} exceeded the maximum number of restarts within the time window.")
                    # TODO: Send an alert or take further action
        else:
            logger.info("All ports are running.")

        logger.info("Completed a monitoring cycle. Waiting for the next check interval.")
        time.sleep(CONFIG['check_interval'])

def main():
    """
    Main function to start the process monitor.
    """
    try:
        logger.info("Starting MOEServer process monitor...")
        monitor_processes()
    except KeyboardInterrupt:
        logger.info("Monitoring stopped manually via KeyboardInterrupt.")

if __name__ == "__main__":
    main()
