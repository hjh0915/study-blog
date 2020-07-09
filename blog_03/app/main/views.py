from flask import render_template
from flask_login import login_required

from . import main

@main.route('/show_users')
@login_required #强制登录

def show_users():
    return render_template('main/index.html')