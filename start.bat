@echo off

echo ϵͳ������...
cd %~dp0\tutorial
C:\git\bin\git.exe stash
C:\git\bin\git.exe pull origin master
C:\git\bin\git.exe stash pop
C:\git\bin\git.exe stash clear
echo ϵͳ������...
C:\python3\Scripts\jupyter-lab
