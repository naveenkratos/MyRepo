import smtplib,ssl
from prettytable import PrettyTable
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Mailer:

    def __init__(self,config):
        self.config = config

    def triggerMail(self,htmlTableData):

        my_message = htmlTableData

        html = """\
        <html>
            <head>
            <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 5px;
                    text-align: left;    
                }    
            </style>
            </head>
        <body>
        <p>
        Mail Generated Using Python<br>
        </p>

        <p>
        Project Code is in my repo. <br> click Below Link <br>
        https://github.com/naveenkratos/OptivInterviewProject <br>
        </p>

        <p>VirusTotal results:<br>
        <br>
        %s
        <br>
        <br>
        </p>

        <p>
        AbuseIPDB result excel attached Below<br>
        </p>
        </body>
        </html>
        """ % (my_message)

        htmlPart = MIMEText(html, 'html')
        attachmentPart = MIMEBase('application', "octet-stream")

        attachmentPart.set_payload(open("abuseipdb_xlsx.xlsx", "rb").read())
        encoders.encode_base64(attachmentPart)
        attachmentPart.add_header('Content-Disposition', 'attachment; filename="abuseipdb_xlsx.xlsx"')

        sendFrom = self.config.SENDER_MAIL_ID
        sendFromPasswd = input("Enter Gmail Password:")
        sendTo = self.config.RECEIVER_MAIL_ID

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Optiv Project Interview - Project Data'
        msg['From'] = sendFrom
        msg['To'] = sendTo
        msg.attach(htmlPart)
        msg.attach(attachmentPart)

        with smtplib.SMTP('smtp.gmail.com',587) as smtpServer:
            smtpServer.ehlo()

            smtpServer.starttls()

            smtpServer.login(sendFrom, sendFromPasswd)
            smtpServer.sendmail(sendFrom, sendTo, msg.as_string())

        print("Mail Sended")

# mailer= Mailer(config)
# mailer.trigger_email()