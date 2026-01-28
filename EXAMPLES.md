# ProcessWatcher - Usage Examples

**Comprehensive examples for ProcessWatcher - Smart Process Monitor & Manager**

Quick navigation:
- [Example 1: Basic System Check](#example-1-basic-system-check)
- [Example 2: Finding Resource Hogs](#example-2-finding-resource-hogs)
- [Example 3: Search for Specific Processes](#example-3-search-for-specific-processes)
- [Example 4: Get Process Details](#example-4-get-process-details)
- [Example 5: Kill Stuck Applications](#example-5-kill-stuck-applications)
- [Example 6: Real-Time Monitoring](#example-6-real-time-monitoring)
- [Example 7: Review Resource History](#example-7-review-resource-history)
- [Example 8: Network Statistics](#example-8-network-statistics)
- [Example 9: Automation and Scripting](#example-9-automation-and-scripting)
- [Example 10: Full Diagnostic Workflow](#example-10-full-diagnostic-workflow)

---

## Example 1: Basic System Check

**Scenario:** You want a quick overview of your system's resource usage.

**Steps:**

```bash
python processwatcher.py stats
```

**Expected Output:**

```
==================================================
  SYSTEM RESOURCE MONITOR
==================================================

CPU Usage:    15.2%
Memory Usage: 62.4% (10.0GB / 16.0GB)
Disk Usage:   45.3% (226.5GB / 500.0GB)
==================================================
```

**What You Learned:**
- Instant view of CPU, memory, and disk usage
- Memory shows both percentage and actual GB values
- Great for quick health checks

---

## Example 2: Finding Resource Hogs

**Scenario:** Your computer is running slow and you want to find what's consuming resources.

**Steps:**

```bash
# List top 20 processes by CPU usage
python processwatcher.py list

# Sort by memory usage instead
python processwatcher.py list --sort memory

# Show more processes
python processwatcher.py list --limit 50
```

**Expected Output (CPU sort):**

```
[Top 20 processes by CPU]

PID      NAME                           CPU%     MEM%     STATUS    
----------------------------------------------------------------------
5432     chrome.exe                     25.3     8.54     running   
8765     python.exe                     12.1     3.21     running   
1234     code.exe                       8.5      5.67     running   
9012     WindowsTerminal.exe            3.2      1.23     running   
...
```

**What You Learned:**
- Processes are sorted by resource usage (CPU default)
- You can quickly identify what's consuming the most resources
- Use --sort memory to find memory hogs
- Increase --limit to see more processes

---

## Example 3: Search for Specific Processes

**Scenario:** You want to find all processes related to a specific application.

**Steps:**

```bash
# Find all Chrome processes
python processwatcher.py find chrome

# Find all Python processes
python processwatcher.py find python

# Find database processes
python processwatcher.py find sql
```

**Expected Output:**

```
[Found 5 process(es) matching 'chrome']

PID      NAME                           CPU%     MEM%     STATUS    
----------------------------------------------------------------------
5432     chrome.exe                     25.3     8.54     running   
5433     chrome.exe                     2.1      3.21     running   
5434     chrome.exe                     1.5      2.67     running   
5435     chrome.exe                     0.8      1.23     running   
5436     chrome.exe                     0.2      0.89     running   
```

**What You Learned:**
- Search is case-insensitive
- Finds all processes containing the search term
- Useful for finding all instances of an application
- Shows resource usage for each match

---

## Example 4: Get Process Details

**Scenario:** You found a suspicious process and want more information.

**Steps:**

```bash
# First, find the process
python processwatcher.py find suspicious_app

# Then get detailed info using its PID
python processwatcher.py info 5432
```

**Expected Output:**

```
============================================================
  Process Details - PID 5432
============================================================

Name:         chrome.exe
PID:          5432
Status:       running
CPU:          25.3%
Memory:       8.54%
Memory (MB):  1389.7 MB
User:         DESKTOP-PC\Logan
Started:      2026-01-28 08:15:32
Exe:          C:\Program Files\Google\Chrome\Application\chrome.exe
CWD:          C:\Program Files\Google\Chrome\Application
Command:      "C:\Program Files\Google\Chrome\Application\chrome.exe" --type=browser

============================================================
```

**What You Learned:**
- Complete process information including executable path
- When the process started
- Full command line that launched it
- User running the process
- Exact memory consumption in MB

---

## Example 5: Kill Stuck Applications

**Scenario:** An application has frozen and you need to terminate it.

**Steps:**

```bash
# Find the stuck process
python processwatcher.py find frozen_app

# Note the PID, then terminate gracefully
python processwatcher.py kill 8765

# If it doesn't respond, force kill
python processwatcher.py kill 8765 --force
```

**Expected Output (Graceful):**

```
[OK] Terminated process 8765 (frozen_app.exe)
     (Use --force to force kill if needed)
```

**Expected Output (Force):**

```
[OK] Force killed process 8765 (frozen_app.exe)
```

**What You Learned:**
- Default kill sends SIGTERM (graceful termination)
- Use --force for SIGKILL (immediate termination)
- Process name is shown for confirmation
- May need admin/sudo for some processes

---

## Example 6: Real-Time Monitoring

**Scenario:** You're running a heavy task and want to watch resource usage live.

**Steps:**

```bash
# Start real-time monitoring (default 2 second interval)
python processwatcher.py monitor

# Custom interval (every 5 seconds)
python processwatcher.py monitor --interval 5
```

**Expected Output:**

```
[Real-time monitoring - Press Ctrl+C to stop]

Time                 CPU%     MEM%     DISK%   
--------------------------------------------------
2026-01-28 10:15:32  15.2     62.4     45.3    
2026-01-28 10:15:34  18.7     62.5     45.3    
2026-01-28 10:15:36  45.3     63.1     45.3    
2026-01-28 10:15:38  78.9     65.2     45.3    
2026-01-28 10:15:40  82.1     66.8     45.3    
^C

[Monitoring stopped]
```

**What You Learned:**
- Live tracking of CPU, memory, and disk
- Data is automatically logged to file
- Press Ctrl+C to stop monitoring
- Useful for identifying resource spikes

---

## Example 7: Review Resource History

**Scenario:** You want to analyze resource usage from your monitoring session.

**Steps:**

```bash
# Show last 20 measurements
python processwatcher.py history

# Show last 50 measurements
python processwatcher.py history --lines 50

# Show last 100 measurements
python processwatcher.py history --lines 100
```

**Expected Output:**

```
[Last 20 resource measurements]

Timestamp                 CPU%     MEM%     DISK%   
-------------------------------------------------------
2026-01-28T10:15:32       15.2     62.4     45.3    
2026-01-28T10:15:34       18.7     62.5     45.3    
2026-01-28T10:15:36       45.3     63.1     45.3    
2026-01-28T10:15:38       78.9     65.2     45.3    
2026-01-28T10:15:40       82.1     66.8     45.3    
...
```

**What You Learned:**
- History is saved to `~/.processwatcher/resource_log.txt`
- CSV format allows easy import to spreadsheet apps
- Useful for identifying patterns over time
- Run monitor first to collect data

---

## Example 8: Network Statistics

**Scenario:** You want to check network activity and data transfer.

**Steps:**

```bash
python processwatcher.py network
```

**Expected Output:**

```
==================================================
  NETWORK STATISTICS
==================================================

Bytes Sent:     2.45 GB
Bytes Received: 15.78 GB
Packets Sent:   2,345,678
Packets Recv:   12,456,789
==================================================
```

**What You Learned:**
- Total network I/O since boot
- Useful for tracking bandwidth usage
- Shows both bytes and packet counts
- Helps identify network-heavy applications

---

## Example 9: Automation and Scripting

**Scenario:** You want to integrate ProcessWatcher into your scripts or automation.

**Steps:**

**Python Script Example:**

```python
from processwatcher import ProcessWatcher

# Create instance
watcher = ProcessWatcher()

# Get system info programmatically
info = watcher.get_system_info()

# Use in your scripts
if info['cpu'] > 90:
    print("ALERT: CPU usage critical!")
    
if info['memory_percent'] > 80:
    print("ALERT: Memory usage high!")

# Log current state
print(f"CPU: {info['cpu']:.1f}%")
print(f"Memory: {info['memory_percent']:.1f}%")
print(f"Disk: {info['disk_percent']:.1f}%")
```

**Bash Script Example:**

```bash
#!/bin/bash
# Monitor and alert script

# Check CPU usage
CPU=$(python processwatcher.py stats 2>&1 | grep "CPU" | awk '{print $3}' | tr -d '%')

if (( $(echo "$CPU > 90" | bc -l) )); then
    echo "ALERT: High CPU usage detected!"
    python processwatcher.py list --limit 5
fi
```

**Cron Job Example:**

```bash
# Add to crontab: crontab -e
# Log stats every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/processwatcher.py monitor --interval 300 &
```

**What You Learned:**
- ProcessWatcher can be used as a Python library
- Easy to integrate into monitoring scripts
- Suitable for cron jobs and automation
- get_system_info() returns a dictionary for easy processing

---

## Example 10: Full Diagnostic Workflow

**Scenario:** Your server is acting slow and you need to diagnose the issue.

**Steps:**

```bash
# Step 1: Quick overview
python processwatcher.py stats

# Step 2: Check top resource users
python processwatcher.py list --limit 10

# Step 3: Get details on the top consumer
python processwatcher.py info 5432

# Step 4: Check network activity
python processwatcher.py network

# Step 5: Start monitoring while investigating
python processwatcher.py monitor --interval 5

# (In another terminal) Find suspicious processes
python processwatcher.py find suspicious

# Step 6: If needed, kill problematic process
python processwatcher.py kill 5432

# Step 7: Review history for patterns
python processwatcher.py history --lines 50
```

**Complete Workflow Output Summary:**

```
=== DIAGNOSTIC REPORT ===

System Stats:
- CPU: 78.5% (HIGH!)
- Memory: 85.2% (HIGH!)
- Disk: 45.3%

Top Consumers:
1. runaway_script.py - CPU 65%, Memory 15%
2. chrome.exe - CPU 8%, Memory 25%
3. code.exe - CPU 5%, Memory 12%

Action Taken:
- Identified runaway_script.py as the culprit
- Process started 6 hours ago
- Terminated with PID 5432

Post-Fix Stats:
- CPU: 12.3%
- Memory: 62.1%
- Issue resolved!
```

**What You Learned:**
- Complete diagnostic workflow from detection to resolution
- Multiple commands work together for full picture
- History helps identify when issues started
- Monitor helps track if fixes are effective

---

## Quick Reference

| Task | Command |
|------|---------|
| System overview | `processwatcher.py stats` |
| Top CPU users | `processwatcher.py list` |
| Top memory users | `processwatcher.py list --sort memory` |
| Find process | `processwatcher.py find NAME` |
| Process details | `processwatcher.py info PID` |
| Kill process | `processwatcher.py kill PID` |
| Force kill | `processwatcher.py kill PID --force` |
| Live monitoring | `processwatcher.py monitor` |
| View history | `processwatcher.py history` |
| Network stats | `processwatcher.py network` |

---

## Tips for Best Results

1. **Run with admin/sudo** for full process visibility
2. **Use monitoring** during suspicious activity to catch spikes
3. **Check history** to identify patterns over time
4. **Combine commands** for complete diagnostics
5. **Automate** regular checks with cron or scheduled tasks

---

**Part of Team Brain / Beacon HQ Toolkit**
