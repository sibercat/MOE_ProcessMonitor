This script is straightforward in functionality. Check if port is down, if port is down start .bat that's associated with that port.

===========================================================================

Open your .bat file and make sure it has a direct path to MOEServer.exe

===========================================================================

```
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
    "restart_window": 300,                       # Time window (in seconds) for tracking restarts
}
```
