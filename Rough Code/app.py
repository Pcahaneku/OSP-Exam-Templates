from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from model import db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='avery_long_secret_random_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/') #This leads users to the Homepage
def homepage():
    return render_template('index.html')

@app.route('/register') #This leads users to the Registration Page
def register():
    return render_template('register.html') 

@app.route('/register', methods=['POST'])
def add_users():
    if request.method == 'POST':

        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        plain_password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

        dob = request.form.get('dob')

        if dob: 
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date() #Converts the date of birth string to a date object
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD."

        new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password, dob=dob)

        try:
            db.session.add(new_user) 
            db.session.commit()
            return render_template('login.html') #directs users to the Login Page
        except Exception as e:
            return f"An error occured: {e}"
        
@app.route('/login') #This leads users to the Login Page
def login():
    return render_template('login.html') 




#This helps in running the app in debug mode. By reloading the server when code changes.
if __name__ == '__main__':
    app.run(debug=True)