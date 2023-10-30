from flask import render_template, redirect, flash


from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html.j2")

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    return render_template('forget.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html.j2')