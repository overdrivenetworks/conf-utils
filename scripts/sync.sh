#!/bin/bash
# Grab our config
. scripts/config.sh

if [[ -z "$TMPDIR" ]]; then
	TMPDIR="tmp"
fi

mkdir -p "$TMPDIR"

csync () {
	# Support server-specific paths if defined.
	TARGET_PATH="$(getpath "$1")"

	echo "Sync: $TARGET_FILE @ $1"
	_TMPFILE="$TMPDIR/$1.conf"
	_REAL_TARGETFILE="${SERVERS[$1]}:${TARGET_PATH}/${TARGET_FILE}"

	# Write the config file to a temporary file.
	getconfig "$1" > "$_TMPFILE"

	echo "Transferring $_TMPFILE => $_REAL_TARGETFILE"
	# shellcheck disable=SC2086
	# options are purposely designed be word-split
	scp ${OPTIONS[$1]} "$_TMPFILE" "$_REAL_TARGETFILE"
	rm "$_TMPFILE"
}

declare -A pids
if [[ -z "$1" ]]; then
	for server in "${!SERVERS[@]}"
	do
		csync "$server" &
		pids["$server"]="$!"
		echo ""
	done
	for pid in "${pids[@]}"; do
		wait "$pid"
	done
else
	csync "$1"
fi
