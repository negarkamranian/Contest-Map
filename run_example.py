#!/usr/bin/env python3
"""
Simple script to run the example map test.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the example map test."""
    example_path = Path(__file__).parent / "example_map"
    
    if not example_path.exists():
        print("❌ Example map directory not found!")
        return 1
    
    print("🚀 Running Divar CTF example map test...")
    print("📁 Changing to example_map directory...")
    
    try:
        result = subprocess.run(
            [sys.executable, "test_setup.py"],
            cwd=example_path,
            check=False
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 