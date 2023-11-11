from flask import render_template, flash, session, redirect, url_for, request, make_response, url_for
from flask_login import login_user, logout_user, login_required

from app import app
from app.forms import LoginForm

app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        session['ac'] = account
        session['pw'] = password
        return redirect(url_for('login'))
    return render_template("index.html.j2")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ac = session.get('ac')
    pw = session.get('pw')
    session.pop('ac', None)  # 從session中移除'ac'
    session.pop('pw', None)  # 從session中移除'pw'
    return render_template('login.html.j2', ac=ac, pw=pw)

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    return render_template('forget.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html.j2')

@app.route('/flight', methods=['GET', 'POST'])
def flight():
    return render_template('flight.html.j2')