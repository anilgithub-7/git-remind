from plyer import notification
from playsound import playsound
import os

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

def play_sound(config, sound_type="default"):
    """Play sound based on type (default/git)"""
    if not config.get("sound", {}).get("enabled", False):
        return

    try:
        sound_file = None
        if sound_type == "git" and config.get("sound", {}).get("git_sound"):
            sound_file = config["sound"]["git_sound"]
        elif config.get("sound", {}).get("custom_sound"):
            sound_file = config["sound"]["custom_sound"]
        
        if sound_file and os.path.exists(sound_file):
            playsound(sound_file)
        else:
            # Fallback to default sound
            default_sound = files('devremind1').joinpath('alarm.mp3')
            playsound(str(default_sound))
    except Exception as e:
        print(f"🔇 Error playing sound: {e}")

def send_notification(title, message, timeout=10):
    """Send a desktop notification."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=timeout
        )
    except Exception as e:
        print(f"Error sending notification: {e}")
