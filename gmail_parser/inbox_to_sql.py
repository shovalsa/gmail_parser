import sqlite3
from gmail_parser.connect_and_extract import GmailConnection

class InboxToSQL():
    def __init__(self, dbName, inbox):
        self.dbName = dbName
        self.inbox = inbox.parsed_inbox() # a GmailConnection object
        self.fields = ["uid", "date_sent", "sender", "subject", "body", "html"]

    def create_sql_table(self):
        """
        Initializes SQL file with table 'messages' that contains the following fileds:
        uid, sent_at, receiver, sender, subject, body
        :param dbName: name of the db file e.g. "newFile.db"
        :return:
        """
        sqlFields = {"uid": "INTEGER PRIMARY KEY",
                "date_sent": "TIMESTAMP",
                "sender": "VARCHAR(254)",
                "subject": "VARCHAR(150)",
                "body": "NVARCHAR(1000)",
                "html": "NVARCHAR(1000)"}
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()
        fields_string = ""
        for k,v in sqlFields.items(): #
            fields_string += "%s %s,"%(k,v)
        creation_command = """
        CREATE TABLE message (%s
        );"""%(fields_string[:-1]) # output: CREATE TABLE message (uid INTEGER PRIMARY KEY, sent_at TIMESTAMP, ...);
        try:
            cursor.execute(creation_command)
        except sqlite3.OperationalError:
            print("Either db file already exists or error in command: \n", creation_command)
        connection.commit() #this saves the changes.
        cursor.close()
        connection.close()


    def insertByQuery(self, field=None, value=''):
        """
        If you only want to insert to the sql specific messages that correspond to certain parameters.
        If field and values are not given, the entire inbox is inserted.
        :param field: one of the following: date_sent, sender, subject, body, html
        :param value: the desired query, e.g. shovalsa@gmail.com
        :return:
        """
        query = []
        if value !='':
            for msg in self.inbox:
                if value in msg[field]:
                    query.append(msg)
        else:
            query = self.inbox
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()
        for emailDict in query:
            cursor.execute("SELECT uid FROM message")
            uids = cursor.fetchall()
            notUnique = []
            for uid in uids:
                notUnique.append(uid[0])
            table_fields = ""
            msg_values = "("

            if int(emailDict['uid']) not in notUnique:
                for k,v in emailDict.items():
                    table_fields += k+", "
                    msg_values += "\"%s\", "%v
                msg_values = msg_values[:-2]+");"
                sql_command = """INSERT INTO message (%s) VALUES"""%(table_fields[:-2])+ msg_values
                try:
                    cursor.execute(sql_command)
                except sqlite3.OperationalError:
                    print("sql command: ", sql_command)

        connection.commit() #this saves the changes.
        connection.close()

    def retrieveFromDB(self, field="*", value=None):
            """
            retrieves message(s) according to a certain query (not to confuse with the parent gmail query).
            :param field: the given field, stated as string, e.g. "message_id"
            :param value: the desired value within the field, given as it is saved in db (e.g. 4 for message_id,
            or "shoval@gmail.com" for "sender".
            :return: a 2D list of messages (where the items of the sublist are the values of each message).
            """
            connection = sqlite3.connect(self.dbName)
            cursor = connection.cursor()
            col = (field, )
            if value == None:
                cursor.execute("SELECT %s FROM message" %col) #for some reason the ? placeholder doesn't work
            else:
                general_command = "SELECT * FROM message WHERE %s="%(col)
                #If there's another character after %s (i.e. '=' in this case), is it still vulnerable to SQL injection?
                query = "\"%s\""%(value)
                general_command = general_command+str(query)+";"
                cursor.execute(general_command)
            result = cursor.fetchall()
            messages = []
            for r in result:
                messages.append(dict(zip(self.fields, r)))
            connection.close()
            return messages

    def createInboxDB(self, username, password):
        # self.inbox.connect()
        # self.inbox.login(username, password)
        self.create_sql_table()
        self.insertByQuery()
        self.inbox.logout()