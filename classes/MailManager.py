import smtplib
from email.message import EmailMessage
import ssl
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger('django')

class MailManager :

    #Private members
    __mail_error = None
    __msg = None
    __mail_sender = None
    __mail_server = None
    __mail_receiver = None
    __mail_subject = None
    __context = None

    def __init__(self):
        self.__msg = EmailMessage()
        self.__mail_sender = settings.MAIL_FROM
        self.__msg["From"] = self.__mail_sender
        self.__mail_server = None
        self.__mail_receiver = ""
        self.__mail_subject = ["FollowYourBarber - Création de votre compte.","FollowYourBarber - Confirmer votre compte."]
        self.__context = ssl.create_default_context()

    def set_mail_receiver(self,mail_receiver):
        self.__mail_receiver = mail_receiver
        if 'To' in self.__msg:
            self.__msg.replace_header('To', mail_receiver)
        else:
           self.__msg['To'] = mail_receiver

    def set_mail_subject(self,index):
        if 'Subject' in self.__msg:
            self.__msg.replace_header("Subject",self.__mail_subject[index])
        else:
            self.__msg["Subject"] = self.__mail_subject[index]

    def create_mail_server(self,smtpAddress,port):
        self.__mail_server = smtplib.SMTP_SSL(smtpAddress,port,context=self.__context)
        
    def login_into_mail_server(self,mail_login,mail_password):
        self.__mail_server.login(mail_login,mail_password)

    def send_mail(self):
        self.__mail_server.sendmail(self.__mail_sender,self.__mail_receiver,self.__msg.as_string())

    def set_mail_template(self,template):
       self.__msg.add_alternative(template, subtype = 'html')

    def send_verification_mail(self,firstname,user_mail):
        self.set_mail_receiver([user_mail])
        mail_template = render_to_string("email/mailConfirmation.html",{'FIRSTNAME': firstname})
        self.set_mail_template(mail_template)
        self.set_mail_subject(1)
        self.send_mail()

    def set_mail_error(self, error_message) :
        self.__mail_error = error_message

    def get_mail_error(self) :
        return self.__mail_error

mail_manager = MailManager()
try : 
    mail_manager.create_mail_server(settings.MAIL_SERVER,settings.MAIL_PORT)
    mail_manager.login_into_mail_server(settings.MAIL_USERNAME,settings.MAIL_PASSWORD)
except Exception as e:
    logger.error("An error occurred while creating mail server and login into mails in MailManager", exc_info=True)
