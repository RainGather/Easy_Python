import pathlib
import subprocess


def trust_notebook():
    pro_dir = pathlib.Path(__file__).parent
    tutorial_dir = pro_dir / 'tutorial'
    for p in tutorial_dir.glob('**/*.ipynb'):
        subprocess.call(f'jupyter trust {p}', shell=True)


if __name__ == '__main__':
    trust_notebook()
