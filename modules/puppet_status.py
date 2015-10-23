#!/usr/bin/env python

import subprocess
import requests
import time


class StackdriverPuppetStatus(object):

    def __init__(self):
        self.get_puppet_status()

    def get_instance_id(self):
        resp = requests.get(
            'http://169.254.169.254/latest/meta-data/instance-id')
        return resp.content

    def get_puppet_status(self):
        proc1 = subprocess.Popen("/sbin/service puppet status",
                                 shell=True, stdout=subprocess.PIPE)
        status = proc1.wait()
        if status == 127:
            proc1 = subprocess.Popen(
                "/usr/sbin/service puppet status", shell=True, stdout=subprocess.PIPE)
            status = proc1.wait()

        data_point = {
            'name': 'Puppet Status',
            'value': status,
            'collected_at': int(time.time()),
            'instance': self.get_instance_id(),
        }

        print data_point

if __name__ == '__main__':
    StackdriverPuppetStatus()
