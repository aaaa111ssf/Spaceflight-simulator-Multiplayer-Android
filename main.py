import flet as ft
import threading
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from network import MegaNetwork
    from config import Config
except:
    MegaNetwork = None
    Config = None

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


class SFSMultiplayerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "SFS Multiplayer"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        
        self.config = Config() if Config else None
        self.network = None
        
        if self.config and self.config.email and self.config.password and MegaNetwork:
            try:
                self.network = MegaNetwork(self.config.email, self.config.password)
            except:
                self.network = None
        
        self.status_lines = []
        self.status_text = ft.Text(
            value="$ Ready", 
            size=12,
            selectable=True
        )
        self.status_container = ft.Container(
            content=self.status_text,
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            width=None,
            expand=True
        )
        
        self.world_path_field = ft.TextField(
            label="World Path 存档路径",
            value=self.config.world_path if self.config else DEFAULT_WORLD_PATH,
            hint_text="SFS Worlds folder path",
            expand=True
        )
        self.email_field = ft.TextField(
            label="MEGA Email 邮箱",
            value=self.config.email if self.config else "",
            hint_text="your@email.com",
            width=350
        )
        self.password_field = ft.TextField(
            label="MEGA Password 密码",
            value=self.config.password if self.config else "",
            hint_text="your password",
            password=True,
            can_reveal_password=True,
            width=350
        )
        self.progress = ft.ProgressBar(visible=False, width=300)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ft.Container(
            content=ft.Text(
                "🚀 SFS Multiplayer",
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.symmetric(vertical=20),
            alignment=ft.alignment.center
        )
        
        # Status display
        status_label = ft.Text("Status 状态:", size=14, weight=ft.FontWeight.BOLD)
        
        status_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [status_label, self.status_container],
                    scroll=ft.ScrollMode.AUTO,
                    height=200
                ),
                padding=10
            ),
            margin=ft.margin.only(bottom=15)
        )
        
        # Config section
        config_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("MEGA Account 账号设置", size=16, weight=ft.FontWeight.BOLD),
                    self.email_field,
                    self.password_field,
                    ft.Row([
                        ft.ElevatedButton(
                            "Save 保存账号",
                            on_click=self.save_credentials,
                            icon=ft.icons.SAVE,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.BLUE_700,
                                color=ft.colors.WHITE
                            )
                        )
                    ], spacing=10)
                ], spacing=10),
                padding=15
            ),
            margin=ft.margin.only(bottom=15)
        )
        
        # World path section
        path_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("World Path 存档路径", size=16, weight=ft.FontWeight.BOLD),
                    self.world_path_field,
                    ft.ElevatedButton(
                        "Save Path 保存路径",
                        on_click=self.save_path,
                        icon=ft.icons.FOLDER_OPEN,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.PURPLE_700,
                            color=ft.colors.WHITE
                        )
                    )
                ], spacing=10),
                padding=15
            ),
            margin=ft.margin.only(bottom=15)
        )
        
        # Action buttons
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "Upload 上传",
                on_click=self.upload_files,
                icon=ft.icons.UPLOAD,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREEN_700,
                    color=ft.colors.WHITE
                ),
                height=50,
                expand=True
            ),
            ft.ElevatedButton(
                "Download 下载",
                on_click=self.download_files,
                icon=ft.icons.DOWNLOAD,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE
                ),
                height=50,
                expand=True
            ),
            ft.ElevatedButton(
                "Sync 同步",
                on_click=self.sync_files,
                icon=ft.icons.SYNC,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.ORANGE_700,
                    color=ft.colors.WHITE
                ),
                height=50,
                expand=True
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        
        # Progress bar
        self.progress_row = ft.Row([self.progress], alignment=ft.MainAxisAlignment.CENTER, visible=False)
        
        # Info text
        info_text = ft.Container(
            content=ft.Text(
                "上传会覆盖云端 | 下载会覆盖本地 | 同步=先下载再上传\n"
                "Upload overwrites cloud | Download overwrites local | Sync = download + upload",
                size=11,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.GREY_500
            ),
            padding=15
        )
        
        # Assemble page
        self.page.add(
            header,
            status_card,
            config_card,
            path_card,
            action_buttons,
            self.progress_row,
            info_text
        )
        
    def log(self, message: str):
        """Add message to status log"""
        self.status_lines.append(message)
        if len(self.status_lines) > 100:
            self.status_lines = self.status_lines[-100:]
        self.status_text.value = "\n".join(self.status_lines)
        self.page.update()
        
    def set_progress(self, visible: bool, value: float = 0):
        """Show/hide progress bar"""
        self.progress.visible = visible
        self.progress_row.visible = visible
        if visible:
            self.progress.value = value
        self.page.update()
        
    def save_credentials(self, e):
        """Save MEGA credentials"""
        if not self.config:
            self.log("[X] Config system not available")
            return
            
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        
        if not email or not password:
            self.log("[!] Please enter both email and password 请输入邮箱和密码")
            return
            
        self.config.email = email
        self.config.password = password
        self.config.save()
        
        # Update network with new credentials
        if MegaNetwork:
            try:
                self.network = MegaNetwork(email, password)
                self.log("[+] Credentials saved & logged in 账号已保存并登录")
            except Exception as ex:
                self.log(f"[X] Login failed 登录失败: {ex}")
        else:
            self.log("[+] Credentials saved 账号已保存")
        
    def save_path(self, e):
        """Save world path"""
        if not self.config:
            self.log("[X] Config system not available")
            return
            
        path = self.world_path_field.value.strip()
        
        if not path:
            self.log("[!] Please enter a valid path 请输入有效路径")
            return
            
        self.config.world_path = path
        self.config.save()
        self.log(f"[+] Path saved 路径已保存: {path}")
        
    def upload_files(self, e):
        """Upload local files to MEGA"""
        if not self.validate_config():
            return
            
        def do_upload():
            try:
                self.log("[+] Starting upload 开始上传...")
                self.set_progress(True, 0)
                
                world_path = self.config.world_path
                if not os.path.exists(world_path):
                    self.log(f"[X] Path not found 路径不存在: {world_path}")
                    self.set_progress(False)
                    return
                    
                # Delete existing files first
                self.log("[+] Cleaning cloud storage 清理云端...")
                self.network.delete_all(SYNC_FILES)
                
                # Upload each file
                files = os.listdir(world_path)
                file_list = [f for f in files if os.path.isfile(os.path.join(world_path, f))]
                total = len(file_list)
                success_count = 0
                
                for i, filename in enumerate(file_list):
                    filepath = os.path.join(world_path, filename)
                    if os.path.isfile(filepath):
                        self.log(f"[+] Uploading 上传中 {filename}...")
                        try:
                            self.network.upload_file(filepath)
                            success_count += 1
                        except Exception as e:
                            self.log(f"[!] Failed to upload 上传失败 {filename}: {e}")
                        self.set_progress(True, (i + 1) / total)
                        
                self.log(f"[+] Upload complete! 上传完成 ({success_count}/{total} files)")
            except Exception as ex:
                self.log(f"[X] Upload failed 上传失败: {ex}")
            finally:
                self.set_progress(False)
                
        threading.Thread(target=do_upload, daemon=True).start()
        
    def download_files(self, e):
        """Download files from MEGA"""
        if not self.validate_config():
            return
            
        def do_download():
            try:
                self.log("[+] Starting download 开始下载...")
                self.set_progress(True, 0)
                
                world_path = self.config.world_path
                os.makedirs(world_path, exist_ok=True)
                
                total = len(SYNC_FILES)
                success_count = 0
                
                for i, filename in enumerate(SYNC_FILES):
                    self.log(f"[+] Downloading 下载中 {filename}...")
                    try:
                        self.network.download_file(filename, world_path)
                        success_count += 1
                    except Exception as e:
                        self.log(f"[!] Failed to download 下载失败 {filename}: {e}")
                    self.set_progress(True, (i + 1) / total)
                    
                self.log(f"[+] Download complete! 下载完成 ({success_count}/{total} files)")
            except Exception as ex:
                self.log(f"[X] Download failed 下载失败: {ex}")
            finally:
                self.set_progress(False)
                
        threading.Thread(target=do_download, daemon=True).start()
        
    def sync_files(self, e):
        """Sync files (download then upload)"""
        if not self.validate_config():
            return
            
        def do_sync():
            try:
                self.log("[+] Starting sync 开始同步 (Download + Upload)...")
                self.set_progress(True, 0.1)
                
                world_path = self.config.world_path
                os.makedirs(world_path, exist_ok=True)
                
                # First download
                self.log("[+] Step 1/2: Downloading 下载中...")
                for filename in SYNC_FILES:
                    try:
                        self.network.download_file(filename, world_path)
                    except:
                        pass
                self.set_progress(True, 0.5)
                        
                # Then upload
                self.log("[+] Step 2/2: Uploading 上传中...")
                self.network.delete_all(SYNC_FILES)
                
                files = os.listdir(world_path)
                for filename in files:
                    filepath = os.path.join(world_path, filename)
                    if os.path.isfile(filepath):
                        try:
                            self.network.upload_file(filepath)
                        except:
                            pass
                
                self.set_progress(True, 1.0)
                self.log("[+] Sync complete! 同步完成!")
            except Exception as ex:
                self.log(f"[X] Sync failed 同步失败: {ex}")
            finally:
                self.set_progress(False)
                
        threading.Thread(target=do_sync, daemon=True).start()
        
    def validate_config(self) -> bool:
        """Validate configuration before operations"""
        if not self.config:
            self.log("[X] Config system not available")
            return False
        if not MegaNetwork:
            self.log("[X] Network module not available")
            return False
        if not self.config.email or not self.config.password:
            self.log("[!] Please set MEGA credentials first 请先设置MEGA账号")
            return False
        if not self.config.world_path:
            self.log("[!] Please set world path first 请先设置存档路径")
            return False
        if not self.network:
            try:
                self.network = MegaNetwork(self.config.email, self.config.password)
            except Exception as ex:
                self.log(f"[X] Failed to connect to MEGA 无法连接到MEGA: {ex}")
                return False
        return True


def main(page: ft.Page):
    SFSMultiplayerApp(page)


if __name__ == "__main__":
    ft.app(target=main)
