set WshShell=WScript.CreateObject("WScript.Shell")
strDesktop=WshShell.SpecialFolders("Desktop")
set oShellLink=WshShell.CreateShortcut(strDesktop & "\EasyPython�̳�.lnk")
set ProjectDir=createobject("Scripting.FileSystemObject").GetFolder(".")
oShellLink.TargetPath=ProjectDir & "\\start.bat"
oShellLink.WindowStyle=1
oShellLink.Hotkey=""
oShellLink.IconLocation=ProjectDir & "\\logo.ico"
oShellLink.Description="��Jupyter��ѧϰPython"
oShellLink.WorkingDirectory=strDesktop
oShellLink.Save