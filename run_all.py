import subprocess
import time
import sys
import os

def run_servers():
    print("Starting Main Store Application (Port 5000)...")
    # Start app.py
    app_process = subprocess.Popen([sys.executable, 'app.py'], env=os.environ.copy())
    
    print("Starting Admin Panel (Port 5001)...")
    # Start admin.py
    admin_process = subprocess.Popen([sys.executable, 'admin.py'], env=os.environ.copy())
    
    print("\nServers are starting...")
    print("Store: http://127.0.0.1:5000")
    print("Admin: http://127.0.0.1:5001/login")
    print("\nPress Ctrl+C to stop both servers.")
    
    try:
        # Keep the script running to monitor processes
        while True:
            time.sleep(1)
            # Check if processes are still running
            if app_process.poll() is not None:
                print("Main application stopped unexpectedly.")
                break
            if admin_process.poll() is not None:
                print("Admin panel stopped unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping servers...")
    finally:
        # Terminate processes
        if app_process.poll() is None:
            app_process.terminate()
        if admin_process.poll() is None:
            admin_process.terminate()
            
        # Wait for them to exit
        app_process.wait()
        admin_process.wait()
        print("Servers stopped.")

if __name__ == '__main__':
    run_servers()
