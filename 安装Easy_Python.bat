@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd %~dp0

if exist C:\python3\python.exe (
    goto PIP
)

for /r %%f in (python-3*.exe) do (
    call set file="%%f"
    @echo on
    @echo 找到Python3安装文件： %%f
    @echo off
)

if [%file%]==[] (
    echo 未找到Python3安装文件，将在你按下【任意键】后，将会自动尝试用浏览器下载Python3安装文件。
    echo 等Python3安装文件下载完成后，将其放到与 安装Easy_Python.bat 文件同目录下，并重新运行本程序。
    pause
    start https://npm.taobao.org/mirrors/python/3.6.6/python-3.6.6.exe
    exit
)

echo 安装Python3(%file%)中，可能需要15分钟，请稍后...
%file% /quiet InstallAllUsers=1 PrependPath=1 Shortcuts=1 Include_pip=1 TargetDir=C:\python3
echo Python3安装成功。

:PIP
echo 安装依赖模块中，请稍后...
C:\python3\scripts\pip install jupyter wget gitpython requests jupyterlab -i https://pypi.douban.com/simple
mkdir install
cd install
if exist install.py (
    del install.py
)
C:\python3\python.exe -m wget "http://static.hzasteam.org/Easy_Python_Client/install.py" -o install.py
if not exist install.py (
    C:\python3\python.exe -m wget "https://raw.githubusercontent.com/RainGather/Easy_Python/master/install.py" -o install.py
)
C:\python3\python.exe install.py

echo 已完成全部安装过程，其中可能会因为网络等原因导致失败，如果还无法正常使用本项目，请重新运行本程序安装，按【任意键】退出。
pause
