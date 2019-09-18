var FLAG = "退出账号</button>"

function get_filename() {
    var divs = document.getElementsByTagName("span")
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].getAttribute("class") == 'filename') {
            return divs[i].textContent
        }
    }
    return false
}

function get_source_code() {
    var cell_i = 0
    var divs = document.getElementsByTagName("div")
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].getAttribute("class") && (divs[i].getAttribute("class").indexOf("cell text_cell") != -1 || divs[i].getAttribute("class").indexOf("cell code_cell") != -1)) {
            if (divs[i].getAttribute("class").indexOf("cell code_cell") != -1 && divs[i].textContent.indexOf(FLAG) != -1) {
                var code = Jupyter.notebook.get_cell(cell_i - 1)
                if (code) {
                    return code.get_text()
                } else {
                    return false
                }
            }
            cell_i++
        }
    }
    return false
}

function output_(out_data) {
    if (out_data.msg_type == "error") {
        result = ""
        for (var error in out_data.content.traceback) {
            result += out_data.content.traceback[error].replace(/\n/g, "<br>").trim() + "<br>"
        }
        var output = result.replace(/\[.*?m/g, '') + out_data.content.evalue.replace(/\n/g, "<br>")
        $("#html_output").html(output)
        // document.getElementsByTagName("output")[0].innerHTML = output
    } else {
        var output = out_data.content.text.replace(/\n/g, "<br>")
        $("#html_output").html(output)
        // document.getElementsByTagName("output")[0].innerHTML = output
    }
}

function change_pwd() {
    var old_pwd = $("#old_pwd").val()
    var new_pwd = $("#new_pwd").val()
    var chk_new_pwd = $("#chk_new_pwd").val()
    $("#old_pwd").val("")
    $("#new_pwd").val("")
    $("#chk_new_pwd").val("")
    if (chk_new_pwd != new_pwd) {
        $("#html_output").html("密码不一致！")
        requirejs(['mdui'], function(mdui) {
            mdui.alert("密码不一致！")
        })
        return false
    }
    change_pwd_code = "import mgr\nmgr.change_pwd('" + old_pwd + "', '" + new_pwd + "')"
    var callback = {
        iopub: {
            output: notice,
        }
    }
    IPython.notebook.kernel.execute(change_pwd_code, callback)
}

function reg() {
    var username = $("#reg_username").val()
    var pwd = $("#reg_pwd").val()
    var chk_pwd = $("#reg_chk_pwd").val()
    if (chk_pwd != pwd) {
        $("#html_output").html("密码不一致！")
        requirejs(['mdui'], function(mdui) {
            mdui.alert("密码不一致！")
        })
        return false
    }
    reg_code = "import mgr\nmgr.reg('" + username + "', '" + pwd + "')"
    var callback = {
        iopub: {
            output: notice,
        }
    }
    IPython.notebook.kernel.execute(reg_code, callback)
}

function notice(out_data) {
    if (out_data.msg_type == "error") {
        result = ""
        for (var error in out_data.content.traceback) {
            result += out_data.content.traceback[error].replace(/\n/g, "<br>").trim() + "<br>"
        }
        var output = result.replace(/\[.*?m/g, '') + out_data.content.evalue.replace(/\n/g, "<br>")
        $("#html_output").html(output)
    } else {
        var output = out_data.content.text//.replace(/\n/g, "<br>")
        // alert(output)
        $("#html_output").html(output)
        requirejs(['mdui'], function(mdui) {
            mdui.alert(output)
        })
    }
    if_login_btn_show()
}

function logout() {
    logout_code = "import os\nos.remove(os.path.join('mgr', 'auth.json'))\nprint('退出成功！')"
    var callback = {
        iopub: {
            output: notice,
        }
    }
    IPython.notebook.kernel.execute(logout_code, callback)
}

function login() {
    username = $("#username").val()
    pwd = $("#pwd").val()
    $("#username").val("")
    $("#pwd").val("")
    login_code = "import mgr\nmgr.login('" + username + "', '" + pwd + "')"
    var callback = {
        iopub: {
            output: notice,
        }
    }
    IPython.notebook.kernel.execute(login_code, callback)
}

function sub() {
    var code = get_source_code()
    // alert(typeof(code))
    var code = code.replace(/\"\"\"/g, "\\\"\\\"\\\"").replace(/\\/g, "\\\\")
    var filename = get_filename()
    var sub_code = "import mgr\nmgr.substr(\"\"\"" + filename + "\"\"\", \"\"\"" + code + "\"\"\")"
    var callback = {
        iopub: {
            output: output_,
        }
    }
    IPython.notebook.save_notebook()
    IPython.notebook.kernel.execute(sub_code, callback)
}

function run_cell() {
    var cell_i = 0
    var divs = document.getElementsByTagName("div")
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].getAttribute("class") && (divs[i].getAttribute("class").indexOf("cell text_cell") != -1 || divs[i].getAttribute("class").indexOf("cell code_cell") != -1)) {
            if (divs[i].getAttribute("class").indexOf("cell code_cell") != -1 && divs[i].textContent.indexOf(FLAG) != -1) {
                Jupyter.notebook.execute_cells([cell_i - 1])
                return true
            }
            cell_i++
        }
    }
    return false
}

function jump(out_data) {
    var output = out_data.content.text.trim()
    window.open(output)
}

function next_page(i) {
    next_code = "import pathlib\npj = pathlib.Path('.')\nps = []\nfor p in pj.glob('*-*.ipynb'):\n ps.append(p.name)\nps.sort()\ni = ps.index('" + get_filename()  + ".ipynb')\nprint(ps[i + " + i + "])"
    var callback = {
            iopub : {
                output : jump,
        }
    }
    IPython.notebook.kernel.execute(next_code, callback)
}
