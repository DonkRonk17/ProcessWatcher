# ProcessWatcher - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use ProcessWatcher for session health monitoring

### Step 1: Installation Check

```bash
# Verify psutil is installed
pip show psutil

# If not installed:
pip install psutil

# Verify ProcessWatcher works
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

### Step 2: First Use - Pre-Session Health Check

```python
# In your Forge session startup
from processwatcher import ProcessWatcher

def forge_pre_session_check():
    """Run this before starting orchestration work."""
    watcher = ProcessWatcher()
    info = watcher.get_system_info()
    
    print("[Forge Pre-Session Check]")
    print(f"CPU: {info['cpu']:.1f}%")
    print(f"Memory: {info['memory_percent']:.1f}%")
    print(f"Disk: {info['disk_percent']:.1f}%")
    
    if info['cpu'] > 80 or info['memory_percent'] > 85:
        print("[!] WARNING: System resources constrained!")
        return False
    
    print("[OK] System ready for orchestration")
    return True

# Run check
forge_pre_session_check()
```

### Step 3: Integration with Forge Workflows

**Use Case 1: Monitor during tool review**

```bash
# Start monitoring while reviewing tools
python processwatcher.py monitor --interval 10
# Press Ctrl+C when done

# Check what caused any spikes
python processwatcher.py history --lines 20
```

**Use Case 2: Find resource-heavy processes**

```bash
# When system feels slow
python processwatcher.py list --sort cpu
python processwatcher.py list --sort memory
```

### Step 4: Common Forge Commands

```bash
# Quick health check
python processwatcher.py stats

# Find what's consuming resources
python processwatcher.py list

# Get details on suspicious process
python processwatcher.py info <PID>

# Kill stuck process if needed
python processwatcher.py kill <PID>
```

### Next Steps for Forge

1. Add pre-session check to your session startup routine
2. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
3. Set up alerts with SynapseLink integration
4. Review [EXAMPLES.md](EXAMPLES.md) - Example 10 (Full Diagnostic)

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use ProcessWatcher for build monitoring

### Step 1: Installation Check

```bash
python -c "from processwatcher import ProcessWatcher; print('[OK] ProcessWatcher ready')"
```

### Step 2: First Use - Build Monitoring

```python
# In your Atlas build sessions
from processwatcher import ProcessWatcher
import time

def atlas_build_monitor(build_name: str):
    """Monitor resources during a build."""
    watcher = ProcessWatcher()
    
    # Check resources before build
    info = watcher.get_system_info()
    print(f"[Atlas] Starting build: {build_name}")
    print(f"Pre-build: CPU {info['cpu']:.1f}%, Memory {info['memory_percent']:.1f}%")
    
    # Warning if already constrained
    if info['memory_percent'] > 80:
        print("[!] WARNING: Memory high - build may be slow")
    
    return info

# Use before builds
atlas_build_monitor("Tool X v1.0")
```

### Step 3: Integration with Build Workflows

**During Tool Creation:**

```bash
# Before starting build
python processwatcher.py stats

# Monitor while building
python processwatcher.py monitor --interval 5 &

# After build - check peak usage
python processwatcher.py history --lines 30
```

**When Tests Are Slow:**

```bash
# Find what's competing for resources
python processwatcher.py list --sort memory --limit 10

# Find specific process details
python processwatcher.py find python
python processwatcher.py info <PID>
```

### Step 4: Common Atlas Commands

```bash
# Pre-build check
python processwatcher.py stats

# Track build in real-time
python processwatcher.py monitor

# Find memory hogs during tests
python processwatcher.py list --sort memory

# Check network for downloads
python processwatcher.py network
```

### Next Steps for Atlas

1. Integrate into Holy Grail Phase 5 (Testing) for resource tracking
2. Add to tool build checklist - check resources before heavy operations
3. Try [EXAMPLES.md](EXAMPLES.md) - Example 9 (Automation and Scripting)
4. Set up build resource baseline tracking

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use ProcessWatcher in Linux environments

### Step 1: Linux Installation

```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/ProcessWatcher.git
cd ProcessWatcher

# Install dependency
pip3 install psutil

# Verify installation
python3 processwatcher.py --help
```

### Step 2: First Use - System Health Check

```bash
# Basic system stats
python3 processwatcher.py stats

# Top processes
python3 processwatcher.py list

# Network activity
python3 processwatcher.py network
```

### Step 3: Integration with Clio Workflows

**System Health Script:**

```bash
#!/bin/bash
# clio_health_check.sh

echo "=== CLIO System Health Report ==="
echo "Date: $(date)"
echo ""

echo "--- Resource Usage ---"
python3 /path/to/processwatcher.py stats

echo ""
echo "--- Top 5 CPU Users ---"
python3 /path/to/processwatcher.py list --limit 5

echo ""
echo "--- Network Stats ---"
python3 /path/to/processwatcher.py network

echo ""
echo "=== End Report ==="
```

**Background Monitoring:**

```bash
# Run monitoring in background
nohup python3 processwatcher.py monitor --interval 60 > /tmp/resource_monitor.log 2>&1 &

