from flask import render_template, flash, session, redirect, url_for, request, make_response, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app import app
from app.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        return redirect(url_for('login', ac=account, pw=password))
    return render_template("index.html.j2")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ac = request.args.get('ac')
    pw = request.args.get('pw')
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