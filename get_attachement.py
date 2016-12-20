import email, getpass, imaplib, os
import json

detach_dir = 'data_csvs/attachments' # directory where to save attachments (default: current)

# pwd = getpass.getpass("Enter your password: ")
with open("get_attachment_password.json") as ft:
    passwrd = json.load(ft)
userName = passwrd['user-name']
passwd = passwrd['get_attachments_pwd']
# connecting to the gmail imap server
# m = imaplib.IMAP4_SSL("imap.gmail.com")
# m.login(user,pwd)
# m.select("BILLING-REPORT") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes
try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print('Not able to sign in!')
        raise
    
    imapSession.select("BILLING-REPORT")
    # imapSession.select("[Gmail]/All Mail")

    # imapSession.select('Email alerts')
    typ, data = imapSession.search(None, 'ALL')

    if typ != 'OK':
        print('Error searching Inbox.')
        raise
    
    # Iterating over all emails
    for msgId in data[0].split():
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')

        if typ != 'OK':
            print('Error fetching mail.')
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_string(str(emailBody))
        for part in mail.walk():
            # if part.get_content_maintype() == 'multipart':
            #     print('parts')
            #     # print(part.as_string())
            #     continue
            # if part.get('Content-Disposition') is None:
            #     # print(part.as_string())
            #     print('content-disposition is none')
            #     continue
            fileName = part.get_filename()
            print(fileName)

            if fileName:
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                print(filePath)
                if not os.path.isfile(filePath) :
                    print(fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
except :
    print('Not able to download all attachments.')

# def downloaAttachmentsInEmail(m, emailid, outputdir):
#     resp, data = m.fetch(emailid, "(BODY.PEEK[])")
#     email_body = data[0][1]
#     mail = email.message_from_string(email_body)
#     if mail.get_content_maintype() != 'multipart':
#         return
#     for part in mail.walk():
#         if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
#             open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))