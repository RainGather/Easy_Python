@echo off

echo ϵͳ������...
cd %~dp0\tutorial
git stash 2>NUL || C:\git\bin\git.exe stash
git pull origin master 2>NUL || C:\git\bin\git.exe pull origin master
git stash pop 2>NUL || C:\git\bin\git.exe stash pop
git stash clear 2>NUL || C:\git\bin\git.exe stash clear
python start.py
echo ϵͳ������...
jupyter-notebook
