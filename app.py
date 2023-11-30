from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Configure MySQL database
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'admin123'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'users'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # To receive results as dictionaries

    # Initialize MySQL
    mysql.init_app(app)

    # Define the init_db function
    def init_db():
     with app.app_context():
        conn = mysql.connection
        cursor = conn.cursor()

        try:
            cursor.execute('DROP TABLE IF EXISTS users')
            cursor.execute('DROP TABLE IF EXISTS feedback')
            cursor.execute('''
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    rating INT NOT NULL,
                    message TEXT NOT NULL
                )
            ''')
            print("Tables 'users' and 'feedback' created successfully")
            conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()

    # Run init_db only once
    init_db()

    # Rest of your routes...
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about.html')
    def about():
        return render_template('about.html')


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
            password = request.form['password']

            # Insert the user into the database
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()

            # Redirect to a success page or display a success message
            return redirect(url_for('signup_success'))

        return render_template('signup.html')

    # Signup success route
    @app.route('/signup-success')
    def signup_success():
        return 'Signup completed successfully!'

    @app.route('/feedback.html', methods=['GET', 'POST'])
    def feedback():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            rating = request.form['rating']
            message = request.form['message']
            
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (name, email, rating, message) VALUES (%s, %s, %s, %s)", (name, email, rating, message))
            conn.commit()
            cursor.close()

            return redirect(url_for('feedback_success'))

        return render_template('feedback.html')
       
    @app.route('/feedback-success')
    def feedback_success():
        return 'feedback completed successfully! , Thanks for your feedback !'

    return app

# Create the app using the factory function
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

