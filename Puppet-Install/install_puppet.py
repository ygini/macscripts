#!/usr/bin/env python

import urllib2
from tempfile import mkstemp
from shutil import move, rmtree
from os import remove, close, path, rename, umask
import subprocess
import math

def downloadChunks(url):
    """Helper to download large files
        the only arg is a url
       this file will go to a temp directory
       the file will also be downloaded
       in chunks and print out how much remains
    """

    baseFile = path.basename(url)

    #move the file to a more uniq path
    umask(0002)

    try:
        temp_path='/tmp'
        file = path.join(temp_path,baseFile)

        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                print math.floor( (downloaded / total_size) * 100 )
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:",e.code , url
        return False
    except urllib2.URLError, e:
        print "URL Error:",e.reason , url
        return False

    return file

def internet_on():
    try:
        response=urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
    
if internet_on:
    if path.isdir('/var/lib/puppet'):
        print "Binning old Puppet installation"
        rmtree('/var/lib/puppet')
    if path.isdir('/etc/puppet'):
        rmtree('/etc/puppet')
    print "Downloading Facter"
    the_dmg = downloadChunks("http://downloads.puppetlabs.com/mac/facter-1.6.17.dmg")
    print "Mounting Facter DMG"
    the_command = "/usr/bin/hdiutil attach "+the_dmg
    p=subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    time.sleep(10)
    #install it
    print "Installing Facter"
    the_command = "/usr/sbin/installer -pkg /Volumes/facter-1.6.17/facter-1.6.17.pkg -target /"
    p=subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    time.sleep(20)
    print "Downloading Puppet"
    the_dmg = downloadChunks("http://downloads.puppetlabs.com/mac/puppet-3.0.2.dmg")
    ##mount the dmg
    print "Mounting Puppet DMG"
    the_command = "/usr/bin/hdiutil attach "+the_dmg
    p=subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    time.sleep(10)
    print "Installing Puppet"
    the_command = "/usr/sbin/installer -pkg /Volumes/puppet-3.0.2/puppet-3.0.2.pkg -target /"
    p=subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    time.sleep(20)
    print "Ejecting Puppet"
    the_command = "hdiutil eject /Volumes/puppet-3.0.2"
    subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
    
    print "Ejecting Facter"
    the_command = "hdiutil eject /Volumes/facter-1.6.17"
    subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
    
    print "All done!"