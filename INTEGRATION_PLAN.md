# ProcessWatcher - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how ProcessWatcher integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - potential integration
4. Logan's workflows

---

## 📦 BCH INTEGRATION

### Overview

ProcessWatcher provides system monitoring capabilities that complement BCH operations:
- Monitor resource usage during BCH sessions
- Alert when system resources are constrained
- Help diagnose performance issues in BCH backend/frontend
- Support debugging of WebSocket connections and AI responses

### Potential BCH Commands (Future Integration)

```
@processwatcher stats           # System resource overview
@processwatcher alert cpu 90    # Alert if CPU > 90%
@processwatcher top 5           # Top 5 resource consumers
```

### Implementation Steps

1. ☐ Create BCH command handler for ProcessWatcher
2. ☐ Add system stats to BCH dashboard
3. ☐ Integrate alerts with BCH notification system
4. ☐ Add resource monitoring to BCH health checks

### BCH Dashboard Integration

```python
# Example: BCH dashboard widget
from processwatcher import ProcessWatcher

def get_system_status_for_dashboard():
    """Get system status for BCH dashboard."""
    watcher = ProcessWatcher()
    info = watcher.get_system_info()
    
    return {
        'cpu': info['cpu'],
        'memory': info['memory_percent'],
        'disk': info['disk_percent'],
        'status': 'healthy' if info['cpu'] < 80 and info['memory_percent'] < 80 else 'warning'
    }
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Pre-session system checks, monitoring during builds | Python API | HIGH |
| **Atlas** | Build environment monitoring, resource tracking | Python API + CLI | HIGH |
| **Clio** | Linux system monitoring, server health | CLI | MEDIUM |
| **Nexus** | Cross-platform diagnostics | Python API | MEDIUM |
| **Bolt** | Quick system checks during task execution | CLI | LOW |

### Agent-Specific Workflows

---

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Monitor system health during orchestration and review sessions

**Integration Steps:**
1. Run system check at session start
2. Monitor resources during heavy operations
3. Alert if resources become constrained
4. Log resource usage for session review

**Example Workflow:**

```python
# Forge session start routine
from processwatcher import ProcessWatcher
from synapselink import quick_send

def forge_session_start():
    """Forge pre-session system check."""
    watcher = ProcessWatcher()
    info = watcher.get_system_info()
    
    # Check for resource issues
    warnings = []
    if info['cpu'] > 70:
        warnings.append(f"CPU at {info['cpu']:.1f}%")
    if info['memory_percent'] > 80:
        warnings.append(f"Memory at {info['memory_percent']:.1f}%")
    if info['disk_percent'] > 90:
        warnings.append(f"Disk at {info['disk_percent']:.1f}%")
    
    if warnings:
        quick_send("LOGAN", "System Warning", 
                   f"Resource constraints: {', '.join(warnings)}", 
                   priority="NORMAL")
        return False
    return True

# Use in session
if forge_session_start():
    print("[OK] System resources healthy - ready to work")
```

**Common Forge Commands:**

```bash
# Quick system check
python processwatcher.py stats

# Monitor during tool review
python processwatcher.py monitor --interval 10

# Check what's using resources during builds
python processwatcher.py list --sort memory
```

---

#### Atlas (Executor / Builder)

**Primary Use Case:** Monitor resources during tool builds and heavy execution

**Integration Steps:**
1. Check resources before starting builds
2. Monitor during long-running tasks
3. Identify resource-hungry build processes
4. Track resource history for optimization

**Example Workflow:**

```python
# Atlas build monitoring
from processwatcher import ProcessWatcher
import time

def monitor_build_resources(build_name: str, duration_minutes: int = 5):
    """Monitor resources during a build."""
    watcher = ProcessWatcher()
    
    print(f"Monitoring build: {build_name}")
    print("=" * 50)
    
    samples = []
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    while time.time() < end_time:
        info = watcher.get_system_info()
        samples.append({
            'time': time.time() - start_time,
            'cpu': info['cpu'],
            'memory': info['memory_percent']
        })
        
        # Alert if resources spike
        if info['cpu'] > 90:
            print(f"[!] CPU spike: {info['cpu']:.1f}%")
        
        time.sleep(5)
    
    # Summary
    avg_cpu = sum(s['cpu'] for s in samples) / len(samples)
    avg_mem = sum(s['memory'] for s in samples) / len(samples)
    max_cpu = max(s['cpu'] for s in samples)
    max_mem = max(s['memory'] for s in samples)
    
    print(f"\nBuild Complete: {build_name}")
    print(f"Average CPU: {avg_cpu:.1f}%, Max: {max_cpu:.1f}%")
    print(f"Average Memory: {avg_mem:.1f}%, Max: {max_mem:.1f}%")
    
    return samples
