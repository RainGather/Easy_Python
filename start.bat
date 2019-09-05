@echo off

echo 系统更新中...
cd %~dp0\tutorial
C:\git\bin\git.exe stash
C:\git\bin\git.exe pull origin master
echo 系统启动中...
C:\python3\Scripts\jupyter-lab
