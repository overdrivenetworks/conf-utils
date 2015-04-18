#!/bin/bash

# Grab our config
. scripts/config.sh

motdsync () {
	echo "Sync MOTD: $1.$serversuffix"
	scp ${options[$1]} $1.motd ${servers[$1]}:~/inspircd/etc/ircd.motd
	scp ${options[$1]} ircd.rules ${servers[$1]}:~/inspircd/etc/ircd.rules
}

for server in "${!servers[@]}"
do
   motdsync "$server"
done
