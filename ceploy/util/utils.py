################################
# Copyright 2020
# Author: Thamir M. Qadah
################################

import glob
import os
import sys
import socket
import re
import shlex, subprocess
import smtplib
import shutil
import pprint
import threading
import json
import time
from datetime import timedelta
import multiprocessing

# from termcolor import colored, cprint
import ceploy.constants

class Utils:

    def __init__(self, secrets_path, from_addr, to_addr):
        with open(secrets_path) as data_file:
            self.secrets = json.load(data_file)

        self.from_addr = from_addr
        self.to_addr = to_addr

        username = self.secrets['uname']
        password = self.secrets['password']

        # TODO(tq): de we need to login every time or once here is enough
        self.server = smtplib.SMTP(self.secrets['smtp_server_uri'])
        self.server.ehlo()
        self.server.starttls()
        self.server.login(username, password)

    def __del__(self):
        self.server.quit()

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
            print('Error:')
            for el in p.stderr:
                print(el.decode(encoding="utf-8", errors="strict"), end='')
        return p

    def live_output(p):
        print("liveOutput for {}".format(str(p)))
        while p.poll() is None:
            print(p.stdout.readline().decode(encoding="utf-8", errors="strict"), end='')
        print(p.stdout.readline().decode(encoding="utf-8", errors="strict"), end='')

    def wait_for(plist, expds=None, outputFlag=False, liveOutput=False, live_output_node_idx=0):
        if liveOutput:
            live_output(plist[live_output_node_idx]);
        # done observing live output if enabled
        failed = False
        output = ''
        for i, p in enumerate(plist):
            if p:
                if verbose:
                    print("Waiting for node {} at {}".format(i, node_list[i]))
                try:
                    stdout, stderr = p.communicate(timeout=400)
                    killed = False
                except subprocess.TimeoutExpired:
                    kill_all_processes()
                    stdout, stderr = p.communicate(timeout=10)
                    killed = True

                stdout = stdout.decode('utf-8')
                stderr = stderr.decode('utf-8')
                output = output + '\n\n' + stdout + '\n\n' + stderr

                if p.returncode != 0 or killed:
                    error_s = 'Node[{}] at {} '.format(i, node_list[i])
                    if expds:
                        error_s = error_s + ('failed to run exp for %s (status=%s, killed=%s)' % (
                        format_exp(expds), p.returncode, killed))
                    else:
                        error_s = error_s + (
                                    'failed to run remote command (status=%s, killed=%s)' % (p.returncode, killed))

                    print(COLOR_RED + error_s + COLOR_RESET)
                    failed = True

        if expds:
            filename = dir_name + '/' + gen_filename(expds)
            if failed:
                f_filename = filename + '.failed'
            else:
                f_filename = filename
            outf = open(f_filename, 'w')
            outf.write(output)

        elif outputFlag:
            print('Output of node: {}'.format(i))
            print(output)
            # for ol in p.stdout:
            # print(ol.decode(encoding="utf-8", errors="strict"), end='')
            print('----- End of output of node {} -----'.format(i))

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