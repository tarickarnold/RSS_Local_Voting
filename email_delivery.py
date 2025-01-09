import base64
import os
from mailjet_rest import Client
import sendgrid
from sendgrid.helpers.mail import (
    Content,
    Mail,
    Attachment,
    FileContent,
    FileType,
    FileName,
    Disposition,
)
from config import Config


class Sendgrid_email:

    def __init__(self, sendgrid_api_key) -> None:
        self.sendgrid_api_key = sendgrid_api_key
        self.client = sendgrid.SendGridAPIClient(sendgrid_api_key)

    def send_email(self, from_email, to_email, subject, content) -> None:
        self.from_email: any = from_email
        self.to_email: any = to_email
        self.subject: any = subject
        self.content: any = Content("text/html", content)
        mail = Mail(from_email, to_email, subject, content)
        response: any = self.client.send(mail)


class Mailjet_email:

    def __init__(self, mailjet_api_key, mailjet_api_secret):
        self.api_key = mailjet_api_key
        self.api_secret = mailjet_api_key
        self.mailjet = Client(
            auth=(mailjet_api_key, mailjet_api_secret), version="v3.1"
        )

    def send_email(self, from_email, to_email, subject, content):
        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.content = content

        data = {
            "Messages": [
                {
                    "From": {"Email": from_email, "Name": "bot_sender"},
                    "To": [{"Email": to_email, "Name": "recipeint"}],
                    "Subject": subject,
                    "TextPart": "Greetings from Mailjet!",
                    "HTMLPart": '<h3>Dear passenger 1, welcome to <a href="https://www.mailjet.com/">Mailjet</a>!</h3><br />May the delivery force be with you!',
                }
            ]
        }
        result = Client.send.create(data=data)

