import os
import time
import wget
import subprocess
import pathlib
import sys


def down(urls, path):
    if path.exists():
        os.remove(path)
    for url in urls:
        try:
            print('尝试下载： {}'.format(url))
            wget.download(url, out=str(path))
            return True
        except Exception as e:
            print(e)
    print('网络错误，下载失败！请检查网络后重新运行本程序。')
    sys.exit(2)
    return False


pro_dir = pathlib.Path(__file__).parent.absolute()
git_path = pro_dir / 'git.exe'
install_git_path = pro_dir / 'install-git.bat'
chrome_path = pro_dir / 'chrome-install.exe'

git_download_urls = [
    'https://npm.taobao.org/mirrors/git-for-windows/v2.23.0.windows.1/Git-2.23.0-32-bit.exe', 
    # 'https://github.com/git-for-windows/git/releases/download/v2.23.0.windows.1/Git-2.23.0-32-bit.exe'
]

install_git_bat_download_urls = [
    'http://static.hzasteam.org/Easy_Python_Client/install-git.bat',
    # 'https://raw.githubusercontent.com/RainGather/Easy_Python/release/install-git.bat'
]

git_bare_urls = [
    'https://gitee.com/starfork/Easy_Python.git', 
    # 'https://github.com/RainGather/Easy_Python.git'
]

chrome_download_urls = [
    'http://www.chromeliulanqi.com/ChromeStandaloneSetup.exe'
]


if not git_path.exists():
    print('下载Git工具...')
    down(git_download_urls, git_path)
    down(install_git_bat_download_urls, install_git_path)
    time.sleep(2)
    print('安装Git中...')
    subprocess.check_call(str(pro_dir / 'install-git.bat'), shell=True)
    time.sleep(2)

print('获取Easy Python项目中...')
git_clone_dir = pro_dir.parent.absolute() / 'Easy_Python'
if git_clone_dir.exists():
    try:
        subprocess.check_call(f'cd {git_clone_dir}; C:\\git\\bin\\git.exe pull origin master', shell=False)
    except Exception as e:
        print(e)
else:
    try:
        subprocess.check_call(['C:\\git\\bin\\git.exe', 'clone', git_bare_urls[0], str(git_clone_dir.resolve())], shell=False)
    except Exception as e:
        print(e)
        # subprocess.check_call(['C:\\git\\bin\\git.exe', 'clone', git_bare_urls[1], git_clone_dir], shell=False)

subprocess.check_call('C:\\git\\bin\\git.exe config --global user.name \"learner\"', shell=True)
subprocess.check_call('C:\\git\\bin\\git.exe config --global user.email \"learner@none.com\"', shell=True)

time.sleep(2)

subprocess.call(str(git_clone_dir / 'MkDesktopLnk.vbs'), shell=True, cwd=str(git_clone_dir))

need_set_default = True
i = input('这台电脑是否有安装谷歌Chrome浏览器？是请输入yes并【回车】，不是或者不知道请输入no并【回车】\n')
need_install = i.lower() != 'yes'
if not need_install:
    input('按下【回车】后，会打开一个网页，请观察这个网页是不是用谷歌Chrome浏览器打开的\n')
    subprocess.call('start https://www.bing.com', shell=True)
    i = input('是谷歌Chrome浏览器，输入yes并【回车】，不是或者不知道请输入no并【回车】\n')
    need_set_default = i.lower() != 'yes'
if need_install:
    print('下载Chrome浏览器中...')
    down(chrome_download_urls, chrome_path)
    print('安装Chrome浏览器中...')
    subprocess.call('{} /silent /install'.format(chrome_path), shell=True)
if need_set_default:
    print('请在接下来打开的设置页面中，选择Chrome为默认浏览器。')
    input('按【回车】继续')
    subprocess.call('%windir%\\system32\\control.exe /name Microsoft.DefaultPrograms /page pageDefaultProgram\\pageAdvancedSettings?pszAppName=google%20chrome', shell=True)
print('安装完成，按【回车】将自动开启教程。之后可以双击桌面的【Easy Python教程】快捷方式来进入教程。')
input()
subprocess.call('C:\\python3\\Scripts\\jupyter-lab.exe', shell=True, cwd=str(git_clone_dir / 'tutorial'))
