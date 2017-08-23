"""
Somewhat based on: https://github.com/charlierguo/gmail
Still missing: encoding, actual parsing of data.
"""



import imaplib as imap
import email
from re import escape


class GmailConnection():
    GMAIL_IMAP_HOST = 'imap.gmail.com'
    GMAIL_IMAP_PORT = 993

    # GMail SMTP defaults
    GMAIL_SMTP_HOST = "smtp.gmail.com"
    GMAIL_SMTP_PORT = 587

    def __init__(self):
        self.username = None
        self.password = None
        self.access_token = None

        self.imap = None
        self.smtp = None
        self.logged_in = False

    def connect(self):
        self.imap = imap.IMAP4_SSL(self.GMAIL_IMAP_HOST, self.GMAIL_IMAP_PORT)
        return self.imap

    def login(self, username, password):
        self.username = username
        self.password = password

        if not self.imap:
            self.connect()

        try:
            imap_login = self.imap.login(self.username, self.password)
            self.logged_in = (imap_login and imap_login[0] == 'OK')
            print("successfully logged in.")
        except imap.IMAP4.error:
            raise("Gmail Authentication failed.")

    def logout(self):
        self.imap.close()
        self.imap.logout()
        self.logged_in = False
        print("successfully logged out")

    def get_inbox(self):
        inbox = self.imap.select()[1][0]
        print("inbox: ", int(inbox)) #returns no. of messages in inbox

    def fetch_messages(self):
        self.imap.select('INBOX')
        result, data = self.imap.uid('search', None, "ALL")
        # print(data)
        if result == 'OK':
            self.messages = []
            for num in data[0].split():
                result, data = self.imap.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    raw_message = email.message_from_bytes(data[0][1])    # raw email text including headers
                    self.messages.append([int(num), raw_message])
        return self.messages

    def parsed_inbox(self):
        self.parsed_messages = []
        messages = self.fetch_messages()
        fieldNames = ['uid', 'date_sent', 'sender', 'subject', 'body', 'html']
        for msg in messages:
            attsList = []
            attsList.append((fieldNames[0], msg[0])) #uid
            attsList.append((fieldNames[1], msg[1]['Date'])) #date_sent
            attsList.append((fieldNames[2], msg[1]['From'])) #sender
            attsList.append((fieldNames[3], msg[1]['Subject'])) #sender
            body = None
            html = None
            if msg[1].get_content_maintype() == "multipart":
                for content in msg[1].walk():
                    if content.get_content_type() == "text/plain":
                        body = content.get_payload()
                    elif content.get_content_type() == "text/html":
                        html = content.get_payload()
            elif msg[1].get_content_maintype() == "text":
                body = msg[1].get_payload()
                html = 'NA'
            attsList.append((fieldNames[4], body))
            attsList.append((fieldNames[5], html.replace("\"","***")))
            # dict(attsList)
        # for the moment without attachments


            self.parsed_messages.append(dict(attsList))
        return self.parsed_messages


