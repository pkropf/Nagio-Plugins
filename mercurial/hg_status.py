#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nagios plugin to check the status of a mercurial repository.

Copyright (c) 2011 Peter Kropf. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Sometimes you need to know when a mercurial directory tree has changes
that haven't been committed. This plugin will check the status and
return a warning if there are any changes that haven't been committed.

Example:

    ./hg_status.py /path/to/mercurial/repository
"""


import sys
import os
from optparse import OptionParser
import popen2


prefix = 'hg_status'

class nagios:
    ok       = (0, 'OK')
    warning  = (1, 'WARNING')
    critical = (2, 'CRITICAL')
    unknown  = (3, 'UNKNOWN')


def exit(status, message):
    print prefix + ' ' + status[1] + ' - ' + message
    sys.exit(status[0])


if len(sys.argv) < 2:
    exit(nagios.unknown, 'missing command line arguments')

repo = sys.argv[1]
r, w, e = popen2.popen3('hg status --cwd %s' % repo)
rchanges = r.readline()
echanges = e.readline()
r.close()
w.close()
e.close()

if len(echanges):
    exit(nagios.unknown, 'unknown mercurial status for: %s' % repo)

if len(rchanges) == 0:
    exit(nagios.ok, 'mercurial repository ok: %s' % repo)

elif len(rchanges) > 0:
    exit(nagios.warning, 'mercurial repository has changes: %s' % repo)
