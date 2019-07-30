# conf-utils
A collection of IRCd configuration management tools used by OVERdrive-IRC.

## conf-sync (scripts/sync.sh, scripts/sync-motd.sh)
conf-sync is a simple scp-based IRCd configuration manager.
It currently targets InspIRCd 2.0.x, but can theoretically support any IRCd using a file-based configuration.

### Instructions
First, configure your instance by renaming `scripts/config.sh.example` to `scripts/config.sh`.

Configuration files go in the root directory of the repository. By default, the following files
are merged in this order as `~/inspircd/run/conf/inspircd.conf` on target servers:

 * global.conf
 * `<servername>`.modules.conf
 * modules.conf
 * `<servername>`.links.conf
 * cgiirc.conf
 * globalbans.conf
 * `<servername>`.auth-ex.conf
 * auth-ex.conf
 * opers.conf
 * `<servername>`.serverinfo.conf
 * helpop.conf
 * alias.conf
 * dnsbl.conf
 * filter.conf

Once you're done changing things, run `scripts/sync.sh` to push your changes.
You will have to run rehash your servers manually for changes to take effect.
MOTD syncing is done via `scripts/sync-motd.sh`, which will write `<servername>.motd`
and `ircd.rules` in the target directory.

All scripts **require passwordless SSH access** for scp, so you will need to run
them from a machine that has SSH access to the target servers.

## makelink

**scripts/makelink.py** provides a link block generator between servers.
   - Usage: `scripts/makelink.py <server1> <server2> [<server3> ...]`

If `serverX.links.conf` and `serverX.links.conf` are both present (for each
server name specified), and the fields are in the InspIRCd XML format,
makelink will automatically write link blocks between the servers given.

## passwd

**scripts/passwd.py** provides a simple random password generator.
   - Usage: `scripts/passwd.py [<passwordlength>]`
   - If `<passwordlength>` is not specified, it defaults to 16.
