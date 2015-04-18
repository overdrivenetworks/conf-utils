OVERdrive-IRC Network Configuration
===================

SCP-based network configuration for the OVERdrive-IRC network. IRCd used is InspIRCd.

## Instructions

Here, the configuration files are split up in a way that makes editing 
slightly easier. Once you're done changing something, run `scripts/git-sync.sh`
to push your changes. You will have to run `/rehash *` after for them
to take effect.

The following files are merged in this order to form an `inspircd.conf` on the
target server:

 * global.conf
 * `<servername>`.links.conf
 * opers.conf
 * modules.conf
 * `<servername>`.serverinfo.conf
 * cgiirc.conf
 * auth-ex.conf
 * helpop.conf
 * alias.conf
 * dnsbl.conf

MOTD syncing is done via `scripts/motd.sh` (it will write `<servername>`.motd
and ircd.rules), and server addresses are stored in `scripts/config.sh`.

**Git viewers: rename `scripts/config.sh.example` to `scripts/config.sh` and
write your configuration there!**

All scripts **depend on automated/passwordless SSH logins**, so you will need to run
them from a machine that has SSH access to the target servers. Also, this **requires**
that the target servers have their IRCd configuration directory set to
**`~/inspircd/etc`** (yes, this strays from the default, so pay attention)!

## License

Copyright (c) 2014-2015 OVERdrive-IRC Development Team

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
