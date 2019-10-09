@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
set pro=%~dp0\EasyPython
set lib=%pro%\lib
set install=%pro%\install
set pydir=%pro%\python
set pyexe=%pydir%\python.exe
set pipexe=%pydir%\Scripts\pip.exe
set downloadvbs=%install%\download.vbs
set mklinkvbs=%install%\mklink.vbs
set gitdir=%pro%\git
set gitexe=%gitdir%\bin\git.exe
%pro:0,2%
cd "%~dp0"
mkdir "%pro%"
mkdir "%install%"

(
    echo Sub Download(link, filename)
    echo     Set Post = CreateObject("Msxml2.XMLHTTP")
    echo     Set Shell = CreateObject("Wscript.Shell")
    echo     Post.Open "GET",link,0
    echo     Post.Send()
    echo     Set aGet = CreateObject("ADODB.Stream")
    echo     aGet.Mode = 3
    echo     aGet.Type = 1
    echo     aGet.Open()
    echo     aGet.Write(Post.responseBody)
    echo     aGet.SaveToFile filename,2
    echo     wscript.sleep 1000
    echo End Sub
    echo Download "https://npm.taobao.org/mirrors/python/3.6.6/python-3.6.6.exe" "%install%\pyinstall.exe"
) > "%downloadvbs%"

(
    echo Sub MkDesktopLink(linkname, linkaddr, icon, description)
    echo     set WshShell=WScript.CreateObject("WScript.Shell")
    echo     strDesktop=WshShell.SpecialFolders("Desktop")
    echo     set oShellLink=WshShell.CreateShortcut(strDesktop & "\\" & linkname)
    echo     oShellLink.TargetPath=linkaddr
    echo     oShellLink.WindowStyle=1
    echo     oShellLink.Hotkey=""
    echo     oShellLink.IconLocation=icon
    echo     oShellLink.Description=description
    echo     oShellLink.WorkingDirectory=strDesktop
    echo     oShellLink.Save
    echo End Sub
    echo MkDesktopLink "EasyPython�̳�.lnk" "%lib%" & "\\windows\\start.bat" "%lib%" & "\\logo.ico" "��EasyPython��ʼѧϰ"
) > "%mklinkvbs%"

if not exist "%pyexe%" (
    if not exist "%install%\pyinstall.exe" (
        echo ����Python3�У����Ժ�...
        cscript "%downloadvbs%"
    )
    echo ���԰�װPython3�У�������Ҫ15���ӣ����Ժ�...
    "%install%\pyinstall.exe" /quiet InstallAllUsers=1 PrependPath=1 Shortcuts=1 Include_pip=1 TargetDir="%pydir%"
    if exist "%pyexe%" && exist "%pipexe%" (
        echo Python3��װ�ɹ���
    ) else (
        echo Python3��װʧ�ܣ������ԣ�
        exit
    )
)

echo ��װ����ģ���У����Ժ�...
"%pipexe%" install jupyter wget gitpython requests jupyterlab -i https://pypi.douban.com/simple
if not exist "%gitexe%" (
    if not exist "%install%\git-install.exe" (
        "%pyexe%" -m wget "https://npm.taobao.org/mirrors/git-for-windows/v2.23.0.windows.1/Git-2.23.0-32-bit.exe" -o "%install%\git-install.exe"
        if not exist "%install%\git-install.exe" (
            echo ����git��װ����ʧ�ܣ�������...
            exit
        )
    )
    set installDir=%gitdir%
    set installDir=%installDir:"=%
    (
        echo [Setup]
        echo Lang=default
        echo Dir=%installDir%
        echo Group=Git
        echo NoIcons=0
        echo SetupType=default
        echo Components=icons,ext\reg\shellhere,assoc,assoc_sh
        echo Tasks=
        echo PathOption=Cmd
        echo SSHOption=OpenSSH
        echo CRLFOption=CRLFAlways
        echo BashTerminalOption=ConHost
        echo PerformanceTweaksFSCache=Enabled
        echo UseCredentialManager=Enabled
        echo EnableSymlinks=Disabled
        echo EnableBuiltinDifftool=Disabled
    ) > config.inf

    "%install%\git-install.exe" /VERYSILENT /LOADINF="config.inf"
    if errorlevel 1 (
        @echo on
        if %errorLevel% == 1 ( echo Error opening %file%. File may be corrupt. )
        if %errorLevel% == 2 ( echo Error reading %file%. May require elevated privileges. Run as administrator. )
        exit /b %errorlevel%
    )
    del config.inf

    net session >nul 2>&1
    if %errorLevel% == 0 (
        :: pathman /as "%PATH%;%installDir%/cmd"
        exit 0
    ) else (
        @echo on
        echo SYSTEM PATH Environment Variable may not be set, may require elevated privileges. Run as administrator if it doesn't already exist.
        exit /b 0
    )
    if not exist %gitexe% (
        echo git��װʧ�ܣ������ԣ�
        exit
    )
    "%gitexe%" config --global user.name learner
    "%gitexe%" config --global user.email learner@none.com
)

if not exist "%lib%\start.bat" (
    "%gitexe%" clone https://gitee.com/easypython/Easy_Python_Client.git "%lib%"
) else (
    "%gitexe%" pull origin master -C "%lib%"
)
if exist "%lib%\start.bat" (
    cscript "%mklinkvbs%"
    echo ��װ�ɹ���
    echo ������ϵͳ���⣬���Խ�%pro%��ȫɾ��������ȥ�������ذ�װ��
    echo ǿ���Ƽ���װChrome���������ΪĬ�ϣ���������޷���֤100%���ݣ�����IE�������ȫ�޷��������б�ϵͳ��
    echo ���»س����Զ���װChrome��������粻��Ҫ��������Ͻǹرձ����ں�˫�������EasyPython�̳̼���ʹ�ý̡̳�
    pause
    echo ����Chrome�У����Ժ�...
    if not exist "%install%\chrome-install.exe" (
        "%pyexe%" -m wget "http://www.chromeliulanqi.com/ChromeStandaloneSetup.exe" -o "%install%\chrome-install.exe"
    )
    echo ��װChrome�У����Ժ�...
    "%install%\chrome-install.exe" /silent /install
    echo "Chrome��װ��ɣ�"
) else (
    echo ��װʧ�ܣ���ɾ��%pro%�����ԡ�
)
pause
