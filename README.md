<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f81380d1-8513-4b0e-adde-3f99e5afc780" />

# ⚡ ProcessWatcher - Smart Process Monitor & Manager

**Monitor system resources and manage processes like a pro - all from the command line!**

Never wonder "what's slowing down my computer?" again. ProcessWatcher gives you instant insights into CPU, memory, disk usage, and makes process management effortless.

Perfect for:
- 🔍 Finding resource hogs
- 🚀 Optimizing system performance
- 🛑 Killing stuck processes
- 📊 Tracking resource usage over time
- 💻 System administration
- 🎯 Development and testing

---

## ✨ Features

- **📊 System Stats** - Instant CPU/Memory/Disk usage
- **📋 Process List** - Sort by CPU, memory, or name
- **🔍 Smart Search** - Find processes instantly
- **🔬 Process Details** - Complete info for any process
- **🛑 Process Management** - Terminate or force kill
- **📈 Real-Time Monitoring** - Live resource tracking
- **📜 Usage History** - Track trends over time
- **🌐 Network Stats** - Monitor network I/O
- **🌍 Cross-Platform** - Windows, macOS, Linux
- **⚡ Lightning Fast** - Optimized performance

---

## 📥 Installation

### Requirements

- Python 3.7+
- psutil library

### Step 1: Install Dependencies

```bash
pip install psutil
```

### Step 2: Download ProcessWatcher

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/ProcessWatcher.git
cd ProcessWatcher

# Or download ZIP and extract
```

### Step 3: Start Using!

```bash
python processwatcher.py stats
```

---

## 🚀 Quick Start

### Check System Resources

```bash
python processwatcher.py stats
```

**Output:**
```
==================================================
  SYSTEM RESOURCE MONITOR
==================================================

CPU Usage:    15.2%
Memory Usage: 62.4% (10.0GB / 16.0GB)
Disk Usage:   45.3% (226.5GB / 500.0GB)
==================================================
```

### List Top Processes

```bash
python processwatcher.py list
```

### Find a Process

```bash
python processwatcher.py find chrome
```

### Monitor in Real-Time

```bash
python processwatcher.py monitor
```

---

## 📖 Complete Usage Guide

### 1. System Statistics

Get instant overview of system resources:

```bash
python processwatcher.py stats
```

Shows:
- CPU usage percentage
- Memory used and total
- Disk used and total

### 2. List Processes

**List top 20 by CPU:**
```bash
python processwatcher.py list
```

**Sort by memory:**
```bash
python processwatcher.py list --sort memory
```

**Show top 50:**
```bash
python processwatcher.py list --limit 50
```

**Show all processes (including idle):**
```bash
python processwatcher.py list --all
```

### 3. Find Processes

Search for processes by name:

```bash
python processwatcher.py find python
python processwatcher.py find chrome
python processwatcher.py find code
```

Returns all matching processes with CPU/memory usage.

### 4. Process Details

Get complete information about a specific process:

```bash
python processwatcher.py info 1234
```

Shows:
- Process name and PID
- Status and user
- CPU and memory usage
- Start time
- Executable path
- Working directory
- Command line

### 5. Kill Processes

**Graceful termination (SIGTERM):**
```bash
python processwatcher.py kill 1234
```

**Force kill (SIGKILL):**
```bash
python processwatcher.py kill 1234 --force
```

**⚠️ Note:** Some processes require administrator/sudo privileges.

### 6. Real-Time Monitoring

Monitor resources live with automatic logging:

```bash
python processwatcher.py monitor
```

**Custom update interval:**
```bash
python processwatcher.py monitor --interval 5
```

Press Ctrl+C to stop monitoring.

**Data is automatically logged to:** `~/.processwatcher/resource_log.txt`

### 7. Resource History

View historical resource usage:

```bash
python processwatcher.py history
```

**Show last 50 entries:**
```bash
python processwatcher.py history --lines 50
```

### 8. Network Statistics

Check network I/O:

```bash
python processwatcher.py network
```

Shows:
- Total bytes sent/received
- Packets sent/received

---

## 💡 Real-World Examples

### Example 1: Find What's Slowing Down Your Computer

```bash
# Check overall stats
python processwatcher.py stats

# List top CPU users
python processwatcher.py list

# Get details on the top process
python processwatcher.py info 5432
```

### Example 2: Kill a Stuck Application

```bash
# Find the process
python processwatcher.py find "MyApp"

# Get details
python processwatcher.py info 8765

# Kill it
python processwatcher.py kill 8765
```

### Example 3: Monitor During Heavy Task

```bash
# Start monitoring
python processwatcher.py monitor

# Run your heavy task in another terminal
# Watch real-time CPU/memory usage
# Press Ctrl+C when done

# Review history
python processwatcher.py history
```

### Example 4: Track Resource Usage Over Time

```bash
# Run monitor in background (or in screen/tmux)
python processwatcher.py monitor &

