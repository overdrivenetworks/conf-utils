# conf-utils
A collection of IRCd configuration management tools used by OVERdrive-IRC.

## conf-sync (scripts/sync.sh, scripts/sync-motd.sh)
conf-sync is an SCP-based IRCd configuration syncer used by the OVERdrive-IRC network.
It currently targets InspIRCd 2.0.x, but can theoretically support any IRCd using a file-based configuration.

### Instructions
First, configure your instance by renaming `scripts/config.sh.example` to `scripts/config.sh`.

Configuration files go in the root directory of the repository. By default, the following files
are merged in this order as `~/inspircd/etc/inspircd.conf` on target servers
(yes, this strays from the default paths):

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

Once you're done changing things, run `scripts/git-sync.sh` to push your changes.
You will have to run rehash your servers manually after for them to take effect.
MOTD syncing is done via `scripts/motd.sh`, which will write `<servername>.motd`
and `ircd.rules` in the target directory.

All scripts **require passwordless SSH access**, so you will need to run
them from a machine that has SSH access to the target servers.

## makelink

**scripts/makelink.py** provides a link block generator between servers.
   - Usage: `scripts/makelink.py <server1> <server2> [<server3> ...]`

If `serverX.links.conf` and `serverX.links.conf` are both present (for each
server name specified), adn the fields are in the right format (InspIRCd XML),
makelink will automatically write link blocks between the servers chosen.

## passwd

**scripts/passwd.py** provides a simple random password generator.
   - Usage: `scripts/passwd.py [<passwordlength>]`
   - If `<passwordlength>` is not specified, it defaults to 16.

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
