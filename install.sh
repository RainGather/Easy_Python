#!/bin/bash

source ~/.bashrc

PRO_DIR=~/EasyPythonApp
INSTALL_DIR=$PRO_DIR/Install
mkdir -p $INSTALL_DIR 2>/dev/null
LIB_DIR=$PRO_DIR/EasyPythonLib
TUTORIAL_DIR=$LIB_DIR/tutorial

if [ -z `python --version 2>/dev/null | grep 3.` ] && [ -z `python3 --version 2>/dev/null` ]; then
    echo "找不到Python3。现在开始下载Python3..."
    if [ ! -f "$INSTALL_DIR/python-install.pkg" ]; then
        wget -O $INSTALL_DIR/python-install.pkg -c "https://npm.taobao.org/mirrors/python/3.6.6/python-3.6.6rc1-macosx10.9.pkg" || (echo "下载出错，请重新运行命令" && exit(2))
    fi
    echo "开始安装Python3，请跟着提示进行，安装完成后重新运行本命令。"
    open python-install.pkg
    exit()
fi

if [ -z `git --version 2>/dev/null` ]; then
    echo "找不到git，现在开始下载git..."
    if [ ! -f "$INSTALL_DIR/git-install.pkg" ]; then
        wget -O $INSTALL_DIR/git-install.dmg -c "https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect"
    fi
    echo "开始安装git，请跟着提示进行，安装完成后重新运行本命令。"
    open git-install.dmg
    exit()
fi

pip3 install jupyter wget gitpython requests jupyterlab -i https://pypi.douban.com/simple || (echo "安装失败，请重试！" && exit(2))

if [ -d $LIB_DIR ]; then
    git -C $LIB_DIR pull origin master
else
    git clone https://gitee.com/easypython/Easy_Python_Client.git $LIB_DIR
    git config --global user.name learner
    git config --global user.email learner@none.com
fi

if [ -z `cat ~/.bashrc | grep easypython ` ]; then
    echo "alias easypython='jupyter notebook --notebook-dir=$TUTORIAL_DIR'" > ~/.bashrc
    echo "alias ezpy=easypython" > ~/.bashrc
fi

echo "安装成功！请在命令行输入easypython或ezpy运行"
