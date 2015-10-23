#!/usr/bin/env python

import requests
import json
import time
import subprocess
import os
import ast
import argparse
import re


class Stackdriver(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Stackdriver Custom Metrics')
        parser.add_argument('--key', help='stackdriver api key', nargs='?')
        args = parser.parse_args()

        datapoints = []
        pwd = os.path.dirname(os.path.abspath(__file__))
        for root, _, files in os.walk(pwd + '/modules'):
            for module in files:
                process = subprocess.Popen(os.path.join(
                    root, module), shell=True, stdout=subprocess.PIPE)
                data = process.stdout.read().rstrip()
                datapoints.append(ast.literal_eval(data))
        if not args.key:
            api_key = self.check_for_config()
        else:
            api_key = args.key
        self.send_metric(datapoints, api_key)

    def check_for_config(self):
        with open("/etc/sysconfig/stackdriver") as cfg:
            for line in cfg:
                if re.match('STACKDRIVER_API_KEY', line):
                    _, _, val = line.partition("=")
                    return re.sub(r'^"|"$', '', val).rstrip()

    def send_metric(self, data, key):
        epoch = int(time.time())
        headers = {
            'content-type': 'application/json',
            'x-stackdriver-apikey': key
        }
        gateway_msg = {
            'timestamp': epoch,
            'proto_version': 1,
            'data': data,
        }
        resp = requests.post(
            'https://custom-gateway.stackdriver.com/v1/custom',
            data=json.dumps(gateway_msg),
            headers=headers)
        assert resp.ok, 'Failed to submit custom metric.'

Stackdriver()
