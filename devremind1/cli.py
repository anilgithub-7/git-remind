import time
import argparse
from datetime import datetime

from .config import load_config
from .reminders import get_time_based_message, get_developer_reminder
from .notifications import send_notification, play_sound

def log_reminder(message, config):
    """Log reminders with timestamp"""
    log_file = config.get("general", {}).get("log_file", "reminder_log.txt")
    try:
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()} - {message}\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def remind_every(config=None, **kwargs):
    """
    Main reminder function that accepts both config object and direct arguments
    """
    if config is None:
        config = load_config()

    # Override config with direct arguments if provided
    for key, value in kwargs.items():
        if value is not None:
            if key in ["frequency", "urgency"]:
                config["general"][key] = value
            elif key in ["git_reminders", "doc_reminders", "test_reminders", "review_reminders"]:
                config["developer"][key] = value
            elif key == "sound":
                config["sound"]["custom_sound"] = value
            elif key == "no_sound":
                config["sound"]["enabled"] = not value

    general_config = config.get("general", {})
    developer_config = config.get("developer", {})

    print("🚀 Developer Reminder Started!")
    print(f"🔔 General reminders every {general_config.get('frequency', 60)} minutes")
    if developer_config.get("git_reminders"):
        print(f"💾 Git reminders every {developer_config.get('git_interval', 1)} minutes")
    print("⏹ Press Ctrl+C to stop\n")

    last_git_reminder = time.time()

    try:
        while True:
            current_time = time.time()

            # Git reminders
            if (developer_config.get("git_reminders") and
                current_time - last_git_reminder >= developer_config.get("git_interval", 1) * 60):
                git_msg = developer_config.get("git_message", "Time to commit your changes!")
                send_notification("💾 Git Commit Reminder", git_msg, timeout=5)
                print(f"{datetime.now().strftime('%H:%M')} - {git_msg}")
                play_sound(config, "git")
                log_reminder(f"Git Reminder: {git_msg}", config)
                last_git_reminder = current_time

            # General reminders
            if int(current_time) % (general_config.get("frequency", 60) * 60) == 0:
                message = get_time_based_message(config)
                dev_msg = get_developer_reminder(config)
                full_msg = f"{message}\n\n{dev_msg}" if dev_msg else message

                send_notification("🧠 Developer Reminder", full_msg, timeout=10)
                print(f"⏰ {datetime.now().strftime('%H:%M')} - {message}")
                play_sound(config)
                log_reminder(full_msg, config)

            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        print("\n✅ Reminder stopped by user")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Developer Reminder Tool')
    parser.add_argument('--config', type=str, default=None,
                      help='Path to custom config file')
    parser.add_argument('--frequency', type=int, default=None,
                      help='Reminder frequency in minutes')
    parser.add_argument('--git-interval', type=int, default=None,
                      help='Git reminder frequency in minutes')
    parser.add_argument('--urgency', choices=['low', 'normal', 'high'], default=None,
                      help='Notification urgency level')
    parser.add_argument('--sound', type=str, default=None,
                      help='Path to custom sound file')
    parser.add_argument('--git-sound', type=str, default=None,
                      help='Path to custom git reminder sound')
    parser.add_argument('--no-sound', action='store_true',
                      help='Disable all sounds')
    parser.add_argument('--git-reminders', action='store_true', default=None,
                      help='Enable git commit reminders')
    parser.add_argument('--no-git-reminders', action='store_false', dest='git_reminders',
                      help='Disable git commit reminders')
    parser.add_argument('--doc-reminders', action='store_true', default=None,
                      help='Enable documentation reminders')
    parser.add_argument('--no-doc-reminders', action='store_false', dest='doc_reminders',
                      help='Disable documentation reminders')
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    # Create a dictionary of arguments to pass to the reminder function
    kwargs = {
        'frequency': args.frequency,
        'urgency': args.urgency,
        'sound': args.sound,
        'no_sound': args.no_sound,
        'git_reminders': args.git_reminders,
        'doc_reminders': args.doc_reminders,
        'git_interval': args.git_interval
    }

    if args.git_sound:
        config["sound"]["git_sound"] = args.git_sound

    remind_every(config, **kwargs)
