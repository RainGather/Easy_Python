@echo off

echo �����У����Եȡ�ѧϰ�̳�ʱ����رմ˴��ڡ�
cd %~dp0\tutorial
C:\git\bin\git.exe stash
C:\git\bin\git.exe pull origin master
C:\python3\Scripts\jupyter-lab
