from flask import render_template, flash, session, redirect, url_for, request, make_response, url_for, jsonify
from flask_login import login_user, logout_user, login_required

from app import app, db
from app.models import *

from datetime import datetime

import translators as ts
import requests
import os

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
    translator = Translator.query.order_by(Translator.translator).all()
    if request.method == 'POST':
        text = request.form['text']
        language_from = request.form['langFrom']
        language_to = request.form['langTo']
        translator_select = request.form['translatorSelect']

        translate_out = ts.translate_text(query_text=text, translator=translator_select, from_language=language_from, to_language=language_to)
        translator_id = Translator.query.filter_by(translator=translator_select).first().translatorID
        translation_list = Translation.query.filter_by(translatorID=translator_id).all()
        language_list = Language.query.join(Translation).filter(Translation.translatorID == translator_id).with_entities(Language.language).all()

        serialized_translations = []
        for translation in translation_list:
            serialized_translation = {
                'languageCode': translation.languageCode,
            }
            serialized_translations.append(serialized_translation)

        serialized_languages = []
        for language in language_list:
            serialized_language = {
                'language': language.language,
            }
            serialized_languages.append(serialized_language)

        t_details = {"translate_out": translate_out, "translation_list": serialized_translations, "language_list": serialized_languages}
        return jsonify(t_details)
    return render_template('translate.html.j2', translator=translator)

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    return render_template('forget.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html.j2')

@app.route('/flight', methods=['GET', 'POST'])
def flight():
    return render_template('flight.html.j2')

################################################################## ( Default Data ) ##################################################################

@app.route('/dbtest')
def dbtest():
    db.create_all()
    u1 = User(userID=1, username='john1', email='john1@example.com', password='test01@', login_state=True, last_login=datetime.now(), create_time=datetime.now())
    u2 = User(userID=2, username='susan1', email='susan1@example.com', password='test02@', login_state=True, last_login=datetime.now(), create_time=datetime.now())
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    return "Done"


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    # Find the translator files in the app/default folder
    translator_files = [filename for filename in os.listdir('app/default') if filename.startswith('translate-')]

    for filename in translator_files:
        # Extract the translator value from the filename
        translator = filename.replace('translate-', '').replace('.txt', '')

        # Check if the translator already exists in the Translator table
        existing_translator = Translator.query.filter_by(translator=translator).first()
        if not existing_translator:
            # Find the maximum translatorID and increment it by 1
            max_translator_id = db.session.query(db.func.max(Translator.translatorID)).scalar()
            translator_id = max_translator_id + 1 if max_translator_id else 1

            # Add the translator to the Translator table
            new_translator = Translator(translatorID=translator_id, translator=translator, create_time=datetime.now())
            db.session.add(new_translator)

        else:
            # Use the existing translatorID
            translator_id = existing_translator.translatorID

        # Get the file path for the current translator file
        file_path = os.path.join('app', 'default', filename)

        # Read the data from the current translator file
        with open(file_path, 'r') as file:
            data = file.readlines()

        for line in data:
            # Parse the language code and name from each line
            lang_code, lang_name = line.strip().split(':')

            # Check if the language already exists in the Language table
            existing_language = Language.query.filter_by(language=lang_name).first()
            if existing_language:
                lang_id = existing_language.langID
            else:
                # Add the language to the Language table
                max_lang_id = db.session.query(db.func.max(Language.langID)).scalar()
                lang_id = max_lang_id + 1 if max_lang_id else 1
                new_language = Language(langID=lang_id, language=lang_name, create_time=datetime.now())
                db.session.add(new_language)

            # Check if the translation already exists in the Translation table
            existing_translation = Translation.query.filter_by(languageCode=lang_code, translatorID=translator_id, langID=lang_id).first()
            if existing_translation:
                continue  # Skip adding the translation if it already exists

            # Find the maximum translationID and increment it by 1
            max_translation_id = db.session.query(db.func.max(Translation.translationID)).scalar()
            translation_id = max_translation_id + 1 if max_translation_id else 1

            # Add the translation to the Translation table
            translation = Translation(translationID=translation_id, languageCode=lang_code, translatorID=translator_id, langID=lang_id, create_time=datetime.now())
            db.session.add(translation)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Data added successfully'})