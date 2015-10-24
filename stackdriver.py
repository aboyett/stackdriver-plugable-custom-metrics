#!/usr/bin/env python

import requests
import json
import time
import subprocess
import os
import argparse
import re


class MetricReporter(object):
    FAILED_MODULE_METRIC = "stackdriver.failed_modules"

    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = check_for_config()

        self.failed_modules = 0
        datapoints = []

        pwd = os.path.dirname(os.path.abspath(__file__))
        for root, _, files in os.walk(pwd + '/modules'):
            for module in files:
                process = subprocess.Popen(os.path.join(
                    root, module), shell=True, stdout=subprocess.PIPE)
                data = process.stdout.read().rstrip()
                try:
                    jsondata = json.loads(data)
                    datapoints.append(jsondata)
                except ValueError:
                    print "Failed to parse output from {module}".format(module=module)
                    self.failed_modules += 1
        datapoints.append(create_datapoint(self.FAILED_MODULE_METRIC, self.failed_modules))
        self.send_metric(datapoints)

    def send_metric(self, data):
        epoch = int(time.time())
        headers = {
            'content-type': 'application/json',
            'x-stackdriver-apikey': self.api_key
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

def check_for_config():
    """
    parse the stackdriver-extractor config file if it exists (this exists on both .deb and .rpm
    distros) and if it doesn't exist for whatever reason, try to parse stackdriver sysconfig file.
    """
    api_key = None

    extractor_loc = "/opt/stackdriver/extractor/etc/extractor.conf"
    sysconfig_loc = "/etc/sysconfig/stackdriver"

    if os.path.exists(extractor_loc):
        with open(extractor_loc) as cfg:
            expr = re.compile("^apikey=")
            _, _, api_key = filter(expr.search, cfg.readlines())[0].partition('=').strip()
    elif os.path.exists(sysconfig_loc):
        with open(sysconfig_loc) as cfg:
            for line in cfg:
                if re.match('STACKDRIVER_API_KEY', line):
                    _, _, val = line.partition("=")
                    api_key = re.sub(r'^"|"$', '', val).rstrip()

    if not api_key:
        raise RuntimeError("Cannot locate a Stackdriver API key, please provide one.")

    return api_key


def create_datapoint(name, value, include_id=True, instance_id=None, collected_at=None):
    """
    creates a datapoint with the values of name, value, instance_id and collected_at
    if include_id is False the datapoint will lack the instance_id field
    if instance_id is not specified it will be set to the EC2 instance id of the local machine
    collected_at should be the epoch time of data collection (seconds since 1970-01-01 00:00 UTC)
    if collected_at is not specified it will be set to the current time
    """
    datapoint = {}
    datapoint['name'] = name
    datapoint['value'] = value

    datapoint['collected_at'] = collected_at if collected_at is not None else int(time.time())

    if include_id:
        if instance_id is None:
            datapoint['instance_id'] = get_ec2_instance_id()
        else:
            datapoint['instance_id'] = instance_id

    return json.dumps(datapoint)

def get_ec2_instance_id():
    ec2_metadata_id_url = 'http://169.254.169.254/latest/meta-data/instance-id'

    try:
        ec2_id = requests.get(ec2_metadata_id_url).text
    except requests.exceptions.ConnectionError:
        # assume we aren't running in EC2 if we can't connect to metadata server
        ec2_id = None

    return ec2_id

def main():
    parser = argparse.ArgumentParser(
        description='Stackdriver Custom Metrics')
    parser.add_argument('--key', help='stackdriver api key', nargs='?')
    args = parser.parse_args()

    if args.key:
        api_key = args.key
    else:
        api_key = None
    MetricReporter(api_key=api_key)

if __name__ == '__main__':
    main()
