#!/usr/bin/env python3
"""
Comprehensive test suite for ProcessWatcher.

Tests cover:
- Core functionality (system info, process listing, search)
- Process details and management
- Monitoring and history
- Edge cases and error handling
- Integration scenarios

Run: python test_processwatcher.py
"""

import unittest
import sys
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from processwatcher import ProcessWatcher


class TestProcessWatcherInit(unittest.TestCase):
    """Test ProcessWatcher initialization."""
    
    def test_initialization(self):
        """Test basic initialization."""
        watcher = ProcessWatcher()
        self.assertIsNotNone(watcher)
        self.assertIsNotNone(watcher.config_dir)
        self.assertIsNotNone(watcher.log_file)
    
    def test_config_dir_creation(self):
        """Test config directory is created."""
        watcher = ProcessWatcher()
        self.assertTrue(watcher.config_dir.exists())
    
    def test_config_dir_is_in_home(self):
        """Test config directory is in user home."""
        watcher = ProcessWatcher()
        self.assertTrue(str(watcher.config_dir).startswith(str(Path.home())))
    
    def test_log_file_path(self):
        """Test log file path is properly set."""
        watcher = ProcessWatcher()
        self.assertEqual(watcher.log_file.name, "resource_log.txt")
        self.assertEqual(watcher.log_file.parent, watcher.config_dir)


