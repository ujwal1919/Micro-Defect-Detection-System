"""
Quick script to restart the API server
"""
import os
import sys
import subprocess
import signal
import time

def kill_existing_servers():
    """Kill any existing Python processes running app.py"""
    try:
        # Find processes using port 8000 (Windows)
        result = subprocess.run(
            ['netstat', '-ano'], 
            capture_output=True, 
            text=True
        )
        
        # Find Python processes
        python_processes = []
        for line in result.stdout.split('\n'):
            if '8000' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    python_processes.append(pid)
        
        # Kill processes
        for pid in python_processes:
            try:
                subprocess.run(['taskkill', '/F', '/PID', pid], 
                             capture_output=True)
                print(f"Killed process {pid}")
            except:
                pass
    except:
        pass

def start_server():
    """Start the API server"""
    print("=" * 70)
    print("RESTARTING API SERVER")
    print("=" * 70)
    
    # Change to correct directory
    os.chdir(r"C:\Users\Ujwal Gowda KR\OneDrive\Desktop\PCB-main\project\python_backend")
    
    # Kill existing servers
    print("\n[1/2] Stopping existing servers...")
    kill_existing_servers()
    time.sleep(2)
    
    # Start new server
    print("[2/2] Starting new server...")
    print("\nServer starting on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")

if __name__ == "__main__":
    start_server()
