from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import Ticket

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


@views.route("/tickets/")
def tickets():
    # Get the headings for the Ticket table
    headings = Ticket.__table__.columns
    formatted_headings = []
    for header in headings:
        if 'user_id' in str(header):
            continue
        formatted_headings.append(
            str(header).replace('ticket.', '').capitalize().replace('_', ' '))

    tickets = db.session.query(Ticket)
    filtered_tickets = []
    for ticket in tickets:
        filtered_tickets.append(
            [ticket.id, ticket.title, ticket.description, ticket.date_added])

    return render_template("tickets.html", user=current_user, headings=formatted_headings, data=filtered_tickets)


@views.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        new_ticket = Ticket(title=title, description=description)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket created!', category='success')
        return redirect(url_for('views.tickets'))

    return render_template("create_ticket.html", user=current_user)


@views.route("/delete/<int:id>")
def delete(id):
    ticket_to_delete = Ticket.query.get_or_404(id)
    try:
        db.session.delete(ticket_to_delete)
        db.session.commit()
        flash('Ticket successfully deleted!', category='success')
        return redirect(url_for('views.tickets'))
    except:
        return RuntimeError("Error when deleting the ticket")


@views.route("/api/data")
def get_data():
    return views.send_static_file("data.json")
