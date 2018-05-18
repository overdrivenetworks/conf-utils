#!/usr/bin/env python3
"""
MOTD Generator for OVERdrive-IRC.
"""

# Configuration values
default_location = 'Earth'
dbname = 'motd.db'

import re
import sys
import json

try:
    with open(dbname) as f:
        db = json.load(f)
except OSError:
    db = {}
print('Retrived DB from %s' % dbname)
print()

def gethostname(server):
    try:  # Try to get server hostname from the serverinfo.conf
        with open('%s.serverinfo.conf' % server) as f:
            data = f.read()
            sname = re.search(r'\<server name="(.+?)"', data)
            sname = sname.group(1)
    except (OSError, AttributeError):
        # If that fails, fall back to asking for hostname interactively!
        sname = input("What is the hostname of this server? ")
    return sname

def makemotd(server):
    fname = '%s.motd' % server
    print("Output path set to %s" % fname)
    
    # Prepare all our input fields.
    serverkey = db.get(server, {})
    if serverkey:
        print('Got existing serverdata: %s' % serverkey)
    args = {'servername': gethostname(server),
            'location': serverkey.get('location') or input("Where is this server located? ").strip() or default_location}
    db[server] = args
    
    try:
        # Read our MOTD template.
        with open('motd.template') as f:
            motd_template = f.read()
    except OSError:
        print('Error: failed to read motd.template!')
        sys.exit(1)
    else:
        # Write the expanded text to servername.motd.
        with open(fname, 'w') as outf:
            text = motd_template % args
            
            # Unescape escaped characters (e.g. IRC bold \x02)
            text = text.encode("utf-8").decode("unicode_escape")
            
            outf.write(text)
            print("Output file %s written." % fname)
            print()

if __name__ == '__main__':
    # Iterate over command line arguments (each is a server name)
    for sname in sys.argv[1:]:
        makemotd(sname)

    print('Writing DB to %s' % dbname)
    with open(dbname, 'w') as f:
        json.dump(db, f)
