# main.py - Integrated application script
import os
import argparse
import subprocess
import time
import webbrowser
import threading
from pathlib import Path
import requests
import sys # Import sys module

def check_server_ready(url, retries=10, delay=2):
    """Check if a server is ready by sending requests to the given URL."""
    print(f"Checking if server is ready at {url}...")
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            # Allow common success codes or redirects if applicable
            if response.status_code in [200, 204, 301, 302, 307, 308]:
                print(f"Server at {url} responded with status {response.status_code}. Ready!")
                return True
            else:
                 print(f"Attempt {attempt+1}/{retries}: Server at {url} responded with status {response.status_code}.")

        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if attempt < retries - 1:  # Don't print "retrying" on the last attempt
                print(f"Attempt {attempt+1}/{retries} failed ({error_type}). Retrying in {delay} seconds...")
            else:
                print(f"Final attempt {retries}/{retries} failed ({error_type}).")
        time.sleep(delay)
    print(f"Server at {url} did not become ready after {retries} attempts.")
    return False

def main():
    """Main function to run the complete application"""
    parser = argparse.ArgumentParser(description="Staff Feedback Analysis Tool")
    # Keep existing arguments if needed, e.g., --sample, --timeout
    parser.add_argument("--api-only", action="store_true", help="Start only the API server, not the dashboard")
    parser.add_argument("--dashboard-only", action="store_true", help="Start only the dashboard, not the API server")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds for server startup checks")

    args = parser.parse_args()

    # Create temp directory if it doesn't exist
    # Use Path for better cross-platform compatibility
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    api_process = None
    dashboard_process = None
    api_ready = False
    dashboard_ready = False

    # Store process outputs
    api_stdout_log = temp_dir / "api_stdout.log"
    api_stderr_log = temp_dir / "api_stderr.log"
    dashboard_stdout_log = temp_dir / "dashboard_stdout.log"
    dashboard_stderr_log = temp_dir / "dashboard_stderr.log"

    try:
        # Start API server if needed
        if not args.dashboard_only:
            print("Starting API server...")
            try:
                # Use sys.executable to ensure the correct python interpreter is used
                # Capture stdout and stderr to files for debugging
                with open(api_stdout_log, 'wb') as api_out, open(api_stderr_log, 'wb') as api_err:
                    api_process = subprocess.Popen(
                        [sys.executable, "-m", "uvicorn", "api:app", "--reload", "--port", "8000"],
                        stdout=api_out, stderr=api_err
                    )
                print(f"API server process started (PID: {api_process.pid}). Checking readiness...")
                # Increase retries and delay slightly to allow for slower model loading
                api_ready = check_server_ready("http://localhost:8000", retries=(args.timeout//2)+5, delay=3) # Increased retries by 5, delay to 3s
                if api_ready:
                    print("API server running at http://localhost:8000")
                else:
                    print("Error: API server failed to start within timeout period.")
                    print(f"Check logs for details: {api_stdout_log}, {api_stderr_log}")
                    # Read last few lines of stderr if possible
                    try:
                        with open(api_stderr_log, 'r') as f_err:
                            lines = f_err.readlines()
                            print("Last few lines of API stderr:")
                            for line in lines[-10:]: print(f"  {line.strip()}")
                    except Exception as log_err:
                        print(f"  (Could not read stderr log: {log_err})")

                    if not args.api_only:  # Only exit if we're not in API-only mode
                        return # Exit if API failed and we need it for the dashboard
            except Exception as e:
                print(f"Error starting API server process: {str(e)}")
                return

        # Start dashboard if needed
        if not args.api_only:
            # Ensure API is ready if dashboard needs it (unless dashboard_only is specified)
            if not args.dashboard_only and not api_ready:
                 print("Skipping dashboard start because API server failed to start.")
                 return

            print("Starting Streamlit dashboard...")
            try:
                # Use sys.executable and capture output
                with open(dashboard_stdout_log, 'wb') as dash_out, open(dashboard_stderr_log, 'wb') as dash_err:
                    dashboard_process = subprocess.Popen(
                        [sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", "8501"],
                         stdout=dash_out, stderr=dash_err
                    )
                print(f"Dashboard process started (PID: {dashboard_process.pid}). Checking readiness...")
                # Check Streamlit readiness (might need adjustment based on Streamlit's behavior)
                # Streamlit doesn't have a simple health check endpoint like FastAPI's root.
                # We'll rely on a longer delay and check_server_ready, but it might not be perfect.
                time.sleep(5) # Give Streamlit some time to initialize
                dashboard_ready = check_server_ready("http://localhost:8501", retries=args.timeout//2, delay=3)

                if dashboard_ready:
                    print("Dashboard running at http://localhost:8501")
                    time.sleep(2)  # Small delay before opening browser
                    webbrowser.open("http://localhost:8501")
                else:
                    print("Error: Dashboard failed to start or respond within timeout period.")
                    print(f"Check logs for details: {dashboard_stdout_log}, {dashboard_stderr_log}")
                    # Read last few lines of stderr if possible
                    try:
                        with open(dashboard_stderr_log, 'r') as f_err:
                            lines = f_err.readlines()
                            print("Last few lines of Dashboard stderr:")
                            for line in lines[-10:]: print(f"  {line.strip()}")
                    except Exception as log_err:
                        print(f"  (Could not read stderr log: {log_err})")

            except Exception as e:
                print(f"Error starting dashboard process: {str(e)}")

        # Keep the main thread alive until interrupted if servers are running
        # Check if at least one process was intended to start and potentially succeeded
        if (not args.dashboard_only and api_process) or (not args.api_only and dashboard_process):
             print("\nServers are running. Press Ctrl+C to shut down...")
             while True:
                 # Check if processes are still alive (optional)
                 api_alive = api_process and api_process.poll() is None
                 dashboard_alive = dashboard_process and dashboard_process.poll() is None

                 if not args.dashboard_only and not api_alive:
                     print("API process terminated unexpectedly.")
                     break
                 if not args.api_only and not dashboard_alive:
                     print("Dashboard process terminated unexpectedly.")
                     break
                 if (args.dashboard_only or not api_alive) and (args.api_only or not dashboard_alive):
                     # Both intended processes have stopped (or weren't started)
                     break

                 time.sleep(1)
        else:
             print("No servers were started successfully or none were requested.")


    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nUnexpected error in main loop: {str(e)}")
    finally:
        # Cleanup processes
        if api_process and api_process.poll() is None: # Check if process is running
            print("Terminating API server...")
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("API server did not terminate gracefully, killing...")
                api_process.kill()

        if dashboard_process and dashboard_process.poll() is None: # Check if process is running
            print("Terminating dashboard...")
            dashboard_process.terminate()
            try:
                dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Dashboard did not terminate gracefully, killing...")
                dashboard_process.kill()

        print("Shutdown complete.")

if __name__ == "__main__":
    main()