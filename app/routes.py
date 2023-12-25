from flask import render_template, flash, session, redirect, url_for, request, make_response, url_for, jsonify
from flask_login import login_user, logout_user, login_required
from app import app
from app.forms import LoginForm
import translators as ts
import requests

app.secret_key = 'super secret key'

#API
api_id = 'e5ajctjbfg'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        session['ac'] = account
        session['pw'] = password

        # Create a dictionary with the data to send
        data = {
            'account': account,
            'password': password
        }

        # Make an HTTP POST request to the API Gateway endpoint
        response = requests.post('https://' + api_id + '.execute-api.us-east-1.amazonaws.com/prod/data', json=data)

        response_data = response.json()

        # Access the message from the response
        message = response_data['message']
        session['ms'] = message

        if response.status_code == 200:
            # Handle a successful response from the API Gateway
            return redirect(url_for('login'))
        else:
            # Handle an error response from the API Gateway
            # You can display an error message to the user or perform other error handling logic
            session.pop('ac', None)  # 從session中移除'ac'
            session.pop('pw', None)  # 從session中移除'pw'
            return redirect(url_for('index'))
    return render_template("index.html.j2")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ac = session.get('ac')
    pw = session.get('pw')
    ms = session.get('ms')
    session.pop('ac', None)  # 從session中移除'ac'
    session.pop('pw', None)  # 從session中移除'pw'
    session.pop('ms', None)
    return render_template('login.html.j2', ac=ac, pw=pw, ms=ms)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        language_from = request.form['langFrom']
        language_to = request.form['langTo']
        text = request.form['text']
        translate_out = ts.translate_text(query_text=text, translator='deepl', from_language=language_from,to_language=language_to)
        return jsonify({'translation': translate_out})
    return render_template('translate.html.j2')

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    return render_template('forget.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html.j2')

@app.route('/flight', methods=['GET', 'POST'])
def flight():
    return render_template('flight.html.j2')