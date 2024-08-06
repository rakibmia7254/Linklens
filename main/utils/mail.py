from django.core.mail import send_mail


# Email Service
email_service = False

APP_NAME = "Linklens"
email_from = "mail@linklens.com"
URL = "http://localhost:8000"


def send_forgot_password_email(email, token):
    subject = f"Reset your {APP_NAME} password"

    ACTION_URL = f"{URL}/reset_password/{token}"

    body = f"""
    <p>Hello,</p>
    <p>Click on the button below to reset your password.</p>
    <p>
    <a class="btn" href="{ACTION_URL}" target="_blank" rel="noopener">Reset password</a>
    </p>
    <p><i>If you didn't ask to reset your password, you can ignore this email.</i></p>
    <p>
        Thanks,<br/>
        {APP_NAME} team
    </p>"""

    send_mail(subject, body, email_from, [email])


def send_verify_email(email, token):
    subject = f"Verify your {APP_NAME} account"

    ACTION_URL = f"{URL}/verify/{token}"

    body = f"""
        <p>Hello,</p>
        <p>Thank you for joining us at {APP_NAME}.</p>
        <p>Click on the button below to verify your email address.</p>
        <p>
          <a class="btn" href="{ACTION_URL}" target="_blank" rel="noopener">Verify</a>
        </p>
        <p>
          Thanks,<br/>
          {APP_NAME} team
        </p>"""
    send_mail(subject, body, email_from, [email])
