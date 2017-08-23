from gmail_handler.connect_and_extract import GmailConnection
from gmail_handler.inbox_to_sql import InboxToSQL

contact = GmailConnection()
contact.connect()
user = input("Username: \n")
pswrd = input("Password: \n")
contact.login(user, pswrd)
fileName = input("Please type in a file name (e.g. myDB.db): \n")
trialDB = InboxToSQL(fileName, contact)
trialDB.create_sql_table()
trialDB.insertByQuery()
contact.logout()

