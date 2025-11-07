import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ✅ Gmail sender credentials
from_address = "abhishekojha786786@gmail.com"
app_password = "ognojytoigydntpk"  # App password, not normal password


def send_mail(to_address, subject, body, attachment_path=None):
    """
    Sends an email with optional attachment using Gmail SMTP.
    """

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # (Optional) Add attachment
        if attachment_path:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment_path.split('/')[-1]}",
                )
                msg.attach(part)

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_address, app_password)
        server.send_message(msg)
        server.quit()

        print(f"📧 Email sent successfully to {to_address}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
