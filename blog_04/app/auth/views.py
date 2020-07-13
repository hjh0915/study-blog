from flask import render_template, request, redirect, make_response, url_for, flash
from flask import current_app
from flask_login import login_required, logout_user, login_user, current_user
from . import auth
from ..models import User
from .. import vcode
from ..email import send_email

# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint \
#                 and request.blueprint != 'auth' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))

# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #如果是get
    if request.method == 'GET':
        return render_template('auth/login.html')

    #如果是post,获取表单信息进行验证登录
    if request.method == 'POST':
        username = request.form.get('fname')
        password = request.form.get('fpwd')
        vcode = request.form.get('fcode')

        u = User.query.filter_by(username=username).first()
        if u == None:
            return render_template('auth/login.html')
        
        v = request.cookies.get('auth_code')

        if u.verify_password(password) and v == vcode:
            login_user(u)
            # return redirect('/main/show_user')
            return render_template('main/index.html')
        else:
            return render_template('auth/login.html')

@auth.route('/makeimage')
def make_image():
    """生成验证码"""

    s = vcode.gen_rand_str()
    c = vcode.make_image(current_app.config['IMAGE_FONT'], s)
    rsp = make_response(c.getvalue())
    rsp.mimetype = "image/jpeg"

    rsp.set_cookie('auth_code', s)

    return rsp

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/auth/login')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))