# Let it run for hours/days
# Later, check history
python processwatcher.py history --lines 100
```

### Example 5: Find Memory Leaks

```bash
# Monitor specific app
python processwatcher.py find myapp

# Note the memory usage
# Do this periodically to check if memory keeps growing
```

---

## 🎯 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `stats` | Show system resource statistics | `processwatcher.py stats` |
| `list` | List running processes | `processwatcher.py list --sort memory` |
| `find <term>` | Find processes by name | `processwatcher.py find chrome` |
| `info <pid>` | Show process details | `processwatcher.py info 1234` |
| `kill <pid>` | Terminate process | `processwatcher.py kill 1234` |
| `kill <pid> --force` | Force kill process | `processwatcher.py kill 1234 --force` |
| `monitor` | Real-time monitoring | `processwatcher.py monitor --interval 2` |
| `history` | Show resource history | `processwatcher.py history --lines 50` |
| `network` | Network I/O statistics | `processwatcher.py network` |

---

## 📂 File Storage

ProcessWatcher stores logs in your home directory:

```
~/.processwatcher/
└── resource_log.txt    # Resource usage history (CSV format)
```

**Windows:** `C:\Users\YourName\.processwatcher\`  
**Linux/Mac:** `/home/username/.processwatcher/`

**Log format:** `timestamp,cpu%,memory%,disk%`

---

## 🔧 Advanced Usage

### Create Aliases for Quick Access

**Linux/Mac (.bashrc or .zshrc):**
```bash
alias pw='python /path/to/processwatcher.py'
alias pwstats='python /path/to/processwatcher.py stats'
alias pwlist='python /path/to/processwatcher.py list'
alias pwmon='python /path/to/processwatcher.py monitor'
```

**Windows (PowerShell profile):**
```powershell
Function pw { python C:\path\to\processwatcher.py $args }
Function pwstats { python C:\path\to\processwatcher.py stats }
```

### Automated Monitoring

**Start on system boot (Linux systemd):**
```bash
# Create service file: /etc/systemd/system/processwatcher.service
[Unit]
Description=ProcessWatcher Resource Monitor

[Service]
ExecStart=/usr/bin/python3 /path/to/processwatcher.py monitor
Restart=always

[Install]
WantedBy=multi-user.target
```

**Scheduled monitoring (Cron):**
```bash
# Add to crontab: Monitor every hour
0 * * * * /usr/bin/python3 /path/to/processwatcher.py stats >> /tmp/pw.log
```

### Parse History Data

The log file is CSV format, easy to analyze:

```python
import pandas as pd
df = pd.read_csv('~/.processwatcher/resource_log.txt', 
                 names=['timestamp', 'cpu', 'memory', 'disk'])
print(df['cpu'].mean())  # Average CPU usage
```

---

## 🐛 Troubleshooting

### "psutil not installed"
**Solution:**
```bash
pip install psutil
```

### "Access denied" when killing process
**Solution:** Run with elevated privileges:
```bash
# Windows
Run Command Prompt as Administrator

# Linux/Mac
sudo python processwatcher.py kill 1234
```

### "No processes found"
**Solution:** Some processes might be system-protected. Try:
```bash
python processwatcher.py list --all
```

### History shows no data
**Solution:** Run monitor first to start logging:
```bash
python processwatcher.py monitor
# Let it run for a bit, then Ctrl+C
python processwatcher.py history
```

---

## 🎨 Why ProcessWatcher?

**vs. Task Manager (Windows) / Activity Monitor (Mac):**
- ✅ Faster (CLI = instant)
- ✅ Scriptable (automation friendly)
- ✅ History logging (built-in)
- ✅ Remote accessible (SSH)

**vs. top/htop (Linux):**
- ✅ Cross-platform (same commands everywhere)
- ✅ Easier to use (simpler syntax)
- ✅ History tracking (not in top/htop)
- ✅ Process search (find by name)

**vs. Other Python tools:**
- ✅ More features (stats + list + monitor + history)
- ✅ Better UX (clear output format)
- ✅ Actively developed
- ✅ Comprehensive docs

---

## 🔒 Privacy & Security

- ✅ **Local only** - No network calls, no telemetry
- ✅ **Open source** - Full transparency
- ✅ **No admin required** - Works with normal privileges (except kill)
- ✅ **Minimal dependencies** - Only psutil

ProcessWatcher respects your privacy and doesn't share any data.

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/c495494d-b01c-4daa-9281-6ade452bb71e" />


## 🤝 Contributing

Found a bug? Have a feature idea?

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

## 🌟 Support

If you find ProcessWatcher useful:
- ⭐ Star this repository
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features
- 📢 Share with fellow developers!

---

**Created by Team Brain**  
**Part of the Holy Grail Automation Project**

Take control of your system resources! ⚡
