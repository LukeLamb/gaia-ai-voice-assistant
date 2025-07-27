import json
import os
from datetime import datetime

class UserMemory:
    def __init__(self, memory_file="user_memory.json"):
        self.memory_file = memory_file
        self.user_data = self._load_memory()

    def _load_memory(self):
        """Load user memory from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_memory(self):
        """Save user memory to file."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user memory: {e}")

    def get_user_name(self):
        """Get the stored user name."""
        return self.user_data.get("name")

    def set_user_name(self, name):
        """Store the user's name."""
        self.user_data["name"] = name
        self.user_data["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_memory()

    def is_user_known(self):
        """Check if we know the user."""
        return "name" in self.user_data and self.user_data["name"]

    def get_last_seen(self):
        """Get when user was last seen."""
        return self.user_data.get("last_seen")

    def update_last_seen(self):
        """Update the last seen timestamp."""
        self.user_data["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_memory()
