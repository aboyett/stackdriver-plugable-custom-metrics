# Stackdriver Pluggable Custom Metrics

This is a pluggable system for [Stackdriver](http://www.stackdriver.com) to handle custom metrics.

## Requirements
I've tried to keep the requirements fairly light, you need Python 2.6 installed on a Linux machine and Factor. 
It's also assumed that you're on Amazon Web Services.

## Usage
`stackdriver.py --key <YOUR API KEY>`

## How it works
stackdriver.py will execute files in the ./modules/ directory and will attempt to send
the resulting output of those files to Stackdriver.

This is nice because it does it in one bulk update instead of sending multiple single updates.

## Your custom modules
I've included a sendmail.py example however you can create a module in whatever language you'd like,
even shell scripts. It just needs to output (to stdout) a JSON encoded string that includes the 
following fields:
'instance': 
'name': 
'value': 
'collected_at':

Example:
`{'instance': 'i-18bc2e2c', 'name': 'Mail Queue Size', 'value': 0, 'collected_at': 1379719066}`
