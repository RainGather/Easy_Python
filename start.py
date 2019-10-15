import json
import os
import shutil
import filecmp
import pathlib
import datetime
import subprocess


easy_python_client_dir = pathlib.Path(__file__).parent.absolute()
pro_dir = pathlib.Path(__file__).parent.parent.absolute()
tutorial_dir = easy_python_client_dir / 'tutorial'
history_save_dir = tutorial_dir / '历史保存'
trust_list_path = easy_python_client_dir / 'trust_list.json'
git_exe = pro_dir / 'git' / 'bin' / 'git.exe'
if not git_exe.exists():
    git_exe = 'git'
else:
    git_exe = str(git_exe.resolve())
jupyter_notebook_exe = pro_dir / 'python' / 'Scripts' / 'jupyter-notebook.exe'
if not jupyter_notebook_exe.exists():
    jupyter_notebook_exe = 'jupyter-notebook'
else:
    jupyter_notebook_exe = str(jupyter_notebook_exe.resolve())
jupyter_exe = pro_dir / 'python' / 'Scripts' / 'jupyter.exe'
if not jupyter_exe.exists():
    jupyter_exe = 'jupyter'
else:
    jupyter_exe = str(jupyter_exe.resolve())
now = datetime.datetime.now()


def trust_notebook():
    if trust_list_path.exists():
        with trust_list_path.open('r', encoding='utf-8') as fr:
            trust_list = json.load(fr)['trust_list']
    else:
        trust_list = ['000-HelloWorld.ipynb']
    for p in tutorial_dir.glob('*.ipynb'):
        if p.name not in trust_list:
            subprocess.call([jupyter_exe, 'trust', str(p.resolve())])
            trust_list.append(p.name)
            with trust_list_path.open('w', encoding='utf-8') as fw:
                json.dump({'trust_list': trust_list}, fw)


def history_save():
    for p in tutorial_dir.glob('**/*'):
        sp = str(p.relative_to(tutorial_dir))
        if 'mgr' not in sp[:3] and '历史保存' not in sp[:4]:
            save_p = history_save_dir / now.strftime('%Y-%m-%d_%H%M%S') / sp
            save_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(p, save_p)


def git_update():
    history_save()
    subprocess.check_output([git_exe, '-C', str(easy_python_client_dir.resolve()), 'checkout', '.'])
    subprocess.check_output([git_exe, '-C', str(easy_python_client_dir.resolve()), 'pull', 'origin', 'master'])
    for p in history_save_dir.glob('**/*'):
        if p.is_dir(): continue
        cmp_p = tutorial_dir / pathlib.Path(*p.relative_to(history_save_dir).parts[1:])
        if cmp_p.exists() and filecmp.cmp(p, cmp_p):
            os.remove(p)
    for p in history_save_dir.glob('**/*'):
        if p.is_dir():
            try:
                os.rmdir(p)
            except Exception as e:
                pass


if __name__ == '__main__':
    try:
        print('系统更新中...')
        git_update()
        trust_notebook()
        print('系统启动中...')
        subprocess.call([jupyter_notebook_exe, '--notebook-dir', str(tutorial_dir.resolve())])
    except Exception as e:
        print(e)
        print('系统错误，请查看网络是否正常，系统时间是否正常，如一切正常请关闭打开重试。')
