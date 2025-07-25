import os
import json

# Default configuration
DEFAULT_CONFIG = {
    "general": {
        "frequency": 60,
        "log_file": "reminder_log.txt",
        "urgency": "normal"
    },
    "messages": {
        "morning": "Time to start your day! Review your tasks.",
        "afternoon": "Time to stretch or drink water!",
        "evening": "Have you committed your work today?",
        "default": "Time to take a break!"
    },
    "developer": {
        "git_reminders": True,
        "git_interval": 1,  # Minutes between git reminders
        "git_message": "⏰ Time to commit your changes!",
        "doc_reminders": True,
        "test_reminders": False,
        "review_reminders": True
    },
    "sound": {
        "enabled": True,
        "custom_sound": None,
        "git_sound": None  # Custom sound for git reminders
    }
}

def load_config(config_path=None):
    """Load configuration from file or use defaults"""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Merge with default config to ensure all keys are present
        for key in DEFAULT_CONFIG:
            if key not in config:
                config[key] = DEFAULT_CONFIG[key]
            elif isinstance(DEFAULT_CONFIG[key], dict):
                # Merge dictionaries to add new default keys if they don't exist
                config[key] = {**DEFAULT_CONFIG[key], **config[key]}
        return config
    return DEFAULT_CONFIG.copy()  # Return a copy to avoid modifying defaults

def save_config(config, config_path):
    """Save configuration to file"""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
