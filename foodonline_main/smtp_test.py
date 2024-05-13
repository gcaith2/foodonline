import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "gcaith2@gmail.com"
SMTP_PASSWORD = "hner zuyy qocg lanh"

# Sender and recipient email addresses
SENDER_EMAIL = "gcaith2@gmail.com"
RECIPIENT_EMAIL = "gcaith2@gmail.com"

# Email content
subject = 'SMTP Connection Test'
body = 'This is a test email sent using Python and smtplib.'

# Create a MIMEText object
message = MIMEMultipart()
message['From'] = SENDER_EMAIL
message['To'] = RECIPIENT_EMAIL
message['Subject'] = subject

# Attach body to the email
message.attach(MIMEText(body, 'plain'))

try:
    # Establish a connection to the SMTP server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Start TLS encryption
    # Login to the SMTP server
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    
    # Send the email
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
    print('Email sent successfully!')
    
except Exception as e:
    print(f'Error sending email: {e}')

finally:
    # Close the connection to the SMTP server
    server.quit()
