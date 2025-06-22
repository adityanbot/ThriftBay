from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib  # For password hashing (optional but recommended)
import mysql.connector as msc

app = Flask(__name__)
app.secret_key = 'totally_encrypted_key'  # Secret key for session handling

# Database connection
db = msc.connect(host="localhost", user="root", passwd="deens", database="thriftbay")
mycursor = db.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    mycursor.execute("USE thriftbay;")
    mycursor.execute("SELECT * FROM userdata;")
    userdataDB = mycursor.fetchall()

    emailList = [row[0] for row in userdataDB]

    if username not in emailList:
        flash("Username does not exist. Please sign up.")
        return redirect(url_for('login'))

    ind = emailList.index(username)
    stored_password = userdataDB[ind][1]

    # Simple password check (consider using hashing later)
    if password == stored_password:
        session['username'] = username
        flash("Login successful.")
        return redirect(url_for('home'))
    else:
        flash("Incorrect password.")
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash("You must be logged in to view this page.")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    mycursor.execute("USE thriftbay;")

    try:
        mycursor.execute("INSERT INTO userdata (email, password) VALUES (%s, %s);", (username, password))
        db.commit()
        flash(f"Account created for {username}. Please log in.")
        return redirect(url_for('login'))
    except msc.Error:
        flash("Account with this email already exists.")
        return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)
