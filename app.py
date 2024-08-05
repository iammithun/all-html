from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
db_path = 'users.db'

def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, 
                password TEXT
            )
        ''')

def user_exists(username):
    with sqlite3.connect(db_path) as conn:
        result = conn.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone()
        return result is not None

def add_user(username, password):
    with sqlite3.connect(db_path) as conn:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

def verify_user(username, password):
    with sqlite3.connect(db_path) as conn:
        result = conn.execute('SELECT 1 FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        return result is not None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if user_exists(username):
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            add_user(username, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if verify_user(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Login failed. Please check your username and password.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