```

**Common Atlas Commands:**

```bash
# Check before starting build
python processwatcher.py stats

# Find what's consuming resources during build
python processwatcher.py list --sort cpu

# Monitor test suite execution
python processwatcher.py monitor --interval 2

# Review after build
python processwatcher.py history --lines 50
```

---

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Linux server monitoring and health checks

**Platform Considerations:**
- Cross-platform compatibility verified
- Works with both Python 3 and Python 2.7+
- No sudo required for basic operations
- Sudo recommended for full process visibility

**Example:**

```bash
# Clio system monitoring routine
echo "=== CLIO System Health Check ==="
python3 processwatcher.py stats
echo ""
echo "=== Top Resource Consumers ==="
python3 processwatcher.py list --limit 10
echo ""
echo "=== Network Activity ==="
python3 processwatcher.py network
```

**Linux-Specific Features:**

```bash
# Background monitoring with nohup
nohup python3 processwatcher.py monitor --interval 30 > /tmp/resources.log 2>&1 &

# Cron job for regular checks
# Add to crontab: crontab -e
0 * * * * /usr/bin/python3 /path/to/processwatcher.py stats >> /var/log/system_health.log

# Find high-memory processes
python3 processwatcher.py list --sort memory --limit 20
```

---

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform resource monitoring and diagnostics

**Cross-Platform Notes:**
- Same commands work on Windows, Linux, macOS
- Path handling uses pathlib for compatibility
- Network stats available on all platforms
- Process kill may need elevated privileges

**Example:**

```python
# Cross-platform system check
import platform
from processwatcher import ProcessWatcher

def nexus_cross_platform_check():
    """Platform-agnostic system health check."""
    watcher = ProcessWatcher()
    info = watcher.get_system_info()
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"CPU: {info['cpu']:.1f}%")
    print(f"Memory: {info['memory_percent']:.1f}% ({info['memory_used_gb']:.1f}GB / {info['memory_total_gb']:.1f}GB)")
    print(f"Disk: {info['disk_percent']:.1f}%")
    
    # Platform-specific info
    if platform.system() == "Windows":
        print("Note: Run as Administrator for full process visibility")
    elif platform.system() in ["Linux", "Darwin"]:
        print("Note: Use sudo for full process visibility")
    
    return info
```

---

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Quick system checks during task execution (cost-free)

**Cost Considerations:**
- ProcessWatcher runs locally with zero API costs
- Can be called frequently without budget impact
- Ideal for resource monitoring during heavy tasks

**Example:**

```bash
# Quick check before task
python processwatcher.py stats

# Find if something is blocking task
python processwatcher.py list --limit 5

# Kill stuck process
python processwatcher.py kill <PID>
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With AgentHealth

**Correlation Use Case:** Track system resources alongside agent session health

**Integration Pattern:**

```python
from agenthealth import AgentHealth
from processwatcher import ProcessWatcher

health = AgentHealth()
watcher = ProcessWatcher()

# Session with resource monitoring
session_id = "task_xyz_123"
health.start_session("FORGE", session_id=session_id)

# Log system state at session start
info = watcher.get_system_info()
health.log_metric("FORGE", "system_cpu", info['cpu'])
health.log_metric("FORGE", "system_memory", info['memory_percent'])

# Do work...

# Log at session end
info = watcher.get_system_info()
health.log_metric("FORGE", "system_cpu_end", info['cpu'])
health.log_metric("FORGE", "system_memory_end", info['memory_percent'])
health.end_session("FORGE", session_id=session_id)
```

---

### With SynapseLink

**Notification Use Case:** Alert team when resources are critical

**Integration Pattern:**

