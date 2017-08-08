#!/bin/bash
if [[ "$(git symbolic-ref --short -q HEAD)" != master ]] && [[ $1 != "force" ]]; then
	echo "Aborting sync since we're not on branch 'master'. Run --force to sync anyways."
	exit 1
fi

# Grab our config
. scripts/config.sh

if [[ -z "$tmpfolder" ]]; then
	tmpfolder="tmp"
fi

if [[ -z "$targetpath" ]]; then
	echo "No target path specified in conf?"
	exit 1
fi

mkdir -p "$tmpfolder"

csync () {
	# XXX: make this configurable, but in a backwards-compatible fashion
	targetfile="inspircd.conf"

	echo "Sync: $targetfile @ $1"
	_TMPFILE="$tmpfolder/$1.conf"
	_REAL_TARGETFILE="${servers[$1]}:${targetpath}/${targetfile}"

	# Write the config file to a temporary file.
	getconfig "$1" > "$_TMPFILE"

	echo "Transfering $_TMPFILE => $_REAL_TARGETFILE"
	# shellcheck disable=SC2086
	# options are purposely designed be word-split
	scp ${options[$1]} "$_TMPFILE" "$_REAL_TARGETFILE"
	rm "$_TMPFILE"
}

if [[ -z $1 ]]; then
	for server in "${!servers[@]}"
	do
		csync "$server"
		echo ""
	done
else
	csync "$1"
fi
