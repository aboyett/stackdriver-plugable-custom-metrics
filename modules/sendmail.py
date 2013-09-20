#!/usr/bin/env python

import subprocess

class stackdriver_sendmail(object):

  def __init__(self):
    self.get_mailqueue()

  def get_instance_id(self):
    p1 = subprocess.Popen("facter -p ec2_instance_id", shell=True, stdout=subprocess.PIPE)
    data = p1.stdout.read().rstrip().lstrip()
    return data

  def get_mailqueue(self):
    p1 = subprocess.Popen("/usr/bin/mailq", shell=True, stdout=subprocess.PIPE)
    p2 = subprocess.Popen("grep Total", shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen("cut -d: -f2", shell=True, stdin=p2.stdout, stdout=subprocess.PIPE)
    data = p3.stdout.read().rstrip().lstrip()

    data_point = {
      'name': 'Mail Queue Size',
      'value': int(data),
      'collected_at': int(time.time()),
      'instance': self.get_instance_id(),
    }

    print data_point

stackdriver_sendmail()
