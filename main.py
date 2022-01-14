import email, smtplib, ssl, json, time
from fileinput import close

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from os import listdir, rename
from os.path import isfile, join
from json import dump, load
from helpers.checkIfDirectoryExists import checkAndCreateFolder
def determineEmailStatuses(data, filenames, status):
    for i in filenames:
        data[i] = status

    print(f'{status}!')
    

def send():
        data = {}
        source = '/Users/username/Desktop'
        destination = './sent'
        dataFile = 'data.json'
        checkAndCreateFolder(destination)
        files = [f for f in listdir(source) if isfile(join(source, f)) and '.png' in f]
        SENT = 'sent'
        FAILED = 'failed'
        if os.name == 'nt':
            files.remove('desktop.ini')    
        if isfile(dataFile):
            with open(dataFile, 'r') as openfile:
                try:
                    if openfile.readline:
                        data =  load(openfile)
                except:
                    pass 
            openfile.close()  
        # exit()

        subject = "Screenshot!!!"
        body = "See screenshots below"
        sender_email = "sender@example.com"
        receiver_email = "reciever@example.com"
        cc_email = "cc@example.com"
        password = 'your-password'
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = cc_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        for filename in files:
            if hasattr(data, filename) and data[filename] == SENT:
                continue
            # print(f'{source}/{filename}')
            # exit()
            with open(f'{source}/{filename}', "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

        try:

            if files:
                # Log in to server using secure context and send email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)
                    determineEmailStatuses(data, files, SENT)

                    for filename in files:
                        rename(f'{source}/{filename}',f'{destination}/{filename}')

        except:

            determineEmailStatuses(data, files, FAILED)
            
        finally:

            with open("data.json", "w") as outfile:
                dump(data, outfile)



while True:
    send()
    timer_length = 60 * 2
    time.sleep(timer_length)
