################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

import ceploy.provider.google

class Cloud:
    providerName = 'google'
    def __init__(self, providerName='google'):
        self.providerName = providerName

    def send_email(subject, msg):
        fromaddr = 'tq.autosender@gmail.com'
        toaddrs = 'qadah.thamir@gmail.com'
        rmsg = "\r\n".join([
            "From: tq.autosender@gmail.com",
            "To: qadah.thamir@gmail.com",
            "Subject: {}".format(subject),
            "",
            msg
        ])
        username = secrets['uname']
        password = secrets['password']
        server = smtplib.SMTP(secrets['smtp_server_uri'])
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, rmsg)
        server.quit()


