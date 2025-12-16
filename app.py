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
        
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('input_page'))  # Redirect to home after successful login
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route("/input", methods=["POST", "GET"])
def input_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        try:
            # Extracting the form data (make sure field names match exactly)
            age_65 = int(request.form["age.65"])
            amnesia_before = int(request.form['amnesia.before'])
            basal_skull_fracture = int(request.form['basal.skull.fracture'])
            gcs_decrease = int(request.form['GCS.decrease'])
            gcs_13 = int(request.form['GCS.13'])
            gcs_15_2hours = int(request.form['GCS.15.2hours'])
            loss_of_consciousness = int(request.form['loss.of.consciousness'])
            open_skull_fracture = int(request.form['open.skull.fracture'])
            vomiting = int(request.form['vomiting'])
            clinically_important_brain_injury = int(request.form['clinically.important.brain.injury'])

            # Prepare the input data for the model (use the same order as the model's training data)
            input_data = [[age_65, amnesia_before, basal_skull_fracture, gcs_decrease, gcs_13, gcs_15_2hours,
                           loss_of_consciousness, open_skull_fracture, vomiting, clinically_important_brain_injury]]

            # Predict the result
            result = model.predict(input_data)

            # Return the result as "High Risk" or "Low Risk"
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
def chart():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("chart.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5002, debug=True)
