from flask import render_template, flash, session, redirect, url_for, request, make_response, url_for, jsonify
from flask_login import login_user, logout_user, login_required

from app import app, db
from app.models import *
from app.function import *

from datetime import datetime

import translators as ts
import google.generativeai as genai
import requests
import os

#API
genai.configure(api_key="AIzaSyBKKrru_GxR7mqkwhxCQArhR_visshHGRA")
model = genai.GenerativeModel('gemini-1.0-pro-latest')
weather_api_key = "HUWKPABHTM63Q2TKPPXW6XU3V"
aws_api_id = 'e5ajctjbfg'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        password_correct = check_password(password, account)
        if password_correct == "true":
            return render_template("menu.html.j2")
        else:
            if account or password is None:
                problem = "None"
            else:
                problem = "Wrong"
            return render_template("login.html.j2", problem=problem)
    return render_template("index.html.j2")

@app.route('/meun', methods=['GET', 'POST'])
def meun():
    return render_template("meun.html.j2")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        if account or password is None:
            flash('Please fill in your account name or password!', 'danger')
    return render_template('login.html.j2')

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


@app.route('/travel-itinerary-planner', methods=["GET", "POST"])
def planner():

    def generate_itinerary(source, destination, start_date, end_date, no_of_day):
        prompt = f"Generate a personalized trip itinerary for a {no_of_day}-day trip {source} to {destination} from {start_date} to {end_date}, with an optimum budget (Currency:HKD)."
        response = model.generate_content(prompt)
        return response.text

    def get_weather_data(weather_api_key: str, location: str, start_date: str, end_date: str) -> dict:
        # Date Formatting as per API "YYYY-MM-DD"
        base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={weather_api_key}&contentType=json"

        try:
            response = requests.get(base_url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    if request.method == "POST":
        global source, destination, start_date, end_date
        source = request.form.get("source")
        destination = request.form.get("destination")
        start_date = request.form.get("date")
        end_date = request.form.get("return")
        # Calculating the number of days
        no_of_day = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
        # Process the route input here
        if no_of_day < 0:
            flash("Return date should be greater than the Travel date (Start date).", "danger")
            return redirect(url_for("planner"))
        else:
            try:
                weather_data = get_weather_data(weather_api_key, destination, start_date, end_date)
            except requests.exceptions.RequestException as e:
                flash(f"Error in retrieving weather data: {e}", "danger")
                return redirect(url_for("planner"))
        
        try:
            plan = generate_itinerary(source, destination, start_date, end_date, no_of_day)
        except Exception as e:
            flash("Error in generating the plan. Please try again later.", "danger")
            return redirect(url_for("planner"))
        
        if weather_data:
            # Render the weather information in the template
            return render_template("travel-genai.html.j2", weather_data=weather_data, plan=plan)
    
    return render_template('travel-itinerary-planner.html.j2')

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
    u1 = User(userID=1, username='test01', email='test01@example.com', password=hash_password('Test01@'), login_state=True, last_login=datetime.now(), create_time=datetime.now())
    u2 = User(userID=2, username='test02', email='test02@example.com', password=hash_password('Test02@'), login_state=True, last_login=datetime.now(), create_time=datetime.now())
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