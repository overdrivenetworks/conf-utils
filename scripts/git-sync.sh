#!/bin/bash
if [[ `git symbolic-ref --short -q HEAD` != master ]] && [[ $1 != "force" ]]; then
	echo "Aborting sync since we're not on branch 'master'."
	exit 0
fi

# Grab our config
. scripts/config.sh

mkdir -p tmp/

csync () {
	echo "Sync: $1.$serversuffix"
	getconfig $1 > tmp/$1.conf
	scp ${options[$1]} tmp/$1.conf ${servers[$1]}:${targetpath}/inspircd.conf
	rm tmp/$1.conf
}

if [[ -z $1 ]]; then
	for server in "${!servers[@]}"
	do
		csync "$server"
	done
else
	csync "$1"
fi
