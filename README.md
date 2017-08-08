# conf-utils
A collection of IRCd configuration management tools used by OVERdrive-IRC.

## conf-sync (scripts/sync.sh, scripts/sync-motd.sh)
conf-sync is an SCP-based IRCd configuration syncer used by the OVERdrive-IRC network.
It currently targets InspIRCd 2.0.x, but can theoretically support any IRCd using a file-based configuration.

### Instructions
First, configure your instance by renaming `scripts/config.sh.example` to `scripts/config.sh`.

Configuration files go in the root directory of the repository. By default, the following files
are merged in this order as `~/inspircd/run/conf/inspircd.conf` on target servers:

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

Once you're done changing things, run `scripts/sync.sh` to push your changes.
You will have to run rehash your servers manually after for them to take effect.
MOTD syncing is done via `scripts/sync-motd.sh`, which will write `<servername>.motd`
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
