This script is straightforward in functionality

==============================================================================================

```
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
```
