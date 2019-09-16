import json
import pathlib
import subprocess


def trust_notebook():
    pro_dir = pathlib.Path(__file__).parent
    tutorial_dir = pro_dir / 'tutorial'
    trust_list_path = pro_dir / 'trust_list.txt'
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


if __name__ == '__main__':
    trust_notebook()