# Check logs later
tail -f /tmp/resource_monitor.log
```

**Cron Job Setup:**

```bash
# Add to crontab for hourly checks
crontab -e

# Add this line:
0 * * * * /usr/bin/python3 /path/to/processwatcher.py stats >> /var/log/system_health.log 2>&1
```

### Step 4: Common Clio Commands

```bash
# Full system overview
python3 processwatcher.py stats

# Find specific processes
python3 processwatcher.py find nginx
python3 processwatcher.py find postgres

# Monitor server load
python3 processwatcher.py monitor --interval 30

# Kill stuck process (may need sudo)
sudo python3 processwatcher.py kill <PID> --force
```

### Platform-Specific Notes

- Use `python3` explicitly on most Linux systems
- `sudo` may be needed for full process visibility
- Log files go to `~/.processwatcher/` by default
- Works in WSL without modifications

### Next Steps for Clio

1. Add to ABIOS startup routine
2. Create system monitoring cron job
3. Set up alerts for critical thresholds
4. Try [EXAMPLES.md](EXAMPLES.md) - Example 6 (Real-Time Monitoring)

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of ProcessWatcher

### Step 1: Platform Detection

```python
import platform
from processwatcher import ProcessWatcher

watcher = ProcessWatcher()
print(f"Platform: {platform.system()} {platform.release()}")

info = watcher.get_system_info()
print(f"CPU: {info['cpu']:.1f}%")
print(f"Memory: {info['memory_percent']:.1f}%")
```

### Step 2: First Use - Cross-Platform Diagnostics

```python
# Cross-platform system check
from processwatcher import ProcessWatcher

def nexus_system_check():
    """Works on Windows, Linux, and macOS."""
    watcher = ProcessWatcher()
    info = watcher.get_system_info()
    
    status = "healthy"
    warnings = []
    
    if info['cpu'] > 80:
        warnings.append(f"High CPU: {info['cpu']:.1f}%")
        status = "warning"
    if info['memory_percent'] > 85:
        warnings.append(f"High Memory: {info['memory_percent']:.1f}%")
        status = "warning"
    if info['disk_percent'] > 90:
        warnings.append(f"Low Disk: {100 - info['disk_percent']:.1f}% free")
        status = "critical"
    
    return {
        'status': status,
        'cpu': info['cpu'],
        'memory': info['memory_percent'],
        'disk': info['disk_percent'],
        'warnings': warnings
    }

# Run check
result = nexus_system_check()
print(f"Status: {result['status'].upper()}")
for warn in result['warnings']:
    print(f"  [!] {warn}")
```

### Step 3: Platform-Specific Considerations

**Windows:**
- Run as Administrator for full process visibility
- Use `python` command
- Paths use backslashes but ProcessWatcher handles this

**Linux:**
- Use `python3` command
- `sudo` for full process visibility
- Paths use forward slashes

**macOS:**
- Use `python3` command
- `sudo` for full process visibility
- Activity Monitor shows similar info graphically

### Step 4: Common Nexus Commands

```bash
# Same commands work everywhere:
python processwatcher.py stats
python processwatcher.py list --sort memory
python processwatcher.py find python
python processwatcher.py monitor
```

### Next Steps for Nexus

1. Test on all 3 platforms you have access to
2. Create platform-agnostic monitoring scripts
3. Report any platform-specific issues
4. Try [EXAMPLES.md](EXAMPLES.md) - Example 4 (Process Details)

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use ProcessWatcher for quick system checks (zero API cost)

### Step 1: Verify Free Access

```bash
# ProcessWatcher requires NO API keys!
python processwatcher.py --help

# Zero cost system check
python processwatcher.py stats
```

### Step 2: First Use - Quick System Check

```bash
# Fast check before heavy task
python processwatcher.py stats

# See what's running
python processwatcher.py list --limit 5
```

### Step 3: Integration with Bolt Workflows

**Pre-Task Check:**

```bash
# Before running any heavy operation:
python processwatcher.py stats
# If CPU > 90% or Memory > 85%, wait or alert

# Check what's using resources
python processwatcher.py list --sort cpu --limit 3
```

**When Task Is Slow:**

```bash
# Find competing processes
python processwatcher.py find python
python processwatcher.py list --sort memory

# If needed, kill stuck process
python processwatcher.py kill <PID>
```

### Step 4: Common Bolt Commands

```bash
# Quick health check (most common)
python processwatcher.py stats

# Find resource hogs
python processwatcher.py list

# Kill stuck process
python processwatcher.py kill <PID> --force

# Network check
python processwatcher.py network
```

### Cost Considerations

- **Zero API cost** - ProcessWatcher runs entirely locally
- **Zero dependencies** on external services
- **Call as often as needed** without budget impact
- Great for monitoring during heavy local tasks

### Next Steps for Bolt

1. Add `processwatcher.py stats` to task startup
2. Use for quick diagnostics when things are slow
3. Report any issues via Synapse
4. Try [EXAMPLES.md](EXAMPLES.md) - Example 5 (Kill Stuck Applications)

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/ProcessWatcher/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Forge for complex issues

---

**Last Updated:** January 28, 2026  
**Maintained By:** Forge (Team Brain)
