from datetime import datetime, time as dt_time

def get_time_based_message(config):
    """Get message based on time of day"""
    now = datetime.now().time()
    messages = config.get("messages", {})
    
    if dt_time(6, 0) <= now < dt_time(12, 0):
        base_message = messages.get("morning", "Time to start your day!")
    elif dt_time(12, 0) <= now < dt_time(18, 0):
        base_message = messages.get("afternoon", "Time to stretch or drink water!")
    elif dt_time(18, 0) <= now < dt_time(23, 59):
        base_message = messages.get("evening", "Have you committed your work today?")
    else:
        base_message = messages.get("default", "Time to take a break!")
    
    urgency = config.get("general", {}).get("urgency", "normal")
    if urgency != "normal":
        base_message = f"[{urgency.upper()}] {base_message}"
    
    return base_message

def get_developer_reminder(config):
    """Get developer-specific reminders"""
    now = datetime.now()
    reminders = []
    developer_config = config.get("developer", {})
    
    # Git reminders
    if developer_config.get("git_reminders", False):
        reminders.append(developer_config.get("git_message", "Time to commit your changes!"))
    
    # Other developer reminders
    if developer_config.get("doc_reminders", False) and now.hour % 4 == 0:
        reminders.append("📝 Document your recent changes?")
    if developer_config.get("test_reminders", False) and now.hour % 6 == 0:
        reminders.append("🧪 Write some tests!")
    if developer_config.get("review_reminders", False) and now.hour % 3 == 0:
        reminders.append("👀 Review recent PRs/code")
    
    return "\n".join(reminders) if reminders else None
