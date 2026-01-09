#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProcessWatcher - Smart Process Monitor & Manager
=================================================
Monitor system resources, manage processes, and get alerts - all from CLI.

Author: Team Brain / Forge
License: MIT
"""

import os
import sys
import time
import signal
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    except:
        pass

try:
    import psutil
except ImportError:
    print("[X] Error: psutil not installed!")
    print("Install with: pip install psutil")
    sys.exit(1)


class ProcessWatcher:
    """Main ProcessWatcher application class."""

    def __init__(self):
        """Initialize ProcessWatcher."""
        self.config_dir = Path.home() / ".processwatcher"
        self.config_dir.mkdir(exist_ok=True)
        self.log_file = self.config_dir / "resource_log.txt"

    def get_system_info(self):
        """Get current system resource usage."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': memory.used / (1024**3),
            'memory_total_gb': memory.total / (1024**3),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used / (1024**3),
            'disk_total_gb': disk.total / (1024**3),
        }

    def display_system_stats(self):
        """Display current system statistics."""
        info = self.get_system_info()
        
        print("\n" + "="*50)
        print("  SYSTEM RESOURCE MONITOR")
        print("="*50)
        print(f"\nCPU Usage:    {info['cpu']:.1f}%")
        print(f"Memory Usage: {info['memory_percent']:.1f}% ({info['memory_used_gb']:.1f}GB / {info['memory_total_gb']:.1f}GB)")
        print(f"Disk Usage:   {info['disk_percent']:.1f}% ({info['disk_used_gb']:.1f}GB / {info['disk_total_gb']:.1f}GB)")
        print("="*50 + "\n")

    def list_processes(self, sort_by='cpu', limit=20, show_all=False):
        """List running processes sorted by resource usage."""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                # Skip system processes with 0 usage unless show_all
                if not show_all and pinfo['cpu_percent'] == 0 and pinfo['memory_percent'] == 0:
                    continue
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort processes
        reverse = True
        if sort_by == 'cpu':
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=reverse)
        elif sort_by == 'memory':
            processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=reverse)
        elif sort_by == 'name':
            processes.sort(key=lambda x: x['name'].lower())
            reverse = False

        # Limit results
        if limit:
            processes = processes[:limit]

        if not processes:
            print("No processes found.")
            return

        # Display
        print(f"\n[Top {len(processes)} processes by {sort_by.upper()}]")
        print(f"\n{'PID':<8} {'NAME':<30} {'CPU%':<8} {'MEM%':<8} {'STATUS':<10}")
        print("-" * 70)
        
        for proc in processes:
            pid = proc['pid']
            name = proc['name'][:28] if proc['name'] else 'N/A'
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            status = proc['status']
            
            print(f"{pid:<8} {name:<30} {cpu:<8.1f} {mem:<8.2f} {status:<10}")
        
        print()

    def find_process(self, search_term):
        """Find processes matching search term."""
        matches = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                if search_term.lower() in pinfo['name'].lower():
                    matches.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not matches:
            print(f"No processes found matching '{search_term}'")
            return

        print(f"\n[Found {len(matches)} process(es) matching '{search_term}']")
        print(f"\n{'PID':<8} {'NAME':<30} {'CPU%':<8} {'MEM%':<8} {'STATUS':<10}")
        print("-" * 70)
        
        for proc in matches:
            pid = proc['pid']
            name = proc['name'][:28]
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            status = proc['status']
            
            print(f"{pid:<8} {name:<30} {cpu:<8.1f} {mem:<8.2f} {status:<10}")
        
        print()

    def get_process_details(self, pid):
        """Get detailed information about a process."""
        try:
            proc = psutil.Process(pid)
            
            print(f"\n{'='*60}")
            print(f"  Process Details - PID {pid}")
            print(f"{'='*60}\n")
            
            print(f"Name:         {proc.name()}")
            print(f"PID:          {proc.pid}")
            print(f"Status:       {proc.status()}")
            print(f"CPU:          {proc.cpu_percent(interval=0.5):.1f}%")
            print(f"Memory:       {proc.memory_percent():.2f}%")
            print(f"Memory (MB):  {proc.memory_info().rss / (1024*1024):.1f} MB")
            
            try:
                print(f"User:         {proc.username()}")
            except:
                print(f"User:         N/A")
            
            try:
                create_time = datetime.fromtimestamp(proc.create_time())
                print(f"Started:      {create_time.strftime('%Y-%m-%d %H:%M:%S')}")
            except:
                print(f"Started:      N/A")
            
            try:
                print(f"Exe:          {proc.exe()}")
            except:
                print(f"Exe:          N/A")
            
            try:
                print(f"CWD:          {proc.cwd()}")
            except:
                print(f"CWD:          N/A")
            
            try:
                cmdline = ' '.join(proc.cmdline())
                if len(cmdline) > 100:
                    cmdline = cmdline[:97] + "..."
                print(f"Command:      {cmdline}")
            except:
                print(f"Command:      N/A")
            
            print(f"\n{'='*60}\n")
            return True
            
        except psutil.NoSuchProcess:
            print(f"[X] Process {pid} not found!")
            return False
        except psutil.AccessDenied:
            print(f"[X] Access denied to process {pid}!")
            return False

    def kill_process(self, pid, force=False):
        """Kill a process by PID."""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            
            if force:
                proc.kill()  # SIGKILL
                print(f"[OK] Force killed process {pid} ({name})")
            else:
                proc.terminate()  # SIGTERM
                print(f"[OK] Terminated process {pid} ({name})")
                print("     (Use --force to force kill if needed)")
            
            return True
            
        except psutil.NoSuchProcess:
            print(f"[X] Process {pid} not found!")
            return False
        except psutil.AccessDenied:
            print(f"[X] Access denied! Cannot kill process {pid}")
            print("     (Try running with administrator/sudo)")
            return False

    def monitor_realtime(self, interval=2):
        """Monitor system resources in real-time."""
        print("\n[Real-time monitoring - Press Ctrl+C to stop]\n")
        print(f"{'Time':<20} {'CPU%':<8} {'MEM%':<8} {'DISK%':<8}")
        print("-" * 50)
        
        try:
            while True:
                info = self.get_system_info()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"{timestamp:<20} {info['cpu']:<8.1f} {info['memory_percent']:<8.1f} {info['disk_percent']:<8.1f}")
                
                # Log to file
                self.log_resource(info)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n[Monitoring stopped]")

    def log_resource(self, info):
        """Log resource usage to file."""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = f"{timestamp},{info['cpu']:.1f},{info['memory_percent']:.1f},{info['disk_percent']:.1f}\n"
            
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except:
            pass  # Silent fail for logging

    def show_resource_history(self, lines=20):
        """Show resource usage history from log."""
        if not self.log_file.exists():
            print("No resource history found.")
            print("Run 'processwatcher monitor' to start logging.")
            return

        try:
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
            
            # Get last N lines
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            if not recent_lines:
                print("No history data available.")
                return
            
            print(f"\n[Last {len(recent_lines)} resource measurements]")
            print(f"\n{'Timestamp':<25} {'CPU%':<8} {'MEM%':<8} {'DISK%':<8}")
            print("-" * 55)
            
            for line in recent_lines:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    timestamp = parts[0][:19]  # Trim microseconds
                    cpu = float(parts[1])
                    mem = float(parts[2])
                    disk = float(parts[3])
                    print(f"{timestamp:<25} {cpu:<8.1f} {mem:<8.1f} {disk:<8.1f}")
            
            print()
            
        except Exception as e:
            print(f"[X] Error reading history: {e}")

    def get_network_stats(self):
        """Get network I/O statistics."""
        net_io = psutil.net_io_counters()
        
        print("\n" + "="*50)
        print("  NETWORK STATISTICS")
        print("="*50)
        print(f"\nBytes Sent:     {net_io.bytes_sent / (1024**3):.2f} GB")
        print(f"Bytes Received: {net_io.bytes_recv / (1024**3):.2f} GB")
        print(f"Packets Sent:   {net_io.packets_sent:,}")
        print(f"Packets Recv:   {net_io.packets_recv:,}")
        print("="*50 + "\n")


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="ProcessWatcher - Smart Process Monitor & Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  processwatcher stats                    # Show system stats
  processwatcher list                     # List top 20 processes by CPU
  processwatcher list --sort memory       # Sort by memory usage
  processwatcher list --limit 50          # Show top 50
  processwatcher find chrome              # Find processes by name
  processwatcher info 1234                # Get details for PID 1234
  processwatcher kill 1234                # Terminate process 1234
  processwatcher kill 1234 --force        # Force kill process 1234
  processwatcher monitor                  # Real-time monitoring
  processwatcher history                  # Show resource history
  processwatcher network                  # Network statistics
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Stats command
    subparsers.add_parser("stats", help="Show system resource statistics")

    # List command
    parser_list = subparsers.add_parser("list", help="List running processes")
    parser_list.add_argument("--sort", choices=["cpu", "memory", "name"], default="cpu", help="Sort by")
    parser_list.add_argument("--limit", type=int, default=20, help="Number of processes to show")
    parser_list.add_argument("--all", action="store_true", help="Show all processes including idle ones")

    # Find command
    parser_find = subparsers.add_parser("find", help="Find processes by name")
    parser_find.add_argument("term", help="Search term")

    # Info command
    parser_info = subparsers.add_parser("info", help="Show process details")
    parser_info.add_argument("pid", type=int, help="Process ID")

    # Kill command
    parser_kill = subparsers.add_parser("kill", help="Kill a process")
    parser_kill.add_argument("pid", type=int, help="Process ID")
    parser_kill.add_argument("--force", action="store_true", help="Force kill (SIGKILL)")

    # Monitor command
    parser_monitor = subparsers.add_parser("monitor", help="Real-time resource monitoring")
    parser_monitor.add_argument("--interval", type=int, default=2, help="Update interval in seconds")

    # History command
    parser_history = subparsers.add_parser("history", help="Show resource usage history")
    parser_history.add_argument("--lines", type=int, default=20, help="Number of entries to show")

    # Network command
    subparsers.add_parser("network", help="Show network statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    watcher = ProcessWatcher()

    if args.command == "stats":
        watcher.display_system_stats()

    elif args.command == "list":
        watcher.list_processes(sort_by=args.sort, limit=args.limit, show_all=args.all)

    elif args.command == "find":
        watcher.find_process(args.term)

    elif args.command == "info":
        watcher.get_process_details(args.pid)

    elif args.command == "kill":
        watcher.kill_process(args.pid, force=args.force)

    elif args.command == "monitor":
        watcher.monitor_realtime(interval=args.interval)

    elif args.command == "history":
        watcher.show_resource_history(lines=args.lines)

    elif args.command == "network":
        watcher.get_network_stats()


if __name__ == "__main__":
    main()
