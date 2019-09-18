function hide_input() {
    var cell_i = 0
    var divs = document.getElementsByTagName("div")
    for (var i = 0; i < divs.length; i++) {
        if (divs[i].getAttribute("class") && divs[i].getAttribute("class").indexOf('cell text_cell') != -1 && divs[i].textContent.indexOf("# 注意！严重错误！") != -1) {
            divs[i].style.display = 'none'
        }
        if (divs[i].getAttribute("class") == 'input' && divs[i].textContent.indexOf("%%html") != -1 || divs[i].textContent.indexOf("%%js") != -1) {
            // if (divs[i].textContent.indexOf("%%js") == -1) {
            //     Jupyter.notebook.execute_cells([cell_i])
            // }
            divs[i].style.display = 'none'
        }
        if (divs[i].getAttribute("class") && (divs[i].getAttribute("class").indexOf('cell text_cell') != -1 || divs[i].getAttribute("class").indexOf('cell code_cell') != -1)) {
            cell_i++
        }
    }
}

function if_login_btn_show_cb(out_data) {
    var output = out_data.content.text.trim()
    $("#loading").hide()
    if (output != "False") {
        $("#username_show").text(output)
        $("#username_show").show()
        $("#login_btn").hide()
        $(".login_ui").hide()
        $(".reg_ui").hide()
        $(".change_pwd_ui").hide()
        $("#logout_btn").show()
        $("#manage_btn").show()
        $("#reg_btn").hide()
    } else {
        $("#username_show").hide()
        $("#login_btn").show()
        $("#logout_btn").hide()
        $("#manage_btn").hide()
        $("#reg_btn").show()
    }
}

function if_login_btn_show() {
    var callback = {
        iopub: {
            output: if_login_btn_show_cb,
        }
    }
    var code = "import os, json\np=os.path.join('mgr', 'auth.json')\nif os.path.exists(p):\n with open(p, 'r', encoding='utf-8') as fr:\n  c=json.load(fr)\n print(c['username'])\nelse:\n print(False)"
    IPython.notebook.kernel.execute(code, callback)
}

function login_show() {
    var login = document.getElementsByTagName("login")[0]
    if (login.style.display == "none") {
        login.style.display = "inline"
    } else {
        login.style.display = "none"
    }
}

window.onload = function () {
    this.hide_input()
    this.if_login_btn_show()
    requirejs.config({
        paths: {
            axios: "//cdn.bootcss.com/axios/0.19.0-beta.1/axios.min",
            mdui: "//cdn.bootcss.com/mdui/0.4.3/js/mdui.min"
        }
    })
}
