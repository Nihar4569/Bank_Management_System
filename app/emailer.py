import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# from app.config import app_password, from_address

from_address = "abhishekojha786786@gmail.com"
app_password = "ognojytoigydntpk"

#send email method
def send_mail(to_address, subject, body, attachment_path):
    try:
        #create the email
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "Plain"))

        #Attach file
        if attachment_path:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content Description",
                    f"attachment; filename = {attachment_path.split('/')[-1]}"
                )
                msg.attach(part)

        # Send email via Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_address, app_password)
        server.send_message(msg)
        server.quit()

        return True


    except Exception as e:
        print("Error:", e)
        return False
    
#send email
receiver = input("Enter receiver email: ")  # placeholder for any email
subject = input("Enter subject: ")
body = input("Enter message: ")
attachment = input("Enter file path (or press Enter to skip): ")

if attachment.strip() == "":
    attachment = None

result = send_mail(receiver, subject, body, attachment)
print("Mail sent successfully?", result)