from flask import Flask, request,render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hslfdk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_app'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passwrd = db.Column(db.String(120), nullable=False)
  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    form_username = request.form['username']
    form_password = generate_password_hash(request.form['password'])
    db_username =  User.query.filter_by(username=form_username).first()
    if db_username:
        return "Username already exists"
    else:
        new_user = User(username=form_username, passwrd=form_password)
        return "User created successfully"
        
@app.route('/login', methods=['POST'])
def login():
    form_username = request.form['username']
    form_password = request.form['password']
    user = User.query.filter_by(username=form_username).first()
    if user and User.check_password(form_password):
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')

if __name__ == '__main__':
    app.run(debug=True)