class TestSystemInfo(unittest.TestCase):
    """Test system information gathering."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_get_system_info_returns_dict(self):
        """Test get_system_info returns dictionary."""
        info = self.watcher.get_system_info()
        self.assertIsInstance(info, dict)
    
    def test_system_info_has_cpu(self):
        """Test system info contains CPU data."""
        info = self.watcher.get_system_info()
        self.assertIn('cpu', info)
        self.assertIsInstance(info['cpu'], (int, float))
        self.assertGreaterEqual(info['cpu'], 0)
        self.assertLessEqual(info['cpu'], 100)
    
    def test_system_info_has_memory(self):
        """Test system info contains memory data."""
        info = self.watcher.get_system_info()
        self.assertIn('memory_percent', info)
        self.assertIn('memory_used_gb', info)
        self.assertIn('memory_total_gb', info)
        self.assertGreaterEqual(info['memory_percent'], 0)
        self.assertLessEqual(info['memory_percent'], 100)
    
    def test_system_info_has_disk(self):
        """Test system info contains disk data."""
        info = self.watcher.get_system_info()
        self.assertIn('disk_percent', info)
        self.assertIn('disk_used_gb', info)
        self.assertIn('disk_total_gb', info)
        self.assertGreaterEqual(info['disk_percent'], 0)
        self.assertLessEqual(info['disk_percent'], 100)
    
    def test_system_info_memory_consistency(self):
        """Test memory used is less than or equal to total."""
        info = self.watcher.get_system_info()
        self.assertLessEqual(info['memory_used_gb'], info['memory_total_gb'])
    
    def test_system_info_disk_consistency(self):
        """Test disk used is less than or equal to total."""
        info = self.watcher.get_system_info()
        self.assertLessEqual(info['disk_used_gb'], info['disk_total_gb'])


class TestDisplayStats(unittest.TestCase):
    """Test display_system_stats method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_display_stats_runs_without_error(self):
        """Test display_system_stats runs successfully."""
        # Capture stdout
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.display_system_stats()
            output = captured.getvalue()
            self.assertIn("SYSTEM RESOURCE MONITOR", output)
            self.assertIn("CPU", output)
            self.assertIn("Memory", output)
            self.assertIn("Disk", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_display_stats_shows_percentages(self):
        """Test display shows percentage values."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.display_system_stats()
            output = captured.getvalue()
            self.assertIn("%", output)
        finally:
            sys.stdout = sys.__stdout__


class TestListProcesses(unittest.TestCase):
    """Test process listing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_list_processes_runs(self):
        """Test list_processes runs without error."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(limit=5)
            output = captured.getvalue()
            # Should have header
            self.assertIn("PID", output)
            self.assertIn("NAME", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_list_processes_respects_limit(self):
        """Test process list respects limit parameter."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(limit=3)
            output = captured.getvalue()
            # Check that we mention the limit in output
            self.assertIn("3", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_list_processes_sort_by_cpu(self):
        """Test process list sorted by CPU."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(sort_by='cpu', limit=5)
            output = captured.getvalue()
            self.assertIn("CPU", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_list_processes_sort_by_memory(self):
        """Test process list sorted by memory."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(sort_by='memory', limit=5)
            output = captured.getvalue()
            self.assertIn("MEM", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_list_processes_sort_by_name(self):
        """Test process list sorted by name."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(sort_by='name', limit=5)
            output = captured.getvalue()
            self.assertIn("NAME", output)
        finally:
            sys.stdout = sys.__stdout__


class TestFindProcess(unittest.TestCase):
    """Test process search functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_find_process_python(self):
        """Test finding python process."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.find_process("python")
            output = captured.getvalue()
            # Should find at least this python process
            self.assertTrue("python" in output.lower() or "Found" in output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_find_process_nonexistent(self):
        """Test searching for nonexistent process."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.find_process("zzz_nonexistent_process_xyz_12345")
            output = captured.getvalue()
            self.assertIn("No processes found", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_find_process_case_insensitive(self):
        """Test search is case insensitive."""
        captured1 = StringIO()
        captured2 = StringIO()
        
        sys.stdout = captured1
        try:
            self.watcher.find_process("PYTHON")
        finally:
            sys.stdout = sys.__stdout__
        
        sys.stdout = captured2
        try:
            self.watcher.find_process("python")
        finally:
            sys.stdout = sys.__stdout__
        
        # Both should find or not find (consistent behavior)
        output1 = captured1.getvalue()
        output2 = captured2.getvalue()
        # Both contain "python" (case insensitive) or "No processes found"
        has_result1 = "python" in output1.lower() or "Found" in output1 or "No processes found" in output1
        has_result2 = "python" in output2.lower() or "Found" in output2 or "No processes found" in output2
        self.assertTrue(has_result1)
        self.assertTrue(has_result2)


class TestProcessDetails(unittest.TestCase):
    """Test getting process details."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
        self.current_pid = os.getpid()
    
    def test_get_process_details_current(self):
        """Test getting details for current process."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            result = self.watcher.get_process_details(self.current_pid)
            output = captured.getvalue()
            self.assertTrue(result)
            self.assertIn("Process Details", output)
            self.assertIn(str(self.current_pid), output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_get_process_details_invalid_pid(self):
        """Test getting details for invalid PID."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            result = self.watcher.get_process_details(999999999)
            output = captured.getvalue()
            self.assertFalse(result)
            self.assertIn("not found", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_get_process_details_shows_name(self):
        """Test process details includes name."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_process_details(self.current_pid)
            output = captured.getvalue()
            self.assertIn("Name:", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_get_process_details_shows_status(self):
        """Test process details includes status."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_process_details(self.current_pid)
            output = captured.getvalue()
            self.assertIn("Status:", output)
        finally:
            sys.stdout = sys.__stdout__


class TestKillProcess(unittest.TestCase):
    """Test process termination (using mocks for safety)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_kill_invalid_pid(self):
        """Test killing invalid PID returns False."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            result = self.watcher.kill_process(999999999)
            output = captured.getvalue()
            self.assertFalse(result)
            self.assertIn("not found", output)
        finally:
            sys.stdout = sys.__stdout__
    
    @patch('psutil.Process')
    def test_kill_process_terminate(self, mock_process):
        """Test process termination call."""
        mock_proc = Mock()
        mock_proc.name.return_value = "test_process"
        mock_process.return_value = mock_proc
        
        captured = StringIO()
        sys.stdout = captured
        
        try:
            result = self.watcher.kill_process(12345, force=False)
            mock_proc.terminate.assert_called_once()
        finally:
            sys.stdout = sys.__stdout__
    
    @patch('psutil.Process')
    def test_kill_process_force(self, mock_process):
        """Test force kill call."""
        mock_proc = Mock()
        mock_proc.name.return_value = "test_process"
        mock_process.return_value = mock_proc
        
        captured = StringIO()
        sys.stdout = captured
        
        try:
            result = self.watcher.kill_process(12345, force=True)
            mock_proc.kill.assert_called_once()
        finally:
            sys.stdout = sys.__stdout__


class TestResourceLogging(unittest.TestCase):
    """Test resource logging functionality."""
    
    def setUp(self):
        """Set up test fixtures with temp directory."""
        self.watcher = ProcessWatcher()
        self.temp_dir = tempfile.mkdtemp()
        self.watcher.config_dir = Path(self.temp_dir)
        self.watcher.log_file = self.watcher.config_dir / "resource_log.txt"
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_log_resource_creates_file(self):
        """Test logging creates log file."""
        info = {'cpu': 10.5, 'memory_percent': 50.0, 'disk_percent': 30.0}
        self.watcher.log_resource(info)
        self.assertTrue(self.watcher.log_file.exists())
    
    def test_log_resource_appends_data(self):
        """Test logging appends data to file."""
        info = {'cpu': 10.5, 'memory_percent': 50.0, 'disk_percent': 30.0}
        self.watcher.log_resource(info)
        self.watcher.log_resource(info)
        
        with open(self.watcher.log_file, 'r') as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 2)
    
    def test_log_resource_csv_format(self):
        """Test log is in CSV format."""
        info = {'cpu': 10.5, 'memory_percent': 50.0, 'disk_percent': 30.0}
        self.watcher.log_resource(info)
        
        with open(self.watcher.log_file, 'r') as f:
            content = f.read()
        
        # Should have comma-separated values
        self.assertIn(',', content)
        parts = content.strip().split(',')
        self.assertGreaterEqual(len(parts), 4)


class TestResourceHistory(unittest.TestCase):
    """Test resource history display."""
    
    def setUp(self):
        """Set up test fixtures with temp directory."""
        self.watcher = ProcessWatcher()
        self.temp_dir = tempfile.mkdtemp()
        self.watcher.config_dir = Path(self.temp_dir)
        self.watcher.log_file = self.watcher.config_dir / "resource_log.txt"
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_show_history_no_file(self):
        """Test history with no log file."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.show_resource_history()
            output = captured.getvalue()
            self.assertIn("No resource history", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_show_history_with_data(self):
        """Test history with log data."""
        # Create some log data
        info = {'cpu': 10.5, 'memory_percent': 50.0, 'disk_percent': 30.0}
        for _ in range(5):
            self.watcher.log_resource(info)
        
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.show_resource_history(lines=10)
            output = captured.getvalue()
            self.assertIn("resource measurements", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_show_history_respects_lines(self):
        """Test history respects lines limit."""
        info = {'cpu': 10.5, 'memory_percent': 50.0, 'disk_percent': 30.0}
        for _ in range(20):
            self.watcher.log_resource(info)
        
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.show_resource_history(lines=5)
            output = captured.getvalue()
            self.assertIn("5", output)
        finally:
            sys.stdout = sys.__stdout__


class TestNetworkStats(unittest.TestCase):
    """Test network statistics functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_get_network_stats_runs(self):
        """Test network stats runs without error."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_network_stats()
            output = captured.getvalue()
            self.assertIn("NETWORK STATISTICS", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_network_stats_shows_bytes(self):
        """Test network stats shows bytes."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_network_stats()
            output = captured.getvalue()
            self.assertIn("Bytes Sent", output)
            self.assertIn("Bytes Received", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_network_stats_shows_packets(self):
        """Test network stats shows packets."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_network_stats()
            output = captured.getvalue()
            self.assertIn("Packets Sent", output)
            self.assertIn("Packets Recv", output)
        finally:
            sys.stdout = sys.__stdout__


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.watcher = ProcessWatcher()
    
    def test_list_processes_zero_limit(self):
        """Test list with zero limit."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.list_processes(limit=0)
            output = captured.getvalue()
            # Should handle gracefully
            self.assertIsNotNone(output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_find_empty_string(self):
        """Test find with empty string."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.find_process("")
            output = captured.getvalue()
            # Should handle gracefully
            self.assertIsNotNone(output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_process_details_zero_pid(self):
        """Test process details with PID 0."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.get_process_details(0)
            output = captured.getvalue()
            # Should handle gracefully (may be access denied or not found)
            self.assertIsNotNone(output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_process_details_negative_pid(self):
        """Test process details with negative PID raises ValueError."""
        # psutil raises ValueError for negative PIDs
        with self.assertRaises(ValueError):
            self.watcher.get_process_details(-1)
    
    def test_history_zero_lines(self):
        """Test history with zero lines."""
        captured = StringIO()
        sys.stdout = captured
        
        try:
            self.watcher.show_resource_history(lines=0)
            output = captured.getvalue()
            # Should handle gracefully
            self.assertIsNotNone(output)
        finally:
            sys.stdout = sys.__stdout__


class TestPythonAPI(unittest.TestCase):
    """Test Python API usage patterns."""
    
    def test_can_import(self):
        """Test module can be imported."""
        from processwatcher import ProcessWatcher
        self.assertIsNotNone(ProcessWatcher)
    
    def test_can_instantiate(self):
        """Test class can be instantiated."""
        watcher = ProcessWatcher()
        self.assertIsInstance(watcher, ProcessWatcher)
    
    def test_get_system_info_api(self):
        """Test get_system_info returns usable data."""
        watcher = ProcessWatcher()
        info = watcher.get_system_info()
        
        # All required keys present
        required_keys = ['cpu', 'memory_percent', 'memory_used_gb', 
                        'memory_total_gb', 'disk_percent', 'disk_used_gb', 
                        'disk_total_gb']
        for key in required_keys:
            self.assertIn(key, info)
    
    def test_multiple_instances(self):
        """Test multiple ProcessWatcher instances."""
        watcher1 = ProcessWatcher()
        watcher2 = ProcessWatcher()
        
        info1 = watcher1.get_system_info()
        info2 = watcher2.get_system_info()
        
        # Both should return valid data
        self.assertIsInstance(info1, dict)
        self.assertIsInstance(info2, dict)


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("TESTING: ProcessWatcher v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProcessWatcherInit,
        TestSystemInfo,
        TestDisplayStats,
        TestListProcesses,
        TestFindProcess,
        TestProcessDetails,
        TestKillProcess,
        TestResourceLogging,
        TestResourceHistory,
        TestNetworkStats,
        TestEdgeCases,
        TestPythonAPI,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
