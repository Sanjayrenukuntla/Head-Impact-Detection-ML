from flask import Flask, render_template, request, redirect, url_for, session
import pickle
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Load the machine learning model
with open('clf.pkl', 'rb') as file:
    model = pickle.load(file)

# User data for authentication
users = {
    'admin': generate_password_hash('admin')  # Hashed password for admin
}

@app.route("/", methods=["GET", "POST"])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("IM IN LOGINN HEYY!!!!!!!!!!!!!")
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('home'))  # Redirect to home after successful login
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route("/input", methods=["POST", "GET"])
def input_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        try:
            aged = int(request.form["aged"])
            amnesiabef = int(request.form['amnesiabef'])
            basalskullfracture = int(request.form['basalskullfracture'])
            basa = int(request.form['basa'])
            trek = int(request.form['trek'])
            Ghmc = int(request.form['Ghmc'])
            amesia = int(request.form['clinically.important.brain.injury'])
            loss = int(request.form['loss'])
            open = int(request.form['open'])
            vomitings = int(request.form['vomitings'])

            result = model.predict([[aged, amnesiabef, basalskullfracture, basa, trek, Ghmc, amesia, loss, open, vomitings]])
            res = "High Risk" if result[0] == 1 else "Low Risk"
            return render_template("result.html", data=res)
        except Exception as e:
            return str(e)  
    return render_template("input.html")

@app.route("/result")
def result():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("result.html")

@app.route("/chart")
def charts():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("chart.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5002, debug=True)
