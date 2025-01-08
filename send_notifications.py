import platform
import apprise
from config import Config


class Notification:

    def __init__(self, message, botname) -> None:
        self.message = message
        self.botname = botname
        self.apobj = apprise.Apprise()

    def send_push(self, pushover_user_key, pushover_api_key) -> None:
        # Setup push notification parameters. Must get new API from Pushover for every app.
        self.pushover_user_key = pushover_user_key
        self.pushover_api_key = pushover_api_key
        self.apobj.add(
            f"pover://{pushover_user_key}@{pushover_api_key}/iphone", tag="push"
        )
        self.apobj.notify(
            body=self.message, title=self.botname, body_format="text", tag="push"
        )

    # TODO Fix sms function
    # def send_sms(self, api, user) -> None:
    #     # Set sms notification paramebers
    #     self.api = api
    #     self. user = user
    #     self.apobj.add()
    #     self.apobj.notify(body = self.message, title = self.botname, body_format= "text",
    #     tag = "sms")

    def send_email(self, sendgrid_api_key, from_email, to_email) -> None:
        # Setup email notifcation parameters
        self.sendgrid_api_key = sendgrid_api_key
        self.from_email = from_email
        self.to_email = to_email
        self.apobj.add(
            f"sendgrid://{sendgrid_api_key}:{from_email}/{to_email}", tag="email"
        )
        self.apobj.notify(
            body=self.message, title=self.botname, body_format="text", tag="email"
        )

    def send_desktop(self) -> None:
        # Get system/OS name
        os_platform = platform.system()
        if os_platform.lower() == "windows":
            self.apobj.add("windows://", tag="desktop")
        elif os_platform.lower() == "linux":
            self.apobj.add("dbus://", tag="desktop")
        else:
            os_platform.lower() == "darwin"
            self.apobj.add("macosx://", tag="desktop")
        self.apobj.notify(
            body=self.message, title=self.botname, body_format="text", tag="desktop"
        )

    def send_all_channels(self):
        # Blast notifcation on all channels
        self.apobj.notify(
            body=self.message, title=self.botname, body_format="text", tag="all"
        )
