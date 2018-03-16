#!/usr/bin/env python3

# You should configure this string to be whatever your IRCd names end with.
serversuffix = "overdrivenetworks.com"

import os
import sys
import itertools
import re
import socket
import ipaddress

import passwd

servers = sys.argv[1:]
curdir = os.path.dirname(os.path.abspath(__file__))

DEFAULT_TLS_METHOD = 'gnutls'
def _get_tls_mech(server):
    try:
        with open('%s.modules.conf' % server) as f:
            modulesdata = f.read()
    except OSError:
        print("warn: %s.modules.conf missing! Falling back to using 'gnutls' for links." % server)
        return DEFAULT_TLS_METHOD

    if 'm_ssl_openssl' in modulesdata:
        print("debug: using ssl='openssl' for %s" % server)
        return 'openssl'
    elif 'm_ssl_gnutls' in modulesdata:
        print("debug: using ssl='gnutls' for %s" % server)
        return 'gnutls'
    else:
        print("warn: Failed to detect either 'openssl' or 'gnutls' for encryption. Falling back to 'gnutls'")
        return DEFAULT_TLS_METHOD

def getip(server):
    # Try to grab the hostname and IP of the server from the relevant xyz.serverinfo.conf.
    try:
        with open('%s.serverinfo.conf' % server) as f:
            data = f.read()
    except OSError:
        print("debug: %s.serverinfo.conf missing!" % server)
        data = ''

    real_hostname = '%s.%s' % (server, serversuffix)

    hostname = real_hostname
    try:
        # In this case, we only want what looks like IPv4 addresses.
        hostname = re.search(r'\<server name="(.+?)"', data)
        hostname = hostname.group(1)
        print("debug: hostname for %s found: %s" % (server, hostname))
    except AttributeError:
        # Couldn't read the serverinfo.conf file, try resolving the hostname instead.
        print("debug: Failed to find hostname for %s, using default value of %s instead..." % (server, real_hostname))

    try:  # Ditto with the IP address.
        bind = re.search(r'\<bind address="([0-9\.]+)"', data)
        ip = bind.group(1)
        print("debug: IP for %s found: %s" % (server, ip))
    except AttributeError:
        # That didn't work (probably because we're using a wildcard bind for the server)
        # So, try resolving one of that two hostnames we found.
        try:
            ip = socket.gethostbyname(hostname)
        except socket.error:
            try:
                # Also try the server's hostname instead of the IRCd name (this won't work for closed hub servers)
                ip = socket.gethostbyname(real_hostname)
            except socket.error:
                # Fallback to asking for input if nothing works.
                while True:
                    try:
                        ip = input('Failed to get the server IP for server [%s]; type in the IP manually: ' % server)
                        ipaddress.ip_address(ip)
                    except ValueError:
                        print('Invalid IP address!')
                    except KeyboardInterrupt:
                        print('Aborted.')
                        sys.exit(3)
                    else:
                        break
            else:
                print("debug: IP for %s found (by resolving hostname %s): %s" % (server, real_hostname, ip))
        else:
            print("debug: IP for %s found (by resolving hostname %s): %s" % (server, hostname, ip))
    return (ip, hostname)

def linkblock(targetserver, password, sourceserver):
    s = """
<link name="{hostname}"
    ipaddr="{serverip}"
    allowmask="{serverip}"
    port="7001"
    timeout="300"
    ssl="{tls_method}"
    statshidden="no"
    hidden="no"
    sendpass="{password}"
    recvpass="{password}">
""".format(password=password, hostname=serverips[targetserver][1], serverip=serverips[targetserver][0],
           tls_method=_get_tls_mech(sourceserver))
    return s


if not servers:
    print('Error: No servers specified!')
    p = os.path.basename(__file__)
    print('%s is a quick script to generate link blocks between servers.' % p)
    print('usage: %s <server1> <server2> [<server3> ...]' % p)
    sys.exit(1)

serverips = {}
for server in map(str.lower, servers):
    if not os.path.isfile('%s.links.conf' % server):
        print('Error: No such config file %s.links.conf' % server)
        sys.exit(2)
    serverips[server] = getip(server)

if __name__ == '__main__':
    print("Server IP index: %s" % serverips)
    print()
    for serverpair in itertools.combinations(servers, 2):
        source, target = serverpair
        password = passwd.passwd(50)
        print('Adding to %s.links.conf:' % source)
        L = linkblock(target, password, source)
        print(L)
        with open('%s.links.conf' % source, 'a') as f:
            f.write(L)

        # Add the reverse too.
        print('Adding to %s.links.conf:' % target)
        L = linkblock(source, password, target)
        print(L)
        with open('%s.links.conf' % target, 'a') as f:
            f.write(L)
