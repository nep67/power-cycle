import smtplib, ssl, email
import socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(receiver_email, password, filename, body):
    smtp_server = "smtp.gmail.com" ##dont touch
    port = 587 ##dont touch
    subject = "Bicycle Application Requested Files..."##can be changed
    sender_email = "bicycle.email.bot@gmail.com"  ##bicycle.email.bot@gmail.com"
    connection = False
   
    message = MIMEMultipart()
    message["To"] = receiver_email
    message["From"] = sender_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    #make an array for multiple files
    try:
        socket.create_connection(("www.google.com", 80))
        connection = True
    except OSError:
        connection = False
    if (connection == True):
        ##make a loop for opening all files in the file array
        ##each of these lines is needed to attach the file,
        ##the loop must go through all these lines before repeating
        for i in range(len(filename)):
            try:
                attachment = open(filename[i], "rb")
            except OSError:
                return 0
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename[i])
            message.attach(part)

        text = message.as_string()
        context = ssl.create_default_context() #dont touch
        with smtplib.SMTP(smtp_server, port) as server: #dont touch
            server.starttls(context=context) #dont touch
            try:
                server.login(sender_email, password)
            except smtplib.SMTPAuthenticationError:
                print('Login failure: please reenter credential information.')
                return 1
                      
            server.sendmail(sender_email, receiver_email, text) ##dont touch
            server.quit() 
            
        print("Done!")
    else:
        print("There is no internet connection, files were safely stored")
        f = open("store.txt","a+")
        f.write(receiver_email)
        f.write("\n")
        for i in range(len(filename)):
            f.write(filename[i])
            f.write("\n")
        f.close()