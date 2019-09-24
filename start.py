import json
import shutil
import pathlib
import datetime
import subprocess


pro_dir = pathlib.Path(__file__).parent
tutorial_dir = pro_dir / 'tutorial'
trust_list_path = pro_dir / 'trust_list.json'
now = datetime.datetime.now()


def trust_notebook():
    if trust_list_path.exists():
        with trust_list_path.open('r', encoding='utf-8') as fr:
            trust_list = json.load(fr)['trust_list']
    else:
        trust_list = []
    for p in tutorial_dir.glob('**/*.ipynb'):
        if p.name not in trust_list:
            subprocess.call(f'jupyter trust {p}', shell=True)
            trust_list.append(p.name)
            with trust_list_path.open('w', encoding='utf-8') as fw:
                json.dump({'trust_list': trust_list}, fw)


def history_save():
    for p in tutorial_dir.glob('**/*'):
        sp = str(p.relative_to(tutorial_dir))
        if 'mgr' not in sp[:3] and '历史保存' not in sp[:4]:
            save_p = tutorial_dir / '历史保存' / now.strftime('%Y-%m-%d_%H%M%S') / sp
            save_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(p, save_p)


def git_update():
    history_save()
    subprocess.check_output(f'cd {pro_dir}; git checkout .', shell=True)
    subprocess.check_output(f'cd {pro_dir}; git pull origin master', shell=True)


if __name__ == '__main__':
    git_update()
    trust_notebook()
    print('系统启动中...')
    subprocess.call(f'cd {pro_dir};jupyter-notebook', shell=True)
