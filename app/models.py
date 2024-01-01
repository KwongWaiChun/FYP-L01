from datetime import datetime
from app import app, db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    login_state = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class Profile(db.Model):
    profileID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(50), nullable=True)

class Language(db.Model):
    langID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    language = db.Column(db.String(50), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class Translator(db.Model):
    translatorID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    translator = db.Column(db.String(50), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class Translation(db.Model):
    translationID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    languageCode = db.Column(db.String(10), nullable=False)
    translatorID = db.Column(db.Integer, db.ForeignKey('Translator.translatorID'), nullable=False)
    langID = db.Column(db.Integer, db.ForeignKey('Language.langID'), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class TranslateRecord(db.Model):
    transl_recordID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    translationID = db.Column(db.Integer, db.ForeignKey('Translation.translationID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=False)
    text_input = db.Column(db.Text, nullable=False)
    text_output = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class TranslateFeedback(db.Model):
    transl_feedbackID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=False)
    translatorID = db.Column(db.Integer, db.ForeignKey('Translator.translatorID'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

class TranslateScores(db.Model):
    transl_scoresID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=False)
    translationID = db.Column(db.Integer, db.ForeignKey('Translation.translationID'), nullable=False)
    scores = db.Column(db.Float, nullable=False)
