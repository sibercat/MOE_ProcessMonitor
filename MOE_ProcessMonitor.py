import subprocess
import time
import logging
import json
from logging.handlers import RotatingFileHandler

# Configuration settings for the process monitor
CONFIG = {
    "log_file": "MOE_ProcessMonitor.log",        # Log file name
    "max_log_size": 10 * 1024 * 1024,            # Max log file size (10 MB) multiplies 10 by 1024 and then multiplies the result by 1024 again  = to make (5MB) 5 * 1024 * 1024, 
    "log_backup_count": 5,                       # Number of backup logs to keep
    "check_interval": 120,                       # Time (in seconds) between checks
    "restart_delay": 20,                         # Delay (in seconds) before restarting a process
    "ports": {                                   # Port and corresponding batch file mappings
        "5011": "StartSceneServer_51199.bat",    # Check what ports are down and run specific .bat file that's associated with
        "5012": "StartSceneServer_55862.bat",
        "5013": "StartSceneServer_56731.bat"
    }
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
    while True:
        down_ports = []
        for port, bat_file in CONFIG['ports'].items():
            if not is_port_open(port):
                down_ports.append((port, bat_file))
            else:
                logger.info(f"Port {port} is running.")

        if down_ports:
            for port, bat_file in down_ports:
                logger.warning(f"Port {port} is down. Attempting to restart...")
                start_process(bat_file)
                time.sleep(CONFIG['restart_delay'])
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