#!/usr/bin/env python3

# You should configure this string to be whatever your IRCd names end with.
serversuffix = "overdrivenetworks.com"

import os
import sys
import itertools
import re
import socket
import ipaddress
import string
import secrets  # py3.6+

servers = sys.argv[1:]
curdir = os.path.dirname(os.path.abspath(__file__))

def make_password(length):
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
    return password

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

IPV4_REGEX = r'\<bind address="([0-9\.]+)"'
IPV6_REGEX = r'\<bind address="([0-9a-f:]+)"'
def _get_ip_and_ircd_name(server, ipv6=False):
    """
    Fetches the IP address and IRCd hostname of a server and returns it in a tuple: (IP, hostname)
    """
    # Try to grab the hostname and IP of the server from the relevant xyz.serverinfo.conf.
    try:
        with open('%s.serverinfo.conf' % server) as f:
            data = f.read()
    except OSError:
        print("debug: %s.serverinfo.conf missing!" % server)
        data = ''

    real_hostname = '%s.%s' % (server, serversuffix)

    family = socket.AF_INET6 if ipv6 else socket.AF_INET

    hostname = real_hostname
    try:
        # Try to grab the server hostname
        hostname = re.search(r'\<server name="(.+?)"', data)
        hostname = hostname.group(1)
        print("debug: hostname for %s found: %s" % (server, hostname))
    except AttributeError:
        # Couldn't read the serverinfo.conf file, try resolving the hostname instead.
        print("debug: Failed to find hostname for %s, using default value of %s instead..." % (server, real_hostname))

    try:
        # Ditto with the IP address.
        bind = re.search(IPV6_REGEX if ipv6 else IPV4_REGEX, data)
        ip = bind.group(1)
        print("debug: IP for %s found: %s" % (server, ip))
    except AttributeError:
        # That didn't work (probably because we're using a wildcard bind for the server)
        # So, try resolving one of that two hostnames we found.
        try:
            ip = socket.getaddrinfo(hostname, None, family=family)[0][4][0]
        except (socket.error, IndexError):
            try:
                # Also try the server's hostname instead of the IRCd name (this won't work for closed hub servers)
                ip = socket.getaddrinfo(real_hostname, None, family=family)[0][4][0]
            except (socket.error, IndexError):
                # Fallback to asking for input if nothing works.
                while True:
                    try:
                        ip = input('Failed to get the server IP for server [%s]; type in the IPv%s address manually: ' % (server, '6' if ipv6 else '4'))
                        ipaddress.ip_address(ip)
                    except ValueError:
                        print('Invalid IP address!')
                    except KeyboardInterrupt:
                        print('Aborted.')
                        sys.exit(1)
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

serverips = {}

if __name__ == '__main__':
    print("Server IP index: %s" % serverips)
    print()

    import argparse
    parser = argparse.ArgumentParser(description='link block generator tool for InspIRCd 2.0')
    parser.add_argument('servers', help='specifies the server names to make a link block for', nargs='*')
    parser.add_argument("--ipv6", "-6", help="forces IPv6 for a link block", action='store_true')
    parser.add_argument("--override", "-o", help="forces the hostname and IP for a server to given values: "
                                                 "takes the form --serverip shortservername,IP.address,ircd.hostname",
                        action='append', default=[])
    args = parser.parse_args()

    if len(args.servers) < 2:
        print('ERROR: need at least two servers to create link blocks', file=sys.stderr)
        sys.exit(1)

    forced_serverips = {}
    for entry in args.override:
        servername, ip, host = entry.lower().split(',', 2)
        forced_serverips[servername] = (ip, host)
    if forced_serverips:
        print("Forcing the following IPs/hosts: %s" % forced_serverips)

    for server in map(str.lower, args.servers):
        if server in forced_serverips:
            serverips[server] = forced_serverips[server]
        else:
            if not os.path.isfile('%s.links.conf' % server):
                print('Error: No such config file %s.links.conf' % server)
                sys.exit(1)
            serverips[server] = _get_ip_and_ircd_name(server, ipv6=args.ipv6)

    for serverpair in itertools.combinations(args.servers, 2):
        source, target = serverpair
        password = make_password(50)
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
