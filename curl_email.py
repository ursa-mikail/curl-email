import os
import shutil
import time
import subprocess
from datetime import datetime
import secrets

DIR_START = './sample_data/'
EMAIL_DIR = os.path.join(DIR_START, "emails")
CONFIG_DIR = os.path.join(DIR_START, "config")
ARCHIVE_DIR = os.path.join(DIR_START, "archived")
EMAIL_CONFIG_FILE = os.path.join(CONFIG_DIR, "email_addresses.txt") # u@yahoo.com; u@gmail.com;

def generate_random_hex(length):
    return secrets.token_hex(length)

def write_random_email(email_dir, recipient_email):
    random_subject = generate_random_hex(10)
    random_mark = generate_random_hex(20)
    
    email_content = f"""From: Ursa <u@yahoo.com>
To: Recipient Name <{recipient_email}>
Subject: Test Email {random_subject}

Test email sent using curl via Yahoo's SMTP server. mark: {random_mark}
"""

    timestamp = time.strftime("%Y-%m-%d_%H%M%S")
    email_filename = f"email_{timestamp}.txt"
    email_filepath = os.path.join(email_dir, email_filename)
    
    with open(email_filepath, 'w') as email_file:
        email_file.write(email_content)
    
    print(f"Generated email: {email_filename}")

def get_recipient_emails(config_file):
    with open(config_file, 'r') as file:
        content = file.read().strip()
        emails = [email.strip() for email in content.split(';') if email.strip()]
    return emails

def send_email(email_file, recipient):
    command = [
        "curl", "--url", "smtp://smtp.mail.yahoo.com:587", "--ssl-reqd",
        "--mail-from", "u@yahoo.com",
        "--mail-rcpt", recipient,
        "--upload-file", email_file,
        "--user", "u@yahoo.com:<>", # 
        "--verbose" # "--silent" # 
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Sending email to {recipient}")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

def archive_email(file_path):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M_%S_%f")[:-3]
    file_name = f"email_{timestamp}.txt"
    archive_path = os.path.join(ARCHIVE_DIR, file_name)
    shutil.move(file_path, archive_path)

def process_emails():
    for file_name in os.listdir(EMAIL_DIR):
        email_file_path = os.path.join(EMAIL_DIR, file_name)
        recipient_emails = get_recipient_emails(EMAIL_CONFIG_FILE)
        for recipient in recipient_emails:
            send_email(email_file_path, recipient)
        archive_email(email_file_path)

def run():
    if not os.path.exists(EMAIL_DIR):
        os.makedirs(EMAIL_DIR)
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    
    recipient_emails = get_recipient_emails(EMAIL_CONFIG_FILE)
    
    while True:
        for recipient_email in recipient_emails:
            write_random_email(EMAIL_DIR, recipient_email)
            process_emails()
            time.sleep(20)

if __name__ == "__main__":
    run()
