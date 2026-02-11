"""
Flask web server for Frontier Tech News Aggregator
Serves the dashboard and runs the aggregator on a schedule
"""
import os
import threading
import time
from flask import Flask, send_from_directory, jsonify, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Directory where the dashboard HTML lives
DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "docs")
os.makedirs(DASHBOARD_DIR, exist_ok=True)


@app.route("/")
def index():
    """Serve the dashboard"""
    dashboard_path = os.path.join(DASHBOARD_DIR, "index.html")
    if os.path.exists(dashboard_path):
        return send_from_directory(DASHBOARD_DIR, "index.html")
    return """
    <html>
    <head><title>Frontier Tech Dashboard</title></head>
    <body style="font-family: sans-serif; background: #1a1a2e; color: #e4e4e4;
                 display: flex; align-items: center; justify-content: center; height: 100vh;">
        <div style="text-align: center;">
            <h1>Frontier Tech Dashboard</h1>
            <p>Dashboard is being generated. Check back shortly.</p>
            <p><a href="/run" style="color: #e94560;">Trigger aggregation now</a></p>
        </div>
    </body>
    </html>
    """, 200


@app.route("/health")
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "ok"}), 200


@app.route("/run")
def trigger_run():
    """Manually trigger the aggregator (useful for testing)"""
    try:
        from main import run_aggregator
        # Run in background thread so request doesn't timeout
        thread = threading.Thread(
            target=run_aggregator,
            kwargs={
                "dry_run": False,
                "push_sheets": bool(os.getenv("SPREADSHEET_ID")),
                "send_email": bool(os.getenv("EMAIL_SENDER")),
                "include_twitter": bool(os.getenv("TWITTER_BEARER_TOKEN")),
                "build_dashboard": True,
            },
        )
        thread.start()
        return jsonify({"status": "started", "message": "Aggregation triggered"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def scheduled_run():
    """Background thread that runs the aggregator on a schedule"""
    from main import run_aggregator

    interval_hours = int(os.getenv("RUN_INTERVAL_HOURS", "6"))
    print(f"[Scheduler] Will run every {interval_hours} hours")

    while True:
        try:
            print("[Scheduler] Running aggregator...")
            run_aggregator(
                dry_run=False,
                push_sheets=bool(os.getenv("SPREADSHEET_ID")),
                send_email=bool(os.getenv("EMAIL_SENDER")),
                include_twitter=bool(os.getenv("TWITTER_BEARER_TOKEN")),
                build_dashboard=True,
            )
            print("[Scheduler] Done. Sleeping...")
        except Exception as e:
            print(f"[Scheduler] Error: {e}")

        time.sleep(interval_hours * 3600)


# Start the scheduler in a background thread when the app starts
if os.getenv("ENABLE_SCHEDULER", "true").lower() == "true":
    scheduler_thread = threading.Thread(target=scheduled_run, daemon=True)
    scheduler_thread.start()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
