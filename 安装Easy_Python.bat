@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd %~dp0

python --version 2>NUL && pip --version 2>NUL && goto PIP || echo ��ĵ��Կ�����û�а�װ��Python(��δ��Python��Script����PATH����)...����ȥ��ָ���㰲װPython

for /r %%f in (python-3*.exe) do (
    call set file="%%f"
    @echo on
    @echo �ҵ�Python3��װ�ļ��� %%f
    @echo off
)

if [%file%]==[] (
    echo δ�ҵ�Python3��װ�ļ��������㰴�¡���������󣬽����Զ����������������Python3��װ�ļ���
    echo ��Python3��װ�ļ�������ɺ󣬽���ŵ��� ��װEasy_Python.bat �ļ�ͬĿ¼�£����������б�����
    pause
    start https://npm.taobao.org/mirrors/python/3.6.6/python-3.6.6.exe
    exit
)

echo ��װPython3(%file%)�У�������Ҫ15���ӣ����Ժ�...
%file% /quiet InstallAllUsers=1 PrependPath=1 Shortcuts=1 Include_pip=1 TargetDir=C:\python3
echo Python3��װ�ɹ���

:PIP
echo ��װ����ģ���У����Ժ�...
pip install jupyter wget gitpython requests jupyterlab -i https://pypi.douban.com/simple
mkdir install
cd install
if exist install.py (
    del install.py
)
python -m wget "http://static.hzasteam.org/Easy_Python_Client/install.py" -o install.py
if not exist install.py (
    python -m wget "https://raw.githubusercontent.com/RainGather/Easy_Python/master/install.py" -o install.py
)
python install.py

echo �����ȫ����װ���̣����п��ܻ���Ϊ�����ԭ����ʧ�ܣ�������޷�����ʹ�ñ���Ŀ�����������б�����װ��������������˳���
pause
