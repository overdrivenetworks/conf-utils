#!/bin/bash

# Grab our config
. scripts/config.sh

default_targetpath="$targetpath"

motdsync () {
	# Support server-specific paths if defined.
	if [[ ! -z "${targetpaths[$1]}" ]]; then
		targetpath="${targetpaths[$1]}"
	else
		targetpath="$default_targetpath"
	fi

	echo "Sync MOTD: $1"

	echo "    $1.motd => ${targetpath}/ircd.motd"
	# shellcheck disable=SC2086
	# options are purposely designed be word-split
	scp ${options[$1]} "$1.motd" "${servers[$1]}:${targetpath}/ircd.motd"

	echo "    ircd.rules => ${targetpath}/ircd.rules"
	# shellcheck disable=SC2086
	scp ${options[$1]} ircd.rules "${servers[$1]}:${targetpath}/ircd.rules"
}

if [[ -z "$1" ]]; then
	for server in "${!servers[@]}"
	do
		motdsync "$server"
		echo ""
	done
else
	motdsync "$1"
fi

