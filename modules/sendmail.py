#!/usr/bin/env python

import subprocess
import requests
import time

class stackdriver_sendmail(object):

  def __init__(self):
    self.get_mailqueue()

  def get_instance_id(self):
		resp = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
		return resp.content

  def get_mailqueue(self):
    p1 = subprocess.Popen("/usr/bin/mailq", shell=True, stdout=subprocess.PIPE)
    p2 = subprocess.Popen("grep Total", shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen("cut -d: -f2", shell=True, stdin=p2.stdout, stdout=subprocess.PIPE)
    data = 0
    for values in p3.stdout:
      data = int(values.lstrip().rstrip()) + data

    data_point = {
      'name': 'Mail Queue Size',
      'value': int(data),
      'collected_at': int(time.time()),
      'instance': self.get_instance_id(),
    }

    print data_point

stackdriver_sendmail()
