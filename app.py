import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import Mail
from config import settings
from dotenv import load_dotenv
from functools import wraps
import json
from itsdangerous import URLSafeTimedSerializer

s = URLSafeTimedSerializer(settings.SECRET_KEY)

load_dotenv()

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/forgot-password", methods=["GET", "POST"])
@login_required
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            token = s.dumps(email, salt="samplesalt")
            reset_url = url_for("reset_password", token=token, _external=True)
            
            mail_client = Mail(username="your-email@example.com",
                               password="your-email-password",
                               host="smtp.your-email-provider.com",
                               port=465)
            
            subject = "Password Reset Request"
            body = f"Click the link to reset your password: {reset_url}"
            resp, success = mail_client.send_mail([email], subject, body)
            
            if success:
                flash("Password reset email sent. Please check your inbox.", "success")
            else:
                flash("Error sending email. Please try again later.", "danger")
            
            return redirect(url_for("login")) 

    return render_template("forgot-password.html")



@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        # Decode the token to get the email
        email = s.loads(token, salt="samplesalt", max_age=3600)  # 1 hour expiration
    except:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        old_password = request.form.get("old_password")

        file_path = "old_passwords.json"
        data = {}

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)

        data[email] = old_password
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        flash("Your password has been reset successfully!", "success")
        return redirect(url_for("login"))

    return render_template("reset-password.html", email=email)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin1234":
            session['logged_in'] = True
            flash("You have successfully logged in.")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for("login"))

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)
