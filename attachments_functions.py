import imaplib
import email
import json

# Connect to an IMAP server
def connect(server, user, password,folder):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select(folder)
    return m

# Download all attachment files for a given email
def downloaAttachmentsInEmail(m, emailid, outputdir):
    resp, data = m.fetch(bytes(emailid), '(BODY.PEEK[])')
    email_body = data[0][1]
    mail = email.message_from_string(email_body)
    if mail.get_content_maintype() != 'multipart':
        return
    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))

# Download all the attachment files for all emails in the inbox.
# def downloadAllAttachmentsInInbox(server, user, password, outputdir):
#     m = connect(server, user, password)
#     resp, items = m.search(None, "(ALL)")
#     items = items[0].split()
#     for emailid in items:
#         downloaAttachmentsInEmail(m, emailid, outputdir)




detach_dir = 'data_csvs' # directory where to save attachments (default: current)

# pwd = getpass.getpass("Enter your password: ")
with open("get_attachment_password.json") as ft:
    passwrd = json.load(ft)
userName = passwrd['user-name']
passwd = passwrd['get_attachments_pwd']
serverid = 'imap.gmail.com'


downloaAttachmentsInEmail(connect(serverid,userName,passwd,'"BILLING-REPORT"'),1,detach_dir)
