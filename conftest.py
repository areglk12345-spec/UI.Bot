import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def pytest_sessionfinish(session, exitstatus):
    """
    Hook called after whole test run finished.
    Sends a summary to LINE Messaging API.
    """
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    
    # Check if reporter exists (it might not in some distributed/custom runs)
    if not reporter:
        return
        
    passed = len(reporter.stats.get("passed", []))
    failed = len(reporter.stats.get("failed", []))
    errors = len(reporter.stats.get("error", []))
    skipped = len(reporter.stats.get("skipped", []))
    
    total = passed + failed + errors + skipped
    
    # Don't send empty reports
    if total == 0:
        return
        
    # Check if it is the midnight (Thailand) run. Midnight TH = 17:00 UTC
    from datetime import datetime, timezone
    now_utc = datetime.now(timezone.utc)
    is_midnight_th = now_utc.hour == 17
    
    # Check if this run was triggered by a schedule (cron)
    is_schedule = os.getenv("GITHUB_EVENT_NAME") == "schedule"
    
    # If it is NOT the midnight run, AND it's an automated schedule run, and tests passed -> skip sending
    if is_schedule and not is_midnight_th and failed == 0 and errors == 0:
        print("\n[LINE Notification] Hourly check passed. Skipping LINE message.")
        return
        
    status_icon = "✅" if failed == 0 and errors == 0 else "❌"
    platform = os.getenv("TEST_PLATFORM", "Desktop 💻")
    
    message = (
        f"{status_icon} สรุปผลการทดสอบ UI Bot ({platform})\n\n"
        f"จำนวนทั้งหมด: {total} เคส\n"
        f"✅ ผ่าน (Passed): {passed}\n"
        f"❌ ไม่ผ่าน (Failed): {failed}\n"
        f"⚠️ ขัดข้อง (Error): {errors}\n"
        f"⏭️ ข้าม (Skipped): {skipped}"
    )
    
    # Add Dashboard link
    if os.getenv("GITHUB_ACTIONS") == "true":
        repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
        repo_name = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]
        pages_url = f"https://{repo_owner}.github.io/{repo_name}/index.html"
    else:
        pages_url = "https://areglk12345-spec.github.io/UI.Bot/index.html (อัปเดตล่าสุดบน GitHub)"
        
    message += f"\n\n📊 ดู Dashboard แบบเต็มได้ที่:\n{pages_url}"
    
    send_line_message(message)

def send_line_message(text: str):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    
    if not token or not user_id:
        print("\n[LINE Notification] Skipping: LINE_CHANNEL_ACCESS_TOKEN or LINE_USER_ID not found in .env.")
        return
        
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            print("\n[LINE Notification] Successfully sent message to LINE!")
        else:
            print(f"\n[LINE Notification] Failed to send: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"\n[LINE Notification] Error during request: {str(e)}")
