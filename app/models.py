from datetime import datetime
from app import app, db


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    login_state = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    
    profile = db.relationship('Profile', backref='user', uselist=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(255))
    follow = db.Column(db.Integer, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False, index=True)
    nickname = db.Column(db.String(255))
    introduction = db.Column(db.Text)
    state = db.Column(db.String(255))

class TranslateLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), nullable=False)
    language_id = db.Column(db.String(255), nullable=False, unique=True, index=True)
    translation_services = db.Column(db.String(255), nullable=False)
    
    records = db.relationship('TranslateRecord', backref='library', lazy=True)

class TranslateRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False, index=True)
    text_input = db.Column(db.Text, nullable=False)
    text_output = db.Column(db.Text, nullable=False)
    translation_services = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    
    feedback = db.relationship('TranslateFeedback', backref='record', lazy=True)
    
    library_id = db.Column(db.Integer, db.ForeignKey('translate_library.id'), nullable=False)

class TranslateFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False, index=True)
    translation_services = db.Column(db.String(255), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('translate_record.id'), nullable=False)

class TranslateScores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False, index=True)
    translation_services = db.Column(db.String(255), nullable=False)
    scores = db.Column(db.Integer, nullable=False)