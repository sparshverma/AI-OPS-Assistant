import uvicorn
import webbrowser
import threading
import time
import os
import sys

def open_browser():
    """Waits a moment for the server to start, then opens the browser."""
    time.sleep(1.5)
    print("Opening browser at http://localhost:8081...")
    webbrowser.open("http://localhost:8081")

def main():
    print("Starting AI Operations Assistant Web Interface...")
    
    # Check if dependencies are installed (rudimentary check)
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("Error: Missing dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)

    # Launch browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the server
    # We point to "web_interface.app:app" because the file is in web_interface/app.py
    uvicorn.run("web_interface.app:app", host="127.0.0.1", port=8081, reload=True)

if __name__ == "__main__":
    main()
