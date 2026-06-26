import time
import subprocess
import sys

# Interval in seconds (e.g., 3600 for every hour)
INTERVAL = 3600 

print("🛡️ Watchdog active. Monitoring for mission cycles...")

def trigger_mission():
    try:
        print(f"🔄 Triggering system cycle: {time.ctime()}")
        subprocess.run([sys.executable, "run_mission.py"], check=True)
    except Exception as e:
        print(f"❌ Mission failed: {e}")

if __name__ == "__main__":
    while True:
        trigger_mission()
        print(f"💤 Sleeping for {INTERVAL/60} minutes...")
        time.sleep(INTERVAL)
