import sys
import os
import threading
import time

# Ensure current directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Product, Invoice, DealerPurchase, SystemSetting

def start_flask_server():
    """Runs the Flask backend server locally on port 5000."""
    print("--- Starting Fabrix Local Backend Server ---")
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def run_desktop_app():
    """Launches the Standalone Desktop Application Window."""
    # 1. Start Flask in background thread
    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()
    
    # Wait for local server to initialize
    time.sleep(1.5)
    
    # 2. Try importing pywebview for Native Window
    try:
        import webview
        print("--- Launching Fabrix Native Desktop Window ---")
        webview.create_window(
            title="FABRIX - Luxury Billing & Stock Management",
            url="http://127.0.0.1:5000",
            width=1280,
            height=850,
            resizable=True,
            min_size=(900, 600)
        )
        webview.start()
    except ImportError:
        # Fallback to webbrowser if pywebview is not yet installed
        import webbrowser
        print("--- pywebview not found. Opening Fabrix in local application window ---")
        webbrowser.open("http://127.0.0.1:5000")
        
        # Keep thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Fabrix Desktop exited.")

if __name__ == '__main__':
    run_desktop_app()
