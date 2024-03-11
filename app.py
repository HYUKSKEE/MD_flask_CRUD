from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/김진혁/Desktop/MD_flask_CRUD/db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=True, nullable=False)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    owner = db.relationship('User', foreign_keys=[owner_id])
    comments = db.relationship('Comment', backref='feed', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    writer_name = db.Column(db.String(32), nullable=False)
    comment = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    
    user = db.relationship('User', foreign_keys=[user_id])
    writer = db.relationship('User', foreign_keys=[writer_id])


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    dat = {}
    dat['users'] = User.query.all()
    if request.method == 'GET':
        return render_template('home.html', **dat)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


