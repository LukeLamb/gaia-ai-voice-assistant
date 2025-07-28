#!/usr/bin/env python3
"""
Gaia AI Test Launcher
Convenience script to run tests from project root
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch test runner from project root"""
    # Change to tests directory
    tests_dir = Path(__file__).parent / "tests"
    
    if not tests_dir.exists():
        print("❌ Tests directory not found!")
        return 1
    
    # Change directory and run tests
    os.chdir(tests_dir)
    
    # Pass all arguments to the test runner
    cmd = [sys.executable, "run_tests.py"] + sys.argv[1:]
    
    print("🚀 Launching Gaia AI Test Suite...")
    print(f"📂 Working directory: {tests_dir}")
    print(f"💻 Command: {' '.join(cmd)}")
    print("-" * 50)
    
    return subprocess.call(cmd)

if __name__ == "__main__":
    sys.exit(main())
