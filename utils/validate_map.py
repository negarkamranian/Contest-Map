#!/usr/bin/env python3
"""
Map validation utility for CTF contest submissions.
"""

import os
import sys
import json
import subprocess
import time
import requests
from pathlib import Path

def validate_map_structure(map_path):
    """Validate that the map has the required structure."""
    required_files = [
        'frontend/server.py',
        'frontend/templates/index.html',
        'flags.json',
        'agent_example.py',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (Path(map_path) / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ Map structure is valid")
    return True

def validate_flags_format(map_path):
    """Validate flags.json format."""
    try:
        with open(Path(map_path) / 'flags.json', 'r') as f:
            flags = json.load(f)
        
        if not isinstance(flags, list):
            print("❌ flags.json must be a list")
            return False
        
        for i, flag in enumerate(flags):
            if not isinstance(flag, dict):
                print(f"❌ Flag {i} must be an object")
                return False
            if 'task' not in flag or 'answer' not in flag:
                print(f"❌ Flag {i} missing 'task' or 'answer'")
                return False
        
        print(f"✅ Found {len(flags)} valid flags")
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in flags.json")
        return False
    except FileNotFoundError:
        print("❌ flags.json not found")
        return False

def test_server_startup(map_path):
    """Test that the server starts successfully."""
    print("🧪 Testing server startup...")
    
    server_path = Path(map_path) / 'frontend' / 'server.py'
    try:
        # Start server in background
        process = subprocess.Popen(
            [sys.executable, str(server_path)],
            cwd=str(Path(map_path) / 'frontend'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server responds
        try:
            response = requests.get('http://localhost:8000', timeout=5)
            if response.status_code == 200:
                print("✅ Server starts and responds correctly")
                result = True
            else:
                print(f"❌ Server responds with status {response.status_code}")
                result = False
        except requests.exceptions.RequestException as e:
            print(f"❌ Server not responding: {e}")
            result = False
        
        # Clean up
        process.terminate()
        process.wait(timeout=5)
        
        return result
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_map.py <map_directory>")
        sys.exit(1)
    
    map_path = sys.argv[1]
    
    if not os.path.isdir(map_path):
        print(f"❌ Directory {map_path} does not exist")
        sys.exit(1)
    
    print(f"Validating map: {map_path}")
    print("=" * 40)
    
    all_valid = True
    all_valid &= validate_map_structure(map_path)
    all_valid &= validate_flags_format(map_path)
    all_valid &= test_server_startup(map_path)
    
    print("=" * 40)
    if all_valid:
        print("🎉 Map validation successful!")
    else:
        print("❌ Map validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 