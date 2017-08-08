#!/bin/bash

# Grab our config
. scripts/config.sh

motdsync () {
	echo "Sync MOTD: $1.motd ircd.rules"

        # shellcheck disable=SC2086
        # options are purposely designed be word-split
	scp ${options[$1]} "$1.motd" "${servers[$1]}:${targetpath}/ircd.motd"
        # shellcheck disable=SC2086
	scp ${options[$1]} ircd.rules "${servers[$1]}:${targetpath}/ircd.rules"
}

if [[ -z "$1" ]]; then
	for server in "${!servers[@]}"
	do
		motdsync "$server"
	done
else
	motdsync "$1"
fi

