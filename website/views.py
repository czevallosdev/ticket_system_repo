from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import Ticket, User

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
            formatted_headings.append('Owner')
        else:
            formatted_headings.append(
                str(header).replace('ticket.', '').capitalize().replace('_', ' '))

    tickets = db.session.query(Ticket).filter(
        Ticket.user_id == current_user.id)
    tickets = db.session.query(Ticket)
    my_tickets = []
    remaining_tickets = []
    for ticket in tickets:
        user = db.session.query(User).filter(User.id == ticket.user_id).first()
        if ticket.user_id == current_user.id:
            my_tickets.append(
                [ticket.id, user.email, ticket.title, ticket.description, ticket.date_added])
        else:
            remaining_tickets.append(
                [ticket.id, user.email, ticket.title, ticket.description, ticket.date_added])

    return render_template("tickets.html", user=current_user, headings=formatted_headings, my_tickets=my_tickets, remaining_tickets=remaining_tickets)


@views.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        new_ticket = Ticket(
            title=title, description=description, user=current_user)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket created!', category='success')
        return redirect(url_for('views.tickets'))

    return render_template("create_ticket.html", user=current_user)


@views.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    ticket_to_update = Ticket.query.get_or_404(id)
    if request.method == 'POST':
        ticket_to_update.title = request.form.get('title')
        ticket_to_update.description = request.form.get('description')

        try:
            db.session.commit()
            flash('Ticket Updated!', category='success')
            return redirect(url_for('views.tickets'))
        except:
            raise RuntimeError("There was an error when updating the ticket")
    return render_template("update_ticket.html", user=current_user, ticket_to_update=ticket_to_update)


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


@views.route("/users/")
def users():
    # Get the headings for the Ticket table
    headings = User.__table__.columns
    formatted_headings = []
    for header in headings:
        if 'password' in str(header):
            continue
        formatted_headings.append(
            str(header).replace('user.', '').capitalize().replace('_', ' '))

    users = db.session.query(User)
    filtered_users = []
    for user in users:
        filtered_users.append(
            [user.id, user.email, user.first_name, user.last_name, user.role])

    return render_template("users.html", user=current_user, headings=formatted_headings, data=filtered_users)


@views.route("/api/data")
def get_data():
    return views.send_static_file("data.json")
