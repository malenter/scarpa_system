
import smtplib
from  crm import settings
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print( mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        print('conectando...')
        mensaje = MIMEText('TIENES UN MENSAJE DE XD')
        mensaje['From']=settings.EMAIL_HOST_USER
        mensaje['To']="jsanabria527@unab.edu.co"
        mensaje['Subject']="Tienes un correo"
           
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                "jsanabria527@unab.edu.co",
                mensaje.as_string())
        print('correo enviado correcto')

    except Exception as e:
        print(e)   
    
send_email()    