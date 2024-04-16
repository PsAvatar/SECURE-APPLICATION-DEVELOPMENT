from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.csrf.session import SessionCSRF
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
import re

load_dotenv()


app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect()
csrf.init_app(app)

# Check if the "MY_SECRET_KEY" environment variable is set
if "MY_SECRET_KEY" in os.environ:
    app.config['MY_SECRET_KEY'] = os.getenv("MY_SECRET_KEY")
else:
    # If "MY_SECRET_KEY" is not set, generate a random key
    app.config['MY_SECRET_KEY'] = os.urandom(32)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


bcrypt = Bcrypt(app)
mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'signup'

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        user = User()
        user.id = user_data[0]
        user.name = user_data[1]
        user.email = user_data[2]
        return user
    return None

class MyForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

    class Meta:
        csrf = True
        csrf_class = SessionCSRF

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/TourRecSys/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User()
            user.id = user_data[0]
            user.name = user_data[1]
            user.email = user_data[2]

            login_user(user)
            return redirect(url_for('home'))

        else:
            flash('Invalid email or password', 'error')

    return render_template('Login.html')


# Ορίζουμε το pattern για το email με χρήση regular expressions
email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@(?:gmail\.com|hotmail\.com)$')

# Έλεγχος αν το email πληροί τις προϋποθέσεις
def is_valid_email(email):
    return bool(email_pattern.match(email))

# Ορίζουμε το pattern για τον έλεγχο του password με χρήση regular expressions
password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!-,._])[A-Za-z!-,._0-9]{8,}$')

# Έλεγχος αν το password πληροί τις προϋποθέσεις
def is_valid_password(password):
    return bool(password_pattern.match(password))


@app.route('/TourRecSys/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Έλεγχος αν το email πληροί τις προϋποθέσεις
        if not is_valid_email(email):
            flash('Invalid email format. Please use a valid email address.', 'error')
            return render_template('Register.html', error_message='Invalid email format. Please use a valid email address.')

        # Έλεγχος αν το password πληροί τις προϋποθέσεις
        if not is_valid_password(password):
            flash('Password must contain at least one lowercase letter, one uppercase letter, and one special character (! - . _) and must be at least 8 characters long.', 'error')
            return render_template('Register.html', error_message='Password must contain at least one lowercase letter, one uppercase letter, and one special character (!-,._) and must be at least 8 characters long.')

        # Έλεγχος αν το email υπάρχει ήδη στη βάση δεδομένων
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return render_template('Register.html', error_message='Email already exists. Please use a different email.')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO login (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')


@app.route('/TourRecSys/Home', methods=['GET', 'POST'])
@login_required
def home():
    selected_location = request.form.get('selected_location')

    cur = mysql.connection.cursor()

    if selected_location and selected_location != 'all':
        cur.execute("SELECT * FROM restaurants WHERE location = %s ORDER BY average_rating DESC", (selected_location,))
    else:
        cur.execute("SELECT * FROM restaurants ORDER BY average_rating DESC")

    restaurants = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT AVG(rating) FROM ratings WHERE user_id = %s", (current_user.id,))
    user_average_rating = cur.fetchone()[0]
    cur.close()

    # Fetch latitude and longitude from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT latitude, longitude FROM restaurants")
    restaurant_coords = cur.fetchall()
    cur.close()

    return render_template('Home.html', restaurants=restaurants, user_average_rating=user_average_rating, restaurant_coords=restaurant_coords)

@app.route('/TourRecSys/Rate', methods=['POST'])
@login_required
def rate():
    if request.method == 'POST':
        restaurant_id = request.form['restaurant_id']
        rating = int(request.form['rating'])

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM ratings WHERE user_id = %s AND restaurant_id = %s", (current_user.id, restaurant_id))
            existing_rating = cur.fetchone()

        if existing_rating:
            flash('You have already rated this restaurant.', 'error')
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE restaurants SET total_ratings = total_ratings + 1, total_rating_sum = total_rating_sum + %s, average_rating = total_rating_sum / total_ratings WHERE id = %s", (rating, restaurant_id))
                mysql.connection.commit()

            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO ratings (user_id, restaurant_id, rating) VALUES (%s, %s, %s)", (current_user.id, restaurant_id, rating))
                mysql.connection.commit()
            flash('Rating submitted successfully!', 'success')

    return redirect(url_for('home'))

@app.route('/TourRecSys/average')
def average_rating():
    cur = mysql.connection.cursor()
    cur.execute("SELECT AVG(rating) FROM ratings")
    average_rating = cur.fetchone()[0]
    cur.close()

    return render_template('home.html', average_rating=average_rating)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=False)
