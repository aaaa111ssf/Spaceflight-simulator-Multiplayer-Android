import os
import json

# Config file location (in app's local directory)
CONFIG_FILE = "sfs_multiplayer_config.json"

# Default world path for Android
DEFAULT_WORLD_PATH = "/storage/emulated/0/Android/media/com.StefMorojna.SpaceflightSimulator/Saving/Worlds/"


class Config:
    """Simple configuration manager for storing settings"""
    
    def __init__(self):
        self.email = ""
        self.password = ""
        self.world_path = DEFAULT_WORLD_PATH
        self._load()
        
    def _load(self):
        """Load configuration from file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.email = data.get('email', '')
                    self.password = data.get('password', '')
                    self.world_path = data.get('world_path', DEFAULT_WORLD_PATH)
        except Exception as e:
            print(f"[!] Failed to load config: {e}")
            
    def save(self):
        """Save configuration to file"""
        try:
            data = {
                'email': self.email,
                'password': self.password,
                'world_path': self.world_path
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print("[+] Config saved")
        except Exception as e:
            print(f"[X] Failed to save config: {e}")
            
    def __str__(self):
        return f"Config(email={self.email}, world_path={self.world_path})"