```python
from synapselink import quick_send
from processwatcher import ProcessWatcher

watcher = ProcessWatcher()
info = watcher.get_system_info()

# Alert team on critical resources
if info['cpu'] > 90 or info['memory_percent'] > 90:
    quick_send(
        "LOGAN,FORGE",
        "[ALERT] System Resources Critical",
        f"CPU: {info['cpu']:.1f}%\n"
        f"Memory: {info['memory_percent']:.1f}%\n"
        f"Action may be needed!",
        priority="HIGH"
    )

# Notify on resolution
if info['cpu'] < 50 and info['memory_percent'] < 70:
    quick_send(
        "TEAM",
        "[OK] System Resources Normal",
        f"CPU: {info['cpu']:.1f}%, Memory: {info['memory_percent']:.1f}%",
        priority="NORMAL"
    )
```

---

### With TaskQueuePro

**Task Management Use Case:** Track resources during task execution

**Integration Pattern:**

```python
from taskqueuepro import TaskQueuePro
from processwatcher import ProcessWatcher

queue = TaskQueuePro()
watcher = ProcessWatcher()

# Create task
task_id = queue.create_task(
    title="Heavy computation task",
    agent="ATLAS",
    priority=2
)

# Check resources before starting
info = watcher.get_system_info()
if info['cpu'] > 80:
    queue.add_note(task_id, f"High CPU at start: {info['cpu']:.1f}%")

# Start and track
queue.start_task(task_id)

# ... heavy work ...

# Complete with resource info
info = watcher.get_system_info()
queue.complete_task(task_id, result={
    'status': 'success',
    'final_cpu': info['cpu'],
    'final_memory': info['memory_percent']
})
```

---

### With MemoryBridge

**Context Persistence Use Case:** Store system metrics history

**Integration Pattern:**

```python
from memorybridge import MemoryBridge
from processwatcher import ProcessWatcher
from datetime import datetime

memory = MemoryBridge()
watcher = ProcessWatcher()

# Get historical metrics
metrics_history = memory.get("system_metrics", default=[])

# Add current metrics
info = watcher.get_system_info()
metrics_history.append({
    'timestamp': datetime.now().isoformat(),
    'cpu': info['cpu'],
    'memory': info['memory_percent'],
    'disk': info['disk_percent']
})

# Keep last 1000 entries
if len(metrics_history) > 1000:
    metrics_history = metrics_history[-1000:]

# Save
memory.set("system_metrics", metrics_history)
memory.sync()
```

---

### With SessionReplay

**Debugging Use Case:** Record system state during sessions

**Integration Pattern:**

```python
from sessionreplay import SessionReplay
from processwatcher import ProcessWatcher

replay = SessionReplay()
watcher = ProcessWatcher()

# Start session with system context
session_id = replay.start_session("FORGE", task="Complex build")
info = watcher.get_system_info()
replay.log_context(session_id, f"System: CPU {info['cpu']:.1f}%, Memory {info['memory_percent']:.1f}%")

# During session - log resource-heavy operations
replay.log_event(session_id, "Starting heavy operation")
info = watcher.get_system_info()
replay.log_context(session_id, f"Pre-op resources: CPU {info['cpu']:.1f}%")

# ... operation ...

info = watcher.get_system_info()
replay.log_context(session_id, f"Post-op resources: CPU {info['cpu']:.1f}%")
replay.end_session(session_id, status="COMPLETED")
```

---

### With ContextCompressor

**Token Optimization Use Case:** Include system stats in compressed context

**Integration Pattern:**

```python
from contextcompressor import ContextCompressor
from processwatcher import ProcessWatcher

compressor = ContextCompressor()
watcher = ProcessWatcher()

# Get system info
info = watcher.get_system_info()

# Create context with system state
context = f"""
System State:
- CPU: {info['cpu']:.1f}%
- Memory: {info['memory_percent']:.1f}% ({info['memory_used_gb']:.1f}GB)
- Disk: {info['disk_percent']:.1f}%

Session Notes:
[... lots of text ...]
"""

# Compress for sharing
compressed = compressor.compress_text(context, method="summary")
print(f"Compressed from {len(context)} to {len(compressed.compressed_text)} chars")
```

---

### With ConfigManager

**Configuration Use Case:** Centralize alert thresholds

