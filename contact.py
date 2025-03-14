from flask import Blueprint, request, redirect, url_for, flash, current_app
from flask_mail import Mail, Message

contact_bp = Blueprint('contact', __name__)  # Unique name
mail = Mail()

@contact_bp.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    subject = f"Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    try:
        msg = Message(subject=subject,
              sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Specify sender
              recipients=[current_app.config['MAIL_USERNAME']],
              body=body)
        print("MAIL_DEFAULT_SENDER:", current_app.config.get("MAIL_DEFAULT_SENDER"))
        print("MAIL_USERNAME:", current_app.config.get("MAIL_USERNAME"))


        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        print(f"Error sending mail: {e}")
        flash('Failed to send your message. Please try again later.', 'danger')

    return redirect(url_for('home'))
