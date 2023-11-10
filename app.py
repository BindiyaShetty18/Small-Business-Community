from flask import Flask, render_template, request, redirect, url_for
# ...

import sqlite3

app = Flask(__name__)

# Configure a SQLite database
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, name TEXT, email TEXT, rating INTEGER, message TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('signup_success'))

    return render_template('signup.html')

@app.route('/signup/success')
def signup_success():
    return 'Signup successful! Thank you for registering.'

@app.route('/feedback.html', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        rating = request.form.get('rating')
        message = request.form.get('message')
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)", (name, email, rating, message))
        conn.commit()
        conn.close()

        return redirect(url_for('feedback_success'))

    return render_template('feedback.html')
   
@app.route('/feedback/success')
def feedback_success():
    return 'Feedback successful! Thank you for your feedback.'

if __name__ == '__main__':
    app.run(debug=True) 


