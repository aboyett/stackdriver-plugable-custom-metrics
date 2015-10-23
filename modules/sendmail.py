#!/usr/bin/env python

import subprocess
import requests
import time


class StackdriverSendmail(object):

    def __init__(self):
        self.get_mailqueue()

    def get_instance_id(self):
        resp = requests.get(
            'http://169.254.169.254/latest/meta-data/instance-id')
        return resp.content

    def get_mailqueue(self):
        proc1 = subprocess.Popen("/usr/bin/mailq", shell=True,
                                 stdout=subprocess.PIPE)
        proc2 = subprocess.Popen("grep Total", shell=True,
                                 stdin=proc1.stdout, stdout=subprocess.PIPE)
        proc3 = subprocess.Popen("cut -d: -f2", shell=True,
                                 stdin=proc2.stdout, stdout=subprocess.PIPE)
        data = 0
        for values in proc3.stdout:
            data = int(values.lstrip().rstrip()) + data

        data_point = {
            'name': 'Mail Queue Size',
            'value': int(data),
            'collected_at': int(time.time()),
            'instance': self.get_instance_id(),
        }

        print data_point

StackdriverSendmail()
