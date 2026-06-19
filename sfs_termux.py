#!/usr/bin/env python3
"""
SFS Multiplayer - Terminal Version (for Termux)
This version runs without GUI, perfect for Termux on Android.
"""

import os
import sys
import json
from mega import Mega

# Default world path for Android
DEFAULT_WORLD_PATH = "/storage/emulated/0/Android/media/com.StefMorojna.SpaceflightSimulator/Saving/Worlds/"

# Files to sync
SYNC_FILES = [
    "Achievements.txt",
    "Addresses.txt", 
    "Branches.txt",
    "Rockets.txt",
    "Version.txt",
    "WorldState.txt"
]

# Config file
CONFIG_FILE = ".sfs_multiplayer_config"


def log(msg):
    print(f"[+] {msg}")


def error(msg):
    print(f"[X] {msg}")


def load_config():
    """Load configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'email': '', 'password': '', 'world_path': DEFAULT_WORLD_PATH}


def save_config(config):
    """Save configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def setup():
    """First-time setup"""
    config = load_config()
    
    print("\n=== SFS Multiplayer Setup ===")
    print(f"World Path: {config['world_path']}")
    
    email = input("MEGA Email (press Enter to keep current): ").strip()
    if email:
        config['email'] = email
        
    password = input("MEGA Password (press Enter to keep current): ").strip()
    if password:
        config['password'] = password
        
    world_path = input(f"World Path (press Enter for default): ").strip()
    if world_path:
        config['world_path'] = world_path
        
    save_config(config)
    log("Configuration saved!")
    return config


def connect_mega(email, password):
    """Connect to MEGA"""
    try:
        mega = Mega({'verbose': False})
        mega.login(email, password)
        log("Connected to MEGA")
        return mega
    except Exception as e:
        error(f"Failed to connect: {e}")
        return None


def upload(mega, world_path):
    """Upload files to MEGA"""
    if not os.path.exists(world_path):
        error(f"Path not found: {world_path}")
        return
        
    try:
        log("Cleaning cloud storage...")
        for filename in SYNC_FILES:
            try:
                file = mega.find(filename)
                if file:
                    mega.delete(file[0])
            except:
                pass
                
        log("Uploading files...")
        files = os.listdir(world_path)
        for filename in files:
            filepath = os.path.join(world_path, filename)
            if os.path.isfile(filepath):
                log(f"  Uploading {filename}...")
                mega.upload(filepath)
                
        log("Upload complete!")
    except Exception as e:
        error(f"Upload failed: {e}")


def download(mega, world_path):
    """Download files from MEGA"""
    try:
        os.makedirs(world_path, exist_ok=True)
        
        log("Downloading files...")
        for filename in SYNC_FILES:
            try:
                log(f"  Downloading {filename}...")
                file = mega.find(filename)
                if file:
                    mega.download(file[0], world_path)
                else:
                    print(f"  {filename} not found on MEGA")
            except Exception as e:
                print(f"  Failed to download {filename}: {e}")
                
        log("Download complete!")
    except Exception as e:
        error(f"Download failed: {e}")


def sync(mega, world_path):
    """Sync files (download then upload)"""
    log("Starting sync...")
    download(mega, world_path)
    upload(mega, world_path)
    log("Sync complete!")


def main():
    config = load_config()
    
    # Check if setup is needed
    if not config['email'] or not config['password']:
        config = setup()
        
    while True:
        print("\n=== SFS Multiplayer ===")
        print(f"World Path: {config['world_path']}")
        print("1. Upload (local -> cloud)")
        print("2. Download (cloud -> local)")
        print("3. Sync (download then upload)")
        print("4. Settings")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            mega = connect_mega(config['email'], config['password'])
            if mega:
                upload(mega, config['world_path'])
                
        elif choice == '2':
            mega = connect_mega(config['email'], config['password'])
            if mega:
                download(mega, config['world_path'])
                
        elif choice == '3':
            mega = connect_mega(config['email'], config['password'])
            if mega:
                sync(mega, config['world_path'])
                
        elif choice == '4':
            config = setup()
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            error("Invalid choice")


if __name__ == "__main__":
    main()