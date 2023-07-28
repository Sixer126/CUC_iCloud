### 主要贡献

对放心传的密码管理，针对密码的修改找回储存等方面进行了实现尝试。由于发现从头实现目标功能对我来说较为困难，我在前人代码的基础上进行了改进。

分别从前后端完成了功能的实现。

##### 部分前端代码
body
div class="container"
    div class="forgot-box"
        div class="forgot-box-header"
            h1重置密码/h1
            pPlease enter your email address below to reset your password./p
        /div
        div
            form action="forgot"method="post"
                div class="form-group"
                    input type="email" class="form-control" id="email" name="email" placeholder="请输入你的邮箱"
                /div
                div class="form-box"
                   button 获取验证码/button
                /div
            /form
        /div
    /div
/div
/body
##### 后端
@pages.route('/forgot')
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if email == '':
            flash('请输入邮箱')
            return redirect(url_for('forgot'))
        else:
            sql = bigflySQL()
            if sql.check_email(email):
                flash('已发送验证邮件，请查收')
                sendMail(email)
                return redirect(url_for('set_password'))
            else:
                flash('邮箱未注册')
                return redirect(url_for('forgot'))
    return render_template('forgot.html', pageName='forgot')


@pages.route('/set_password')
def setpassword():
    if request.method == 'POST':
        passwd = request.form['passwd']
        if passwd == '':
            flash('请输入密码')
            return redirect(url_for('set_password'))
        else:
            sql = bigflySQL()
            if sql.set_password(passwd):
                flash('密码设置成功')
                return redirect(url_for('login'))
            else:
                flash('密码设置失败')
                return redirect(url_for('set_password'))
        return redirect(url_for('login'))
    return render_template('set_password.html', pageName='setpassword')

### 遇到的问题
遇到了很多按照所想去更改实现代码功能的时候，发现无法运行，或者运行之后很多地方直接错位失效等等。解决办法就比较简单，尝试一点一点去调试改正，将成功时候的和之前进行一个对比，找出问题到底出现在哪里。