""" Send the email of the day defined in a CSV file """

__author__ = "c.gaspar"
__version__ = "0.1.0"
__license__ = "MIT"


import email, smtplib, ssl
import base64 
import yaml 
import argparse
import os
import datetime
import csv


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def arg_parse():
    """ This is executed when run from the command line """

    text_description = """ email of the day : send the email of the day defined in a CSV file
"""
    parser = argparse.ArgumentParser(
        description=text_description,
        formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('-c', dest='config',
                        action='store', required=False,
                        default='~/.email-of-the-day/configuration.yml',
                        help='configuration file\nDefault : ~/.email-of-the-day/configuration.yml')

    parser.add_argument('csv',
                        nargs='?',
                        help='CSV file to parse the email content\n')

    return parser.parse_args()


def send(email_settings, body):
     
    subject = email_settings['email']['subject']
    sender_email = email_settings['email']['sender_email']
    receiver_email = email_settings['email']['receiver_email']
    cred = email_settings['email']['password']

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = email_settings['email']['sender_from']
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()
    
    ## Log in to server using secure context and send email
    context = ssl.create_default_context()
    # smtp_server.starttls(context)
    with smtplib.SMTP_SSL(email_settings['email']['mail_server_address'], email_settings['email']['mail_server_port'], context=context) as server:
        server.login(sender_email, cred)
        server.sendmail(sender_email, receiver_email, text)


def main():
    """ Main entry point of the app """

    args = arg_parse()

    config = yaml.safe_load(open(os.path.expanduser(args.config)))
    # print(config)

    Ymd = datetime.datetime.now().strftime('%Y%m%d')
    with open(args.csv,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['date'] == Ymd:
                config['email']['subject'] = row['subject']
                send(config, row['description'])


if __name__ == "__main__":
    main()

