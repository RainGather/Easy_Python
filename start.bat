@echo off

echo ϵͳ������...
cd %~dp0\tutorial
C:\git\bin\git.exe stash
C:\git\bin\git.exe pull origin master
echo ϵͳ������...
C:\python3\Scripts\jupyter-lab
