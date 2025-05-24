import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_email(subject: str, body: str, to_email: str) -> bool:
    from_email = settings.email_id
    password = settings.email_password

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
