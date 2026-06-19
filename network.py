import os
import sys

try:
    from mega import Mega
except ImportError:
    print("[!] mega.py not installed. Run: pip install mega.py")
    raise


class MegaNetwork:
    """Handle MEGA.nz API operations for SFS Multiplayer"""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.mega = Mega({'verbose': False})
        self._logged_in = False
        
        if not email or not password:
            raise Exception("Email and password are required")
            
        self._login()
        
    def _login(self):
        """Login to MEGA account"""
        try:
            self.mega.login(self.email, self.password)
            self._logged_in = True
        except Exception as e:
            self._logged_in = False
            raise Exception(f"MEGA login failed: {e}")
            
    def upload_file(self, filepath: str) -> bool:
        """Upload a single file to MEGA"""
        try:
            if not os.path.exists(filepath):
                raise Exception(f"File not found: {filepath}")
                
            filename = os.path.basename(filepath)
            self.mega.upload(filepath)
            return True
        except Exception as e:
            raise Exception(f"Upload failed: {e}")
            
    def download_file(self, filename: str, destination: str) -> bool:
        """Download a file from MEGA to destination folder"""
        try:
            file = self.mega.find(filename)
            if file:
                self.mega.download(file[0], destination)
                return True
            else:
                raise Exception(f"File not found on MEGA: {filename}")
        except Exception as e:
            raise Exception(f"Download failed: {e}")
            
    def delete_file(self, filename: str) -> bool:
        """Delete a file from MEGA"""
        try:
            file = self.mega.find(filename)
            if file:
                self.mega.delete(file[0])
                return True
            return False
        except Exception as e:
            # Don't raise - file might not exist, which is fine
            return False
            
    def delete_all(self, filenames: list) -> bool:
        """Delete multiple files from MEGA"""
        success = True
        for filename in filenames:
            try:
                self.delete_file(filename)
            except:
                pass
        return success
