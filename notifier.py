from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_sms_alert(to_number, message, twilio_sid, twilio_token, from_number):
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    print(f"SMS sent: SID={message.sid}")


def send_email_alert(to_email, subject, body, smtp_server, smtp_port, from_email, email_password):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_email, email_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully")
