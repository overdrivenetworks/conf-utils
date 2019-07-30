#!/bin/bash

# Grab our config
. scripts/config.sh

default_TARGET_PATH="$TARGET_PATH"

motdsync () {
	# Support server-specific paths if defined.
	if [[ ! -z "${TARGET_PATHS[$1]}" ]]; then
		TARGET_PATH="${TARGET_PATHS[$1]}"
	else
		TARGET_PATH="$DEFAULT_TARGET_PATH"
	fi

	echo "Sync MOTD: $1"

	echo "    $1.motd => ${TARGET_PATH}/ircd.motd"
	# shellcheck disable=SC2086
	# options are purposely designed be word-split
	scp ${OPTIONS[$1]} "$1.motd" "${SERVERS[$1]}:${TARGET_PATH}/ircd.motd"

	echo "    ircd.rules => ${TARGET_PATH}/ircd.rules"
	# shellcheck disable=SC2086
	scp ${OPTIONS[$1]} ircd.rules "${SERVERS[$1]}:${TARGET_PATH}/ircd.rules"
}

if [[ -z "$1" ]]; then
	for server in "${!SERVERS[@]}"
	do
		motdsync "$server"
		echo ""
	done
else
	motdsync "$1"
fi

