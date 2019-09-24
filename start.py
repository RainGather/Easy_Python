import json
import shutil
import filecmp
import pathlib
import datetime
import subprocess


pro_dir = pathlib.Path(__file__).parent
tutorial_dir = pro_dir / 'tutorial'
history_save_dir = tutorial_dir / '历史保存'
trust_list_path = pro_dir / 'trust_list.json'
now = datetime.datetime.now()


def trust_notebook():
    if trust_list_path.exists():
        with trust_list_path.open('r', encoding='utf-8') as fr:
            trust_list = json.load(fr)['trust_list']
    else:
        trust_list = []
    for p in tutorial_dir.glob('*.ipynb'):
        if p.name not in trust_list:
            subprocess.call(f'jupyter trust {p}', shell=True)
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
    git_cmd = 'C:\\Git\\bin\\git.exe'
    if not pathlib.Path(git_cmd).exists():
        git_cmd = 'git'
    subprocess.check_output([git_cmd, '-C', str(pro_dir.resolve()), 'checkout', '.'])
    subprocess.check_output([git_cmd, '-C', str(pro_dir.resolve()), 'pull', 'origin', 'master'])
    for p in history_save_dir.glob('**/*'):
        cmp_p = tutorial_dir / p.relative_to(history_save_dir)
        if cmp_p.exists() and filecmp.cmp(p, cmp_p):
            shutil.rmtree(p)


if __name__ == '__main__':
    print('系统更新中...')
    git_update()
    trust_notebook()
    print('系统启动中...')
    subprocess.call(['jupyter-notebook', '--notebook-dir', str(tutorial_dir.resolve())])
