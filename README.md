# Spaceflight-simulator-Multiplayer-Android
Spaceflight-simulator游戏的安卓多人联机方案 未测试  
~~理论上这并不是真正定义上的联机 改成回合制游戏里~~
## 依赖  
pkg install python  
pip install mega  
注意要注册mega云盘  
填写main.py 有注释标注  
## 工作原理  
通过云盘来达到联机效果 ~~应该可以吧~~   
原仓库https://github.com/L4z4r1/Spaceflight-simulator-Multiplayer  
## 如何使用  
1.安装Termux  
链接https://f-droid.org/packages/com.termux/  
2.依次输入运行  
pkg update -y  
pkg install -y python pip  
python --version 〈验证安装〉  
pip install mega.py  
python -c "import mega; print('OK')" 〈验证安装〉  
pkg install -y git  
git clone https://github.com/aaaa111ssf/Spaceflight-simulator-Multiplayer-Android.git  
cd Spaceflight-simulator-Multiplayer-Android  
termux-setup-storage  〈请求存储权限〉  
ls /sdcard/Android/media/com.StefMorojna.SpaceflightSimulator/Saving/Worlds/〈查看路径对不对〉  
nano sfs_termux.py〈修改路径 找到DEFAULT_WORLD_PATH = "/storage/emulated/0/Android/media/com.StefMorojna.SpaceflightSimulator/Saving/Worlds/"
这一行 在media就不用改 在data改成data ctrl+0保存 ctrl+X退出编辑〉  
python sfs_termux.py  〈运行脚本〉  
填你的mega云盘以及密码  
然后会有页面 1上传2下载3同步4设置5退出  
#### 示例  
玩家1玩完之后 退出世界返回主页面 运行脚本 按1上传  
玩家2按2下载 3同步 即可游玩  
注意！必须登录同一mega账号  
### 规划
apk以及更方便的使用  
