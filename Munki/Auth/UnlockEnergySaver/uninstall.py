#!/usr/bin/env python

import subprocess
import sys
import plistlib

# Set the group back to admin
group = 'admin'

command = ['/usr/bin/security', 'authorizationdb', 'read', 'system.preferences.energysaver']

task = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = task.communicate()
formatted = plistlib.readPlistFromString(out)

# If the group doesn't match, we're going to correct it.
if formatted['group'] != group:
    formatted['group'] = group
    # Convert back to plist
    input_plist = plistlib.writePlistToString(formatted)
    # Write the plist back to the authorizationdb
    command = ['/usr/bin/security', 'authorizationdb', 'write', 'system.preferences.energysaver']
    task = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = task.communicate(input=input_plist)