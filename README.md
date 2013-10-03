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

### Note
I am in no way affiliated with Stackdriver. Also this software has no warranty and may very well 
make your system catch on fire, explode and destroy the fabric of the universe.

## License

Stackdriver Pluggable Custom Metrics is licensed under a standard 3-clause BSD license.

Copyright (c) 2013, David Kerr All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of the author nor the names of contributors may be used to endorse or promote products derived from this software without specific prior written permission.

*THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.*
