import os
import re
import sys
import uuid
import json
import pathlib
import hashlib
import requests
import platform
import subprocess

from io import StringIO


project_dir = pathlib.Path(__file__).parent.parent
auth_path = pathlib.Path(__file__).parent / 'auth.json'


class Mgr:
    def __init__(self):
        self.HOST = 'http://ep.hzasteam.org'
        self.DEBUG_HOST = 'http://localhost:5000'
        self.AUTH_PATH = pathlib.Path(__file__).parent / 'auth.json'
        self.CONTACK = '微信：Assert_，QQ群：820510014(申请备注:EasyPython)'
        self.LOGIN_HTML_PATH = pathlib.Path(__file__).parent / 'account.html'
        self.check_debug()
    
    def check_debug(self):
        try:
            r = requests.get(f'{self.DEBUG_HOST}/username_not_exists/test', timeout=0.5)
            if r.ok or r.status_code == 401:
                self.HOST = self.DEBUG_HOST
        except Exception as e:
            pass
    
    def save_auth_info(self, username, pwd):
        mac = self.get_mac_address()
        auth = {
            'username': username,
            'pwd': pwd,
            'mac': mac
        }
        with self.AUTH_PATH.open('w', encoding='utf-8') as fw:
            json.dump(auth, fw)
    
    def login(self, username, pwd):
        r = requests.post(f'{self.HOST}/login/{username}', json={'pwd': pwd}, timeout=10)
        if r.ok:
            self.save_auth_info(username, pwd)
            print('登陆成功！')
            return True
        elif r.status_code == 401:
            print('用户名或密码错误！')
        else:
            print(f'错误代码：{r.status_code}，请稍后重试。')
        return False

    def change_pwd(self, old_pwd, new_pwd):
        auth = self.get_auth()
        username = auth['username']
        save_pwd = auth['pwd']
        if old_pwd != save_pwd:
            print('旧密码错误！')
            return False
        r = requests.post(f'{self.HOST}/change_pwd/{username}', json={'old_pwd': old_pwd, 'new_pwd': new_pwd}, timeout=10)
        if r.ok:
            self.save_auth_info(username, new_pwd)
            print('修改密码成功！')
            return True
        elif r.status_code == 401:
            print('认证错误！')
            return False
        print(f'错误代码：{r.status_code}')
        return False

    def reg(self, username, pwd):
        r = requests.get(f'{self.HOST}/username_not_exists/{username}', timeout=10)
        if r.ok:
            mac = self.get_mac_address()
            r = requests.post(f'{self.HOST}/reg/{username}', json={'pwd': pwd, 'mac': mac}, timeout=10)
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
    
    def substr(self, filename, code):
        if not self.get_auth():
            print('未登陆！请点击右侧“登陆账户”按钮登陆！')
            return False
        code = code.strip().replace('\r', '')
        # code = code.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '')
        # with open('temp_run.py', 'w', encoding='utf-8') as fw:
        #     fw.write(code)
        index = filename.split('-')[0]
        api = f'{self.HOST}/submit'
        ipts = self.get(index)
        if not ipts:
            print('获取测试数据失败！')
            return False
        outputs = {}
        for quiz_dir_name, quiz in ipts.items():
            ipt = quiz['ipt'].strip().replace('\r', '')
            p = subprocess.Popen(['python', '-c', code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            shell_encoding = 'gbk' if 'windows' in platform.system().lower() else 'utf-8'
            out, err = p.communicate(input=ipt.encode(shell_encoding))
            if err:
                err = err.decode(shell_encoding).strip()
                self.error(index, quiz, err)
                return False
            output = out.decode(shell_encoding).strip().replace('\r', '')
            if output == quiz['ans']:
                outputs[quiz_dir_name] = output
            else:
                self.error(index, quiz, output)
                return False
        data = {
            'outputs': outputs,
            'auth': self.get_auth()
        }
        r = requests.post(f'{api}/{index}', json=data, timeout=10)
        if r.ok:
            print(r.text)
            return True
        elif r.status_code == 401:
            print('用户认证错误！请退出重新登陆！')
        elif r.status_code == 403:
            print(f'账户试用期已到，请联系{self.CONTACK}')
        elif r.status_code == 406:
            print(f'提交错误！请勿hack！')
        else:
            print('网络错误！请检查网络或换个时间重试。')
        return False

    def get(self, index):
        if not self.get_auth():
            return False
        api = f'{self.HOST}/getipt'
        url = f'{api}/release/{index}'
        r = requests.post(url, json={'auth': self.get_auth()}, timeout=10)
        if r.ok:
            return r.json()
        elif r.status_code == 401:
            print('用户认证错误！请退出重新登陆！')
        elif r.status_code == 403:
            print(f'账户试用期已到，请联系微信{self.CONTACK}')
        else:
            print('网络错误！')
        return False

    def error(self, index, quiz, output):
        print('##############################')
        print(f'你提交的代码不正确(题目序号{index})：')
        ipt = quiz['ipt']
        ans = quiz['ans']
        print('------------------------------')
        print(f'输入值：\n{ipt}')
        print('------------------------------')
        print(f'正确输出值：\n{ans}')
        print('------------------------------')
        print(f'你的输出值：\n{output}')
        print('------------------------------')
        print('##############################')

    def get_auth(self):
        if not self.AUTH_PATH.exists():
            return False
        with self.AUTH_PATH.open('r', encoding='utf-8') as fr:
            auth = json.load(fr)
        return auth

    def get_mac_address(self):
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        return mac


mgr = Mgr()
get = mgr.get
reg = mgr.reg
login = mgr.login
substr = mgr.substr
change_pwd = mgr.change_pwd


if __name__ == '__main__':
    substr('004T2-测试_输入', """i=input();i=input();print(i) # 请修改此处代码""")
