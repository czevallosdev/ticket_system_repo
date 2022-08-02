from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/about/")
def about():
    return render_template("about.html", user=current_user)

@views.route("/contact/")
def contact():
    return render_template("contact.html", user=current_user)

@views.route("/hello/")
@views.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@views.route("/api/data")
def get_data():
    return views.send_static_file("data.json")
