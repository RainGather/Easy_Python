@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
set pro="%~dp0EasyPython"
set lib=%pro%\lib
set install=%pro%\install
set pydir=%pro%\python
set pyexe=%pydir%\python.exe
set pipexe=%pydir%\Scripts\pip.exe
set downloadvbs=%install%\download.vbs
set mklinkvbs=%install%\mklink.vbs
set gitdir=%pro%\git
git --version 2>NUL && set gitexe=git || set gitexe=%gitdir%\bin\git.exe
%pro:~1,2%
cd "%~dp0"

echo ��ر���������360����Ѷ�ܼҵ��п�������ϵͳ�޸ĵİ�ȫ�������ֹϵͳ��װ����
echo ȷ�Ϲرպ��밴���س���������...
pause
echo ==============================================
mkdir %pro% 2>NUL
mkdir %install% 2>NUL

python --version 2>NUL && goto IFPYVERSION || goto INSTALLPY

:IFPYVERSION
python -c "import sys;sys.version_info.major != 3 or sys.version_info.minor < 6 and print('python�汾���ͣ������Զ���װ���°汾��') and sys.exit(2)" && set pyexe=python && set pipexe=python -m pip && goto INSTALLPIP || goto INSTALLPY

:INSTALLPY
if not exist %install%\pyinstall.exe (
    echo ����Python3�У����Ժ�...
    bitsadmin /transfer "����Python3�У����Ժ�..." "https://npm.taobao.org/mirrors/python/3.6.6/python-3.6.6.exe" %install%\pyinstall.exe
)
echo ���԰�װPython3�У�������Ҫ15���ӡ�
echo �ڼ䴰�ڲ������κα仯��������;�رմ��ڣ�����ᵼ�°�װʧ�ܣ�
echo ���Ժ�...
echo ==============================================
%install%\pyinstall.exe /quiet InstallAllUsers=1 PrependPath=1 Shortcuts=1 Include_pip=1 TargetDir=%pydir%
%pipexe% --version 2>NUL && (
    echo Python3��װ�ɹ���
    echo ===============================================
) || (
    echo Python3��װʧ�ܣ�
    echo ��򿪡�������塿�еġ�����͹��ܡ���������Pythonж�أ���ɾ��%pro%�ļ��У�Ȼ�����°�װ��
    pause
    exit
)

:INSTALLPIP
echo ��װ����ģ���У����Ժ�...
%pipexe% install jupyter wget gitpython requests jupyterlab -i https://pypi.douban.com/simple --upgrade
echo ===============================================

%gitexe% --version 2>NUL && goto GITCLONE

:INSTALLGIT
(
    echo δ�ҵ�git���򣬳��԰�װ��...
    if not exist %install%\git-install.exe (
        %pyexe% -m wget "https://npm.taobao.org/mirrors/git-for-windows/v2.23.0.windows.1/Git-2.23.0-32-bit.exe" -o %install%\git-install.exe
        if not exist %install%\git-install.exe (
            echo ����git��װ����ʧ�ܣ�������...
            pause
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

    %install%\git-install.exe /VERYSILENT /LOADINF="config.inf"
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
        pause
        exit
    )
    %gitexe% config --global user.name learner
    %gitexe% config --global user.email learner@none.com
)

:GITCLONE
if not exist %lib%\start.bat (
    %gitexe% clone https://gitee.com/easypython/Easy_Python_Client.git %lib%
) else (
    %gitexe% -C %lib% pull origin master 2>NUL
)
if exist %lib%\start.bat (
    (
        echo set WshShell=WScript.CreateObject("WScript.Shell"^)
        echo strDesktop=WshShell.SpecialFolders("Desktop"^)
        echo set oShellLink=WshShell.CreateShortcut(strDesktop ^& "\EasyPython�̳�.lnk"^)
        echo oShellLink.TargetPath=%lib%\start.bat
        echo oShellLink.WindowStyle=1
        echo oShellLink.Hotkey=""
        echo oShellLink.IconLocation=%lib%\logo.ico
        echo oShellLink.Description="��EasyPython��ʼѧϰ"
        echo oShellLink.WorkingDirectory=strDesktop
        echo oShellLink.Save
    ) > mklink.vbs
    cscript mklink.vbs
    del mklink.vbs

    echo ��װ�ɹ���
    echo ǿ���Ƽ���װChrome���������ΪĬ�ϣ���������޷���֤100%���ݣ�����IE�������ȫ�޷��������б�ϵͳ��
    echo ���¡��س������Զ���װChrome��������粻��Ҫ��������Ͻǹرձ����ں�˫������ġ�EasyPython�̡̳�����ʹ�ý̡̳�
    pause
    echo ����Chrome�У����Ժ�...
    if not exist %install%\chrome-install.exe (
        %pyexe% -m wget "http://www.chromeliulanqi.com/ChromeStandaloneSetup.exe" -o %install%\chrome-install.exe
    )
    echo ��װChrome�У����Ժ�...
    %install%\chrome-install.exe /silent /install
    echo Chrome��װ��ɣ�
) else (
    echo ��װʧ�ܣ����ڡ�������塿�ġ�����͹��ܡ��У�ж��Python3.6.6��Git����ɾ��%pro%�����ԣ�
)
pause
