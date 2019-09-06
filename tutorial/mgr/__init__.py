import os
import sys
import uuid
import json
import pathlib
import hashlib
import requests
import subprocess


project_dir = pathlib.Path(__file__).parent.parent
auth_path = pathlib.Path(__file__).parent / 'auth.json'


class Mgr:
    def __init__(self):
        self.HOST = 'http://www.hzasteam.org:8097'
        self.HOST = 'http://localhost:5000'
        self.AUTH_PATH = pathlib.Path(__file__).parent / 'auth.json'
        self.WECHAT = 'Assert_'
    
    def save_auth_info(self, username, pwd):
        mac = self.get_mac_address()
        auth = {
            'username': username,
            'pwd': pwd,
            'mac': mac
        }
        with self.AUTH_PATH.open('w', encoding='utf-8') as fw:
            json.dump(auth, fw)
    
    def read_auth_info(self):
        with self.AUTH_PATH.open('r', encoding='utf-8') as fr:
            return json.load(fr)
    
    def login(self):
        username = input('请输入用户名')
        pwd = input('请输入密码')
        r = requests.post(f'{self.HOST}/login/{username}', json={'pwd': pwd})
        if r.ok:
            self.save_auth_info(username, pwd)
            print('登陆成功！')
            return True
        elif r.status_code == 401:
            print('用户名或密码错误！')
        else:
            print(f'错误代码：{r.status_code}，请稍后重试。')
        return False

    def reg(self):
        username = input('请输入用户名')
        r = requests.get(f'{self.HOST}/username_not_exists/{username}')
        if r.ok:
            pwd = input('请输入密码')
            pwd_chk = input('请再次输入密码')
            while pwd != pwd_chk:
                print('两次密码不一致！')
                pwd = input('请输入密码')
                pwd_chk = input('请再次输入密码')
            mac = self.get_mac_address()
            r = requests.post(f'{self.HOST}/reg/{username}', json={'pwd': pwd, 'mac': mac})
            if r.ok:
                self.save_auth_info(username, pwd)
                print('注册成功！')
                return True
            else:
                print(f'错误代码：{r.status_code}，网络错误，请稍后重试！')
                return False
        elif r.status_code == 401:
            print('用户名已存在！')
            return False
        print(f'错误代码：{r.status_code}')
        return False

    def sub(self, index):
        api = f'{self.HOST}/submit'
        file_path = self.get_test_file_path_by_index(index)    
        py_path = file_path.with_suffix('.py')
        if sys.argv[1] == 'submit':
            return None

        subprocess.call(['jupyter', 'nbconvert', '--to', 'python', str(file_path.resolve())], shell=False)

        ipts = self.get(index, release=True)
        if not ipts:
            os.remove(py_path)
            return False
        outputs = {}
        for quiz_dir_name, quiz in ipts.items():
            ipt = quiz['ipt'].strip()
            p = subprocess.Popen(['python', str(py_path.resolve()), 'submit', ipt], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            stdout, stderr = p.communicate()
            if stderr or not stdout:
                if stderr:
                    print(stderr.decode('utf-8').strip())
                    print('程序运行错误！')
                elif not stdout:
                    print('没有输出值！')
                os.remove(py_path)
                sys.exit(2)
            stdout = stdout.decode('utf-8').strip().replace('\r', '')
            if stdout == quiz['ans']:
                outputs[quiz_dir_name] = stdout
            else:
                self.error(index, quiz, stdout)
                os.remove(py_path)
                return False
        data = {
            'outputs': outputs,
            'auth': self.get_auth()
        }
        r = requests.post(f'{api}/{index}', json=data)
        if r.ok:
            print(r.text)
            os.remove(py_path)
            return None
        elif r.status_code == 401:
            print('用户认证错误！')
        elif r.status_code == 403:
            print(f'账户试用期已到，请联系微信{self.WECHAT}')
        else:
            print('网络错误！请检查网络或换个时间重试。')
        os.remove(py_path)
        return False

    def get(self, index, release=False):
        if len(sys.argv) > 1 and sys.argv[1] == 'submit':
            return sys.argv[2].strip()
        api = f'{self.HOST}/getipt'
        if release:
            url = f'{api}/release/{index}'
            r = requests.post(url, json={'auth': self.get_auth()})
            if r.ok:
                return r.json()
            elif r.status_code == 401:
                print('用户认证错误！')
            elif r.status_code == 403:
                print(f'账户试用期已到，请联系微信{self.WECHAT}')
        else:
            url = f'{api}/test/{index}'
            r = requests.post(url, json={'auth': self.get_auth()})
            if r.ok:
                print('数据获取成功！本次测试值为：')
                print(r.text)
                return r.text.strip()
            elif r.status_code == 401:
                print('用户认证错误！')
            elif r.status_code == 403:
                print(f'账户试用期已到，请联系微信{self.WECHAT}')
        return False

    def get_test_file_path_by_index(self, index):
        file_path = None
        for path in project_dir.iterdir():
            if index == path.name[:len(index)] and path.suffix.lower() == '.ipynb':
                file_path = path
                break
        if not file_path:
            print('没有这个序号的文件')
        return file_path


    def error(self, index, quiz, output):
        print('##############################')
        print(f'你提交的代码不正确(题目序号{index})：')
        ipt = quiz['ipt']
        ans = quiz['ans']
        print(f'输入值：{ipt}')
        print(f'正确输出值：{ans}')
        print(f'你的输出值：{output}')
        print('##############################')

    def get_auth(self):
        if not self.AUTH_PATH.exists():
            while True:
                i = input('你还未登陆，输入1注册账号，输入2登陆已有账号')
                if '1' in i:
                    if self.reg():
                        break
                elif '2' in i:
                    if self.login():
                        break
                else:
                    print('输入错误！请重试')
        with self.AUTH_PATH.open('r', encoding='utf-8') as fr:
            auth = json.load(fr)
        return auth

    def get_mac_address(self):
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        return mac


mgr = Mgr()
sub = mgr.sub
get = mgr.get
reg = mgr.reg
login = mgr.login

# def set_name():
#     username = ''
#     while len(username) < 2:
#         username = input('请输入你的昵称，至少2位（尽量长一些，不要和别人重名）：').strip()
#     with auth_path.open('w', encoding='utf-8') as fw:
#         json.dump({'username': username}, fw)

# def set_auth():
#     print('你的试用已结束，请完成如下信息填写：')
#     with auth_path.open('r', encoding='utf-8') as fr:
#         username = json.load(fr)['username']
#     mac = get_mac_address()
#     id_ = hashlib.sha256(f'{username}-{mac}'.encode('utf-8')).hexdigest()[:10]
#     print(f'你的ID为：{id_}')
#     print('你可以加微信xxx，发送你的ID给对方，获取序列号')
#     print('如已购买课程是免费获取的，如果你是在不同电脑上使用跳出此提示，也请联系该微信号')
#     token = input('请输入你获取到的序列号：')
#     auth = {
#         'username': username,
#         'id': id_,
#         'token': token
#     }
#     r = requests.post(f'{HOST}/auth_check', json=auth)
#     if r.ok and r.json().get('state'):
#         with auth_path.open('w', encoding='utf-8') as fw:
#             json.dump(auth, fw)
#         return True
#     return False
