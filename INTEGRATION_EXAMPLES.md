# ProcessWatcher - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

ProcessWatcher is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: ProcessWatcher + AgentHealth](#pattern-1-processwatcher--agenthealth)
2. [Pattern 2: ProcessWatcher + SynapseLink](#pattern-2-processwatcher--synapselink)
3. [Pattern 3: ProcessWatcher + TaskQueuePro](#pattern-3-processwatcher--taskqueuepro)
4. [Pattern 4: ProcessWatcher + MemoryBridge](#pattern-4-processwatcher--memorybridge)
5. [Pattern 5: ProcessWatcher + SessionReplay](#pattern-5-processwatcher--sessionreplay)
6. [Pattern 6: ProcessWatcher + ConfigManager](#pattern-6-processwatcher--configmanager)
7. [Pattern 7: ProcessWatcher + TokenTracker](#pattern-7-processwatcher--tokentracker)
8. [Pattern 8: ProcessWatcher + ErrorRecovery](#pattern-8-processwatcher--errorrecovery)
9. [Pattern 9: Multi-Tool Monitoring Stack](#pattern-9-multi-tool-monitoring-stack)
10. [Pattern 10: Full Team Brain Health Dashboard](#pattern-10-full-team-brain-health-dashboard)

---

## Pattern 1: ProcessWatcher + AgentHealth

**Use Case:** Correlate system resources with agent session health

**Why:** Understand if system constraints affect agent performance

**Code:**

```python
from agenthealth import AgentHealth
from processwatcher import ProcessWatcher
from datetime import datetime

# Initialize both tools
health = AgentHealth()
watcher = ProcessWatcher()

# Start session with system context
session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
agent_name = "FORGE"

# Log system state at session start
info = watcher.get_system_info()
health.start_session(agent_name, session_id=session_id)
health.log_metric(agent_name, "start_cpu", info['cpu'])
health.log_metric(agent_name, "start_memory", info['memory_percent'])

print(f"[{agent_name}] Session started: {session_id}")
print(f"System: CPU {info['cpu']:.1f}%, Memory {info['memory_percent']:.1f}%")

# ... do work ...

# Log system state at session end
info = watcher.get_system_info()
health.log_metric(agent_name, "end_cpu", info['cpu'])
health.log_metric(agent_name, "end_memory", info['memory_percent'])
health.end_session(agent_name, session_id=session_id, status="success")

print(f"[{agent_name}] Session complete")
print(f"Final: CPU {info['cpu']:.1f}%, Memory {info['memory_percent']:.1f}%")
```

**Result:** Session health data correlated with system resource usage for analysis

---

## Pattern 2: ProcessWatcher + SynapseLink

**Use Case:** Alert Team Brain when system resources are critical

**Why:** Keep team informed of system issues automatically

**Code:**

```python
from synapselink import quick_send
from processwatcher import ProcessWatcher

watcher = ProcessWatcher()
info = watcher.get_system_info()

# Define thresholds
CPU_WARNING = 70
CPU_CRITICAL = 90
MEMORY_WARNING = 80
MEMORY_CRITICAL = 90

# Check and alert
alerts = []

if info['cpu'] >= CPU_CRITICAL:
    alerts.append(f"[CRITICAL] CPU at {info['cpu']:.1f}%")
elif info['cpu'] >= CPU_WARNING:
    alerts.append(f"[WARNING] CPU at {info['cpu']:.1f}%")

if info['memory_percent'] >= MEMORY_CRITICAL:
    alerts.append(f"[CRITICAL] Memory at {info['memory_percent']:.1f}%")
elif info['memory_percent'] >= MEMORY_WARNING:
    alerts.append(f"[WARNING] Memory at {info['memory_percent']:.1f}%")

# Send alert if needed
if alerts:
    priority = "HIGH" if any("CRITICAL" in a for a in alerts) else "NORMAL"
    
    quick_send(
        "LOGAN,FORGE",
        f"System Resource Alert",
        f"System alerts detected:\n" + "\n".join(alerts) + 
        f"\n\nFull status:\n"
        f"CPU: {info['cpu']:.1f}%\n"
        f"Memory: {info['memory_percent']:.1f}%\n"
        f"Disk: {info['disk_percent']:.1f}%",
        priority=priority
    )
    print(f"[!] Alert sent: {len(alerts)} issue(s)")
else:
    print(f"[OK] System healthy - no alerts")
```

**Result:** Team automatically notified when system resources need attention

---

## Pattern 3: ProcessWatcher + TaskQueuePro

**Use Case:** Track system resources during task execution

**Why:** Correlate task performance with resource availability

**Code:**

```python
from taskqueuepro import TaskQueuePro
from processwatcher import ProcessWatcher

queue = TaskQueuePro()
watcher = ProcessWatcher()

# Create task with pre-check
info = watcher.get_system_info()

task_id = queue.create_task(
    title="Heavy computation task",
    agent="ATLAS",
    priority=2,
    metadata={
        "pre_cpu": info['cpu'],
        "pre_memory": info['memory_percent'],
        "requires_resources": True
    }
)

# Check if resources allow task execution
if info['cpu'] > 80 or info['memory_percent'] > 85:
    queue.add_note(task_id, f"[!] High resource usage at start - may be slow")
    queue.add_note(task_id, f"CPU: {info['cpu']:.1f}%, Memory: {info['memory_percent']:.1f}%")

# Start task
queue.start_task(task_id)
print(f"[Task {task_id}] Started")

# ... execute task ...

# Complete with resource info
info = watcher.get_system_info()
queue.complete_task(task_id, result={
    "status": "success",
    "post_cpu": info['cpu'],
    "post_memory": info['memory_percent'],
    "resource_delta": {
        "cpu_change": info['cpu'] - queue.get_task(task_id)['metadata']['pre_cpu'],
        "memory_change": info['memory_percent'] - queue.get_task(task_id)['metadata']['pre_memory']
    }
})

print(f"[Task {task_id}] Complete")
```

**Result:** Tasks tracked with resource usage data for performance analysis

---

## Pattern 4: ProcessWatcher + MemoryBridge

**Use Case:** Persist system metrics history to memory core

**Why:** Build long-term resource usage trends

**Code:**

```python
from memorybridge import MemoryBridge
from processwatcher import ProcessWatcher
from datetime import datetime

memory = MemoryBridge()
watcher = ProcessWatcher()

# Load existing metrics
metrics_key = "system_metrics_history"
history = memory.get(metrics_key, default=[])

# Add current metrics
info = watcher.get_system_info()
history.append({
    "timestamp": datetime.now().isoformat(),
    "cpu": info['cpu'],
    "memory_percent": info['memory_percent'],
    "memory_used_gb": info['memory_used_gb'],
    "disk_percent": info['disk_percent']
})

# Keep last 1000 entries (approx 16 hours at 1-minute intervals)
MAX_HISTORY = 1000
if len(history) > MAX_HISTORY:
    history = history[-MAX_HISTORY:]

# Calculate trends
if len(history) >= 10:
    recent_cpu = [h['cpu'] for h in history[-10:]]
    avg_cpu = sum(recent_cpu) / len(recent_cpu)
    
    recent_mem = [h['memory_percent'] for h in history[-10:]]
    avg_mem = sum(recent_mem) / len(recent_mem)
    
    print(f"Recent averages: CPU {avg_cpu:.1f}%, Memory {avg_mem:.1f}%")

# Save
memory.set(metrics_key, history)
memory.sync()

print(f"[OK] Metrics saved ({len(history)} entries in history)")
```

**Result:** Historical system metrics persisted for trend analysis

---

## Pattern 5: ProcessWatcher + SessionReplay

**Use Case:** Record system state during sessions for debugging

**Why:** Replay sessions with full system context

**Code:**

```python
from sessionreplay import SessionReplay
from processwatcher import ProcessWatcher

replay = SessionReplay()
watcher = ProcessWatcher()

# Start recording with system context
session_id = replay.start_session("FORGE", task="Complex tool build")

info = watcher.get_system_info()
replay.log_context(session_id, 
    f"System baseline: CPU {info['cpu']:.1f}%, "
    f"Memory {info['memory_percent']:.1f}%, "
    f"Disk {info['disk_percent']:.1f}%"
)

# During session - log resource-heavy operations
replay.log_event(session_id, "Starting heavy operation: test suite")

info = watcher.get_system_info()
replay.log_context(session_id, f"Pre-operation: CPU {info['cpu']:.1f}%")

# ... operation runs ...

info = watcher.get_system_info()
replay.log_context(session_id, f"Post-operation: CPU {info['cpu']:.1f}%")
replay.log_event(session_id, "Heavy operation complete")

# End session
info = watcher.get_system_info()
replay.log_context(session_id, 
    f"Session end: CPU {info['cpu']:.1f}%, Memory {info['memory_percent']:.1f}%"
)
replay.end_session(session_id, status="COMPLETED")

print(f"[OK] Session {session_id} recorded with system context")
```

**Result:** Full session replay with system state at each step

---

## Pattern 6: ProcessWatcher + ConfigManager

**Use Case:** Centralized alert thresholds configuration

**Why:** Consistent thresholds across all agents and tools

**Code:**

```python
from configmanager import ConfigManager
from processwatcher import ProcessWatcher

config = ConfigManager()
watcher = ProcessWatcher()

# Load thresholds from centralized config
thresholds = config.get("processwatcher", {
    "cpu_warning": 70,
    "cpu_critical": 90,
    "memory_warning": 80,
    "memory_critical": 90,
    "disk_warning": 85,
    "disk_critical": 95,
    "monitor_interval": 5
})

# Get current system state
info = watcher.get_system_info()

# Check against configured thresholds
def check_threshold(value, warning, critical, name):
    if value >= critical:
        return f"[CRITICAL] {name}: {value:.1f}%"
    elif value >= warning:
        return f"[WARNING] {name}: {value:.1f}%"
    return f"[OK] {name}: {value:.1f}%"

print("=== System Check (Configured Thresholds) ===")
print(check_threshold(info['cpu'], 
    thresholds['cpu_warning'], 
    thresholds['cpu_critical'], 
    "CPU"))
print(check_threshold(info['memory_percent'], 
    thresholds['memory_warning'], 
    thresholds['memory_critical'], 
    "Memory"))
print(check_threshold(info['disk_percent'], 
    thresholds['disk_warning'], 
    thresholds['disk_critical'], 
    "Disk"))

# Update config if needed
# config.set("processwatcher.cpu_warning", 75)
# config.save()
```

**Result:** Configurable thresholds shared across all Team Brain tools

---

## Pattern 7: ProcessWatcher + TokenTracker

**Use Case:** Monitor resources alongside API token costs

**Why:** Correlate system health with API usage patterns

**Code:**

```python
from tokentracker import TokenTracker
from processwatcher import ProcessWatcher
from datetime import datetime

tracker = TokenTracker()
watcher = ProcessWatcher()

def session_health_report():
    """Generate combined health and cost report."""
    # Get system state
    info = watcher.get_system_info()
    
    # Get token usage
    session = tracker.get_current_session()
    daily = tracker.get_daily_summary()
    
    print("=" * 50)
    print("  SESSION HEALTH & COST REPORT")
    print("=" * 50)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n--- System Resources ---")
    print(f"CPU: {info['cpu']:.1f}%")
    print(f"Memory: {info['memory_percent']:.1f}% ({info['memory_used_gb']:.1f}GB)")
    print(f"Disk: {info['disk_percent']:.1f}%")
    
    print("\n--- Token Usage ---")
    print(f"Session Tokens: {session.get('tokens', 0):,}")
    print(f"Session Cost: ${session.get('cost', 0):.4f}")
    print(f"Daily Total: ${daily.get('total_cost', 0):.2f}")
    
    print("\n--- Health Status ---")
    system_ok = info['cpu'] < 80 and info['memory_percent'] < 85
    budget_ok = daily.get('total_cost', 0) < 2.00  # $2/day target
    
    print(f"System: {'[OK]' if system_ok else '[WARNING]'}")
    print(f"Budget: {'[OK]' if budget_ok else '[WARNING]'}")
    print("=" * 50)
    
    return {
        'system_healthy': system_ok,
        'budget_ok': budget_ok,
        'system_info': info,
        'token_info': session
    }

# Run report
report = session_health_report()
```

**Result:** Combined view of system health and API costs

---

## Pattern 8: ProcessWatcher + ErrorRecovery

**Use Case:** Include system state in error recovery context

**Why:** Better diagnose if errors are resource-related

**Code:**

```python
from errorrecovery import ErrorRecovery
from processwatcher import ProcessWatcher
import traceback

recovery = ErrorRecovery()
watcher = ProcessWatcher()

def execute_with_resource_context(task_name, task_func, *args, **kwargs):
    """Execute task with system context for error recovery."""
    # Get pre-task system state
    pre_info = watcher.get_system_info()
    
    try:
        # Execute task
        result = task_func(*args, **kwargs)
        return result
        
    except Exception as e:
        # Get post-error system state
        post_info = watcher.get_system_info()
        
        # Log error with system context
        recovery.log_error(
            error_type=type(e).__name__,
            error_message=str(e),
            context={
                'task': task_name,
                'traceback': traceback.format_exc(),
                'pre_task_resources': {
                    'cpu': pre_info['cpu'],
                    'memory': pre_info['memory_percent'],
                    'disk': pre_info['disk_percent']
                },
                'post_error_resources': {
                    'cpu': post_info['cpu'],
                    'memory': post_info['memory_percent'],
                    'disk': post_info['disk_percent']
                },
                'resource_delta': {
                    'cpu_change': post_info['cpu'] - pre_info['cpu'],
                    'memory_change': post_info['memory_percent'] - pre_info['memory_percent']
                }
            }
        )
        
        # Check if error might be resource-related
        if post_info['memory_percent'] > 95:
            print(f"[!] Error may be related to memory exhaustion!")
        if post_info['cpu'] > 95:
            print(f"[!] Error may be related to CPU saturation!")
        
        raise

# Example usage
def heavy_task():
    # Simulated heavy work
    return "completed"

try:
    result = execute_with_resource_context("heavy_computation", heavy_task)
except Exception as e:
    print(f"Task failed: {e}")
```

**Result:** Errors logged with system context for better diagnosis

---

## Pattern 9: Multi-Tool Monitoring Stack

**Use Case:** Complete monitoring workflow with multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
from processwatcher import ProcessWatcher
from agenthealth import AgentHealth
from synapselink import quick_send
from memorybridge import MemoryBridge
from datetime import datetime

# Initialize monitoring stack
watcher = ProcessWatcher()
health = AgentHealth()
memory = MemoryBridge()

def comprehensive_health_check(agent_name: str = "FORGE"):
    """Complete health check using multiple tools."""
    timestamp = datetime.now().isoformat()
    
    # 1. Get system resources
    info = watcher.get_system_info()
    
    # 2. Log to AgentHealth
    health.heartbeat(agent_name, status="checking")
    health.log_metric(agent_name, "system_cpu", info['cpu'])
    health.log_metric(agent_name, "system_memory", info['memory_percent'])
    
    # 3. Store in MemoryBridge
    history = memory.get("health_checks", default=[])
    history.append({
        'timestamp': timestamp,
        'agent': agent_name,
        'cpu': info['cpu'],
        'memory': info['memory_percent'],
        'disk': info['disk_percent']
    })
    memory.set("health_checks", history[-100:])  # Keep last 100
    memory.sync()
    
    # 4. Check for alerts
    alerts = []
    if info['cpu'] > 90:
        alerts.append(f"CPU Critical: {info['cpu']:.1f}%")
    if info['memory_percent'] > 90:
        alerts.append(f"Memory Critical: {info['memory_percent']:.1f}%")
    if info['disk_percent'] > 95:
        alerts.append(f"Disk Critical: {info['disk_percent']:.1f}%")
    
    # 5. Send alerts via SynapseLink if needed
    if alerts:
        quick_send(
            "LOGAN",
            f"[{agent_name}] Health Alert",
            "\n".join(alerts),
            priority="HIGH"
        )
        health.heartbeat(agent_name, status="warning")
    else:
        health.heartbeat(agent_name, status="healthy")
    
    return {
        'timestamp': timestamp,
        'agent': agent_name,
        'system': info,
        'alerts': alerts,
        'status': 'warning' if alerts else 'healthy'
    }

# Run comprehensive check
result = comprehensive_health_check("FORGE")
print(f"Health check complete: {result['status'].upper()}")
```

**Result:** Fully instrumented health monitoring with alerting

---

## Pattern 10: Full Team Brain Health Dashboard

**Use Case:** Dashboard data for BCH integration

**Why:** Production-grade monitoring for Team Brain operations

**Code:**

```python
from processwatcher import ProcessWatcher
from datetime import datetime
import json

watcher = ProcessWatcher()

def generate_dashboard_data():
    """Generate dashboard-ready health data."""
    info = watcher.get_system_info()
    
    # Calculate status levels
    def get_level(value, warning, critical):
        if value >= critical:
            return "critical"
        elif value >= warning:
            return "warning"
        return "healthy"
    
    dashboard = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu": {
                "value": round(info['cpu'], 1),
                "unit": "%",
                "level": get_level(info['cpu'], 70, 90)
            },
            "memory": {
                "value": round(info['memory_percent'], 1),
                "used_gb": round(info['memory_used_gb'], 1),
                "total_gb": round(info['memory_total_gb'], 1),
                "unit": "%",
                "level": get_level(info['memory_percent'], 80, 90)
            },
            "disk": {
                "value": round(info['disk_percent'], 1),
                "used_gb": round(info['disk_used_gb'], 1),
                "total_gb": round(info['disk_total_gb'], 1),
                "unit": "%",
                "level": get_level(info['disk_percent'], 85, 95)
            }
        },
        "overall_status": "critical" if any([
            info['cpu'] >= 90,
            info['memory_percent'] >= 90,
            info['disk_percent'] >= 95
        ]) else "warning" if any([
            info['cpu'] >= 70,
            info['memory_percent'] >= 80,
            info['disk_percent'] >= 85
        ]) else "healthy",
        "recommendations": []
    }
    
    # Add recommendations
    if info['cpu'] > 70:
        dashboard["recommendations"].append({
            "type": "cpu",
            "message": "Consider closing unused applications",
            "priority": "high" if info['cpu'] > 90 else "medium"
        })
    if info['memory_percent'] > 80:
        dashboard["recommendations"].append({
            "type": "memory",
            "message": "Memory pressure detected - may need restart",
            "priority": "high" if info['memory_percent'] > 90 else "medium"
        })
    if info['disk_percent'] > 85:
        dashboard["recommendations"].append({
            "type": "disk",
            "message": "Consider freeing up disk space",
            "priority": "high" if info['disk_percent'] > 95 else "medium"
        })
    
    return dashboard

# Generate and display
dashboard = generate_dashboard_data()
print(json.dumps(dashboard, indent=2))

# For BCH integration:
# return dashboard as JSON response or store in shared location
```

**Result:** Dashboard-ready JSON data for BCH or other visualization

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ AgentHealth - Session health correlation
2. ✅ SynapseLink - Alert notifications
3. ✅ MemoryBridge - Metrics history

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task monitoring
5. ☐ SessionReplay - Debug context
6. ☐ ConfigManager - Centralized thresholds

**Week 3 (Advanced):**
7. ☐ ErrorRecovery - Resource-aware errors
8. ☐ TokenTracker - Cost correlation
9. ☐ Full dashboard integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from processwatcher import ProcessWatcher
```

**Version Conflicts:**
```bash
# Check versions
python processwatcher.py --help

# Update if needed
cd AutoProjects/ProcessWatcher
git pull origin main
```

**Configuration Issues:**
```python
# Reset ProcessWatcher to defaults
import shutil
from pathlib import Path

config_dir = Path.home() / ".processwatcher"
if config_dir.exists():
    shutil.rmtree(config_dir)
print("Configuration reset - will be recreated on next run")
```

---

**Last Updated:** January 28, 2026  
**Maintained By:** Forge (Team Brain)
