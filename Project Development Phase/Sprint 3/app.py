from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import login_user, LoginManager, login_required, logout_user
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_cors import CORS
import joblib
import users_db
import requests

# Enter your API key here
api_key = "9dc73970faafde4beb008b5e93ca7ab1"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# api key from my cloud account
API_KEY = "Ke3Pq9j_CPfm7SmFG5cJerK2XZ4J-AeEMDYrAlxIxnA1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
CORS(app)

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'vidyaibm'

conn = users_db.connect("DATABASE=bludb;HOSTNAME=7ubf76c4-r56c-4ay0-72v9-ac2b4345f4a4.c3n31cmd0npnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ibq38740;PWD=uX6v3MioF6cEBa7c", '', '')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    stmt = users_db.prepare(conn, 'SELECT * FROM user WHERE id=?')
    users_db.bind_param(stmt, 1, user_id)
    users_db.execute(stmt)
    user = users_db.fetch_tuple(stmt)
    usr_obj = User(user[0], user[1], user[2])
    return usr_obj

class User:
    def __init__(self, id, email, username):
        self.id = id
        self.username = username
        self.email = email

    def to_json(self):
        return {"username": self.username, "email": self.email}
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder":"Email"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    rollnumber = StringField(validators=[InputRequired(), Length(min=5, max=10)], render_kw={"placeholder":"RollNumber"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        stmt = users_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        users_db.bind_param(stmt, 1, username.data)
        users_db.execute(stmt)
        existing_user_username = users_db.fetch_tuple(stmt)
        if existing_user_username:
            raise ValidationError('That username already exists. Try another one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    oldpassword = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Previous Password"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Update')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        stmt = users_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        users_db.bind_param(stmt, 1, form.username.data)
        users_db.execute(stmt)
        user = users_db.fetch_tuple(stmt)
        if user:
            if bcrypt.check_password_hash(user[4], form.password.data):
                usr_obj = User(user[0], user[1], user[2])
                login_user(usr_obj)
                return redirect(url_for('welcome'))
            else:
                print('Hello')
                flash(f'Invalid credentials, check and try logging in again.', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return render_template('welcome.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        stmt = ibm_db.prepare(conn, 'INSERT INTO user (email, username, roll_number, pass_word) VALUES (?, ?, ?, ?)')
        users_db.bind_param(stmt, 1, form.email.data)
        users_db.bind_param(stmt, 2, form.username.data)
        users_db.bind_param(stmt, 3, form.rollnumber.data)
        users_db.bind_param(stmt, 4, hashed_password)
        #hash causes size to exceed VARCHAR size in DB2, hence made VARCHAR(8000)
        users_db.execute(stmt)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@ app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        stmt = users_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        users_db.bind_param(stmt, 1, form.username.data)
        users_db.execute(stmt)
        user = users_db.fetch_tuple(stmt)
        if user:
            if bcrypt.check_password_hash(user[4], form.oldpassword.data):
                print(user)
                hashed_password1 = bcrypt.generate_password_hash(form.password.data)
                stmt = users_db.prepare(conn, 'UPDATE user SET pass_word=? WHERE username=?')
                users_db.bind_param(stmt, 1, hashed_password1)
                users_db.bind_param(stmt, 2, form.username.data)
                user = users_db.execute(stmt)
                flash(f'Password changed successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'Invalid password, Enter valid password.', 'danger')
                return redirect(url_for('update'))
        else:
            flash(f'Invalid user, Enter valid User.', 'danger')
            return redirect(url_for('update'))
    return render_template('update.html', form=form)


@app.route('/predict', methods=['POST'])
def predictSpecies():
    hwl = float(request.form['hwl']) 
    cn = input(request.form['cn']) 
    # complete_url variable to store complete url address
    complete_url = base_url + "q=" + cn + "&appid=" + api_key
    # get method of requests module 
    # return response object
    response = requests.get(complete_url)
 
    # json method of response object
    # convert json format data into python format data
    x = response.json()
 
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
 
        # store the value of "main"
        # key in variable y
        y = x["main"]
 
        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]
 
        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]
 
        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        #store the value of "wind"
        # key in variable a
        a = x["wind"]

        # store the value corresponding
        # to the "wind speed" key of a
        current_windspeed = a["speed"]
        current_winddeg = a["deg"]
 
        # store the value of "weather"
        # key in variable z
        z = x["weather"]
 
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

    else:
        print(" City Not Found ")
    X = [[current_temperature, current_pressure, current_humidity, current_windspeed, current_winddeg,hwl]]

    ## NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [[current_temperature, current_pressure, current_humidity, current_windspeed, current_winddeg,hwl]], "values": X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9c062b2f-991b-489c-956b-93a8f76f45b5/predictions?version=2022-11-19', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print("Final prediction : ",predict)

    return render_template('predict.html',predict=predict)

if __name__ == "__main__":
    app.run(debug=True)

