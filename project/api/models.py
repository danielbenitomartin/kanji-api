# project/api/models.py


import datetime

from project import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()


class Kanji(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'kanj'
    entr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txt = db.Column(db.String(1), nullable=False)

    def __init__(self, entr, txt):
        self.entr = entr
        self.txt = txt

class Character(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'chr'
    entr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chr = db.Column(db.String(1), nullable=False)
    bushu = db.Column(db.Integer, nullable=False)
    strokes = db.Column(db.Integer, nullable=False)
    freq = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    jlpt = db.Column(db.Integer, nullable=False)

    def __init__(self, entr, chr, bushu, strokes, freq, grade, jlpt):
        self.entr = entr
        self.chr = chr
        self.bushu = bushu
        self.strokes = strokes
        self.freq = freq
        self.grade = grade
        self.jlpt = jlpt

class Entry(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'entr'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    src = db.Column(db.Integer, nullable=False)
    stat = db.Column(db.Integer, nullable=False)
    seq = db.Column(db.Integer, nullable=False)

    def __init__(self, id, seq):
        self.id = id
        self.seq = seq

class Meaning(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'gloss'
    entr = db.Column(db.Integer, nullable=False)
    sens = db.Column(db.Integer, nullable=False)
    gloss = db.Column(db.Integer, primary_key=True, nullable=False)
    lang = db.Column(db.Integer, nullable=False)
    ginf = db.Column(db.Integer, nullable=False)
    txt = db.Column(db.String(100), nullable=False)

    def __init__(self, entr, sens, gloss, lang, ginf, txt):
        self.entr = entr
        self.sens = sens
        self.gloss = gloss
        self.lang = lang
        self.ginf = ginf
        self.txt = txt

class Reading(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'rdng'
    entr = db.Column(db.Integer, nullable=False)
    rdng = db.Column(db.Integer, primary_key=True, nullable=False)
    txt = db.Column(db.String(10), nullable=False)

    def __init__(self, entr, rdng, txt):
        self.entr = entr
        self.rdng = rdng
        self.txt = txt

class ReadingInfo(db.Model):
    #__bind_key__ = 'kanji'
    __tablename__ = 'rinf'
    entr = db.Column(db.Integer, nullable=False)
    rdng = db.Column(db.Integer, primary_key=True, nullable=False)
    kw = db.Column(db.Integer, nullable=False)

    def __init__(self, entr, rdng, kw):
        self.entr = entr
        self.rdng = rdng
        self.kw = kw
