#!/usr/bin/env python3
"""
Test setup script for the Divar CTF example map.
This script helps test both the server and agent components.
"""

import os
import sys
import time
import requests
import subprocess
import signal
from pathlib import Path

def set_api_key():
    """Set the OpenAI API key in the environment."""
    # Check if API key is already set
    if os.environ.get("OPENAI_API_KEY"):
        print("✅ OpenAI API key already set in environment")
        return True
    
    # Try to read from .env file if available
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        if os.environ.get("OPENAI_API_KEY"):
            print("✅ OpenAI API key loaded from .env file")
            return True
    
    print("❌ OpenAI API key not found!")
    print("Please set your API key in one of these ways:")
    print("1. Environment variable: export OPENAI_API_KEY='your-key-here'")
    print("2. Create a .env file with: OPENAI_API_KEY=your-key-here")
    return False

def start_server():
    """Start the FastAPI server."""
    print("🚀 Starting server...")
    frontend_path = Path(__file__).parent / "frontend"
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=frontend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    for _ in range(10):
        try:
            response = requests.get("http://localhost:8000", timeout=1)
            if response.status_code == 200:
                print("✅ Server started successfully on http://localhost:8000")
                return server_process
        except requests.exceptions.RequestException:
            time.sleep(1)
    
    print("❌ Failed to start server")
    server_process.terminate()
    return None

def test_agent():
    """Test the agent."""
    print("🤖 Testing agent...")
    try:
        result = subprocess.run(
            [sys.executable, "agent_example.py"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Agent test completed successfully")
            print("Agent output:")
            print(result.stdout)
        else:
            print("❌ Agent test failed")
            print("Error:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Agent test timed out")
        return False
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def main():
    """Main test function."""
    print("=== Divar CTF Example Map Test ===\n")
    
    # Check API key
    if not set_api_key():
        return 1
    
    # Start server
    server_process = start_server()
    if not server_process:
        return 1
    
    try:
        # Test agent
        success = test_agent()
        
        if success:
            print("\n🎉 All tests passed! The setup is working correctly.")
            print("\nTo run manually:")
            print("1. Start server: cd frontend && python3 server.py")
            print("2. Run agent: python3 agent_example.py")
            return 0
        else:
            print("\n❌ Tests failed. Check the error messages above.")
            return 1
            
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ Server stopped")

if __name__ == "__main__":
    sys.exit(main()) 