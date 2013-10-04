#!/usr/bin/env python

import subprocess
import requests
import time

class stackdriver_puppet_status(object):

  def __init__(self):
    self.get_puppet_status()

  def get_instance_id(self):
    resp = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return resp.content

  def get_puppet_status(self):
    p1 = subprocess.Popen("/sbin/service puppet status", shell=True, stdout=subprocess.PIPE)
    status = p1.wait()

    data_point = {
      'name': 'Puppet Status',
      'value': status,
      'collected_at': int(time.time()),
      'instance': self.get_instance_id(),
    }

    print data_point

stackdriver_puppet_status()
