import smtplib
import ssl


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    #Basic code to send and receive from the same email
    username = "cfgprojectqueries@gmail.com"
    password = "vknzegbybldhicxf"

    receiver = "cfgprojectqueries@gmail.com"


    context = ssl.create_default_context() #sending email securely

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username,password)
        #owner of the account
        server.sendmail(username, receiver, message)