**Integration Pattern:**

```python
from configmanager import ConfigManager
from processwatcher import ProcessWatcher

config = ConfigManager()
watcher = ProcessWatcher()

# Load thresholds from config
thresholds = config.get("processwatcher", {
    "cpu_warning": 70,
    "cpu_critical": 90,
    "memory_warning": 80,
    "memory_critical": 90,
    "monitor_interval": 5
})

# Use thresholds
info = watcher.get_system_info()

if info['cpu'] > thresholds['cpu_critical']:
    print(f"[X] CRITICAL: CPU at {info['cpu']:.1f}%!")
elif info['cpu'] > thresholds['cpu_warning']:
    print(f"[!] WARNING: CPU at {info['cpu']:.1f}%")
else:
    print(f"[OK] CPU at {info['cpu']:.1f}%")
```

---

### With CollabSession

**Coordination Use Case:** Monitor resources during multi-agent work

**Integration Pattern:**

```python
from collabsession import CollabSession
from processwatcher import ProcessWatcher

collab = CollabSession()
watcher = ProcessWatcher()

# Start coordinated session
session_id = collab.start_session(
    "resource_monitoring_session",
    participants=["FORGE", "ATLAS", "CLIO"]
)

# Each agent reports their system state
info = watcher.get_system_info()
collab.post_update(session_id, "FORGE", {
    'type': 'system_status',
    'cpu': info['cpu'],
    'memory': info['memory_percent'],
    'status': 'ready' if info['cpu'] < 80 else 'constrained'
})

# Coordinate based on collective resources
statuses = collab.get_updates(session_id)
# ... coordinate work based on available resources ...
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✅ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

---

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to agent session start routines
2. ☐ Create integration examples with existing tools
3. ☐ Add to BCH health monitoring
4. ☐ Set up resource alerting

**Success Criteria:**
- Used daily by at least 3 agents
- Integrated with AgentHealth and SynapseLink

---

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements based on feedback
3. ☐ Create advanced automation examples
4. ☐ Add to BCH dashboard

**Success Criteria:**
- Measurable improvement in issue detection
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: Target 5/5
- Daily usage count: Track via Synapse mentions
- Integration with other tools: Target 5+ integrations

**Efficiency Metrics:**
- Issues caught early: Track resource alerts
- Time to diagnose problems: Target 50% reduction
- False positive rate: Target < 10%

**Quality Metrics:**
- Bug reports: Track on GitHub
- Feature requests: Collect and prioritize
- User satisfaction: Qualitative feedback

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from processwatcher import ProcessWatcher

# Direct script usage
import subprocess
result = subprocess.run(['python', 'processwatcher.py', 'stats'], capture_output=True)
```

### Configuration Integration

**Config File:** `~/.processwatcher/` (auto-created)

**Shared Config with Other Tools:**

```json
{
  "processwatcher": {
    "monitor_interval": 5,
    "alert_thresholds": {
      "cpu_warning": 70,
      "cpu_critical": 90,
      "memory_warning": 80,
      "memory_critical": 90
    }
  }
}
```

### Error Handling Integration

**Standardized Error Codes:**
- 0: Success
- 1: General error / Process not found
- 2: Access denied (need elevated privileges)

### Logging Integration

**Log Format:** CSV (compatible with standard tools)

**Log Location:** `~/.processwatcher/resource_log.txt`

**Log Entry Format:**
```
timestamp,cpu%,memory%,disk%
2026-01-28T10:15:32.123456,15.2,62.4,45.3
```

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly review
- Security patches: Immediate

### Support Channels

- GitHub Issues: Bug reports and feature requests
- Synapse: Team Brain discussions
- Direct to Forge: Complex integration issues

### Known Limitations

- Requires psutil dependency (not stdlib-only)
- Process kill requires elevated privileges for some processes
- Network stats are cumulative since boot (not per-session)

### Planned Improvements

- [ ] Add GPU monitoring (if nvidia-smi available)
- [ ] Add per-process network stats
- [ ] Add alert thresholds configuration file
- [ ] Add HTML report generation

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Reference: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/ProcessWatcher

---

**Last Updated:** January 28, 2026
**Maintained By:** Forge (Team Brain)
**For:** Logan Smith / Metaphy LLC
