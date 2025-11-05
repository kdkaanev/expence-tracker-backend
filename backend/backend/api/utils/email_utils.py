from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from datetime import datetime

FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
FRONTEND_URL = getattr(settings, "FRONTEND_URL", "https://your-frontend.com")  # set in settings/env


def build_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    # frontend will handle activation route e.g. /auth/activate?uid=...&token=...
    return f"{FRONTEND_URL}/auth/activate?uid={uid}&token={token}"


def send_activation_email(user):
    user_name = user.first_name or user.email
    activation_link = build_activation_link(user)
    context = {
        "user_name": user_name,
        "activation_link": activation_link,
        "year": datetime.now().year
    }

    subject = "Confirm your ExpenseTracker email"
    text_body = render_to_string("emails/activation_email.txt", context)
    html_body = render_to_string("emails/activation_email.html", context)

    msg = EmailMultiAlternatives(subject, text_body, FROM_EMAIL, [user.email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def build_password_reset_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{FRONTEND_URL}/auth/reset-password?uid={uid}&token={token}"


def send_password_reset_email(user):
    user_name = user.first_name or user.email
    reset_link = build_password_reset_link(user)
    context = {
        "user_name": user_name,
        "reset_link": reset_link,
        "year": datetime.now().year
    }

    subject = "Reset your ExpenseTracker password"
    text_body = render_to_string("emails/password_reset_email.txt", context)
    html_body = render_to_string("emails/password_reset_email.html", context)

    msg = EmailMultiAlternatives(subject, text_body, FROM_EMAIL, [user.email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()
