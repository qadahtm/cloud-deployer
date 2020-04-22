################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

import os
import subprocess
import smtplib
import threading
import json


# from termcolor import colored, cprint

class Utils:

    server_init = False

    def __init__(self, secrets_path='', from_addr='', to_addr=''):
        if secrets_path != '':
            with open(secrets_path) as data_file:
                self.secrets = json.load(data_file)
        else:
            self.secrets = {}

        self.from_addr = from_addr
        self.to_addr = to_addr

        self.server_init = False

    def __del__(self):
        if self.server_init:
            self.server.quit()


    def init_email_server(self):
        username = self.secrets['uname']
        password = self.secrets['password']
        # TODO(tq): de we need to login every time or once here is enough
        self.server = smtplib.SMTP(self.secrets['smtp_server_uri'])
        self.server.ehlo()
        self.server.starttls()
        self.server.login(username, password)

    def send_email(self, subject, msg):
        rmsg = "\r\n".join([
            "From: {}".format(self.to_addr),
            "To: {}".format(self.to_addr),
            "Subject: {}".format(subject),
            "",
            msg
        ])

        self.server.sendmail(self.from_addr, self.to_addr, rmsg)

    def exec_cmd(self, cmd, is_async=False):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=dict(os.environ))
        if not is_async:
            p.wait()
            print('Output:')
            for ol in p.stdout:
                print(ol.decode(encoding="utf-8", errors="strict"), end='')
            p.stdout.close()

            print('Error:')
            for el in p.stderr:
                print(el.decode(encoding="utf-8", errors="strict"), end='')
            p.stderr.close()

        return p

    def live_output(p):
        print("liveOutput for {}".format(str(p)))
        while p.poll() is None:
            print(p.stdout.readline().decode(encoding="utf-8", errors="strict"), end='')
        print(p.stdout.readline().decode(encoding="utf-8", errors="strict"), end='')

class expThread (threading.Thread):

    def __init__(self, node_idx, nip, rcmd, exp, verbose, secrets_path, from_addr, to_addr):
        threading.Thread.__init__(self)
        self.node_idx = node_idx
        self.rcmd = rcmd
        self.output = ''
        self.killed = False
        self.stdout = ''
        self.stderr = ''
        self.returncode = 0
        self.verbose = verbose
        self.utils = Utils(secrets_path, from_addr, to_addr)

    def run(self):
        p = self.utils.exec_cmd(self.rcmd, True)
        try:
            stdout, stderr = p.communicate(timeout=400)
            self.killed = False
        except subprocess.TimeoutExpired:
            self.kill_all_processes()
            stdout, stderr = p.communicate(timeout=10)
            self.killed = True

        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        self.output =  stdout + '\n\n' + stderr
        self.returncode = p.returncode


    def kill_all_processes(self, node_list):
        proc_list = []
        for nip in node_list:
            if self.verbose:
                print('sending command (kill all) to node: {}'.format(nip))
            rcmd = 'ssh -oStrictHostKeyChecking=no ubuntu@{} "{}"'.format(nip, 'pkill -9 rundb; pkill -9 runcl')
            proc_list.append(self.utils.exec_cmd(rcmd, True))
        self.utils.wait_for(proc_list)
        proc_list.clear()
        print('done (kill-all)!')