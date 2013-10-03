#!/usr/bin/env python

import requests
import json
import time
import subprocess
import os
import ast
import argparse

class stackdriver(object):

  def __init__(self):
    parser = argparse.ArgumentParser(description='Stackdriver Custom Metrics')
    parser.add_argument('--key', help='stackdriver api key',nargs='?')
    args = parser.parse_args()

    timestamp = int(time.time())
    epoch = time.gmtime()
    datapoints = []
    pwd = os.path.dirname(__file__)
    for root, dirs, files in os.walk(pwd + '/modules'):
      for file in files:
        process = subprocess.Popen( os.path.join(root,file), shell=True, stdout=subprocess.PIPE)
        data = process.stdout.read().rstrip()
        datapoints.append(ast.literal_eval(data))
    self.send_metric(datapoints, args)

  def send_metric(self, data, args):
    headers = {
      'content-type': 'application/json',
      'x-stackdriver-apikey': args.key
    }
    gateway_msg = {
      'timestamp': int(time.time()),
      'proto_version': 1,
      'data': data,
    }
    resp = requests.post(
      'https://custom-gateway.stackdriver.com/v1/custom',
      data=json.dumps(gateway_msg),
      headers=headers)
    assert resp.ok, 'Failed to submit custom metric.'


stackdriver()

