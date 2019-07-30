# conf-utils
A collection of IRCd configuration management tools used by OVERdrive-IRC.

## certpush [beta]

Certpush is a utility that generates Let's Encrypt TLS certificates for IRC servers. It uses rootless certbot with DNS validation as its backend, creating a unique certificate for every server. Each certificate is only valid for that server's name(s) plus configured round robin addresses, allowing granular certificate revocation / removal compared to sharing certificates between servers.

Certpush uses the same scp-syncing mechanism as conf-sync below, and shares some config elements with it (target server addresses and paths).

An example configuration lives in `certpush/certpush.config.sh.example`.

```
$ ./certpush.sh
Usage:
./certpush.sh newserver [server name] - generates a certificate for the given server
./certpush.sh renew - renews all known certificate and pushes them to servers
./certpush.sh push [server name] - pushes the certificate for the given server via SFTP
./certpush.sh runcmd [command] [args] - run arbitrary certbot commands under certpush's config directories
```

[beta] `certpush.sh renew` can be safely crontabbed to ensure that certificates are kept up to date.

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
