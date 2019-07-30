#!/bin/bash
# A frontend to certbot for managing IRC RR TLS certificates.

error() {
    echo "ERROR: $*"
    exit 1
}

cd "${0%/*}" || { error "Could not cd to script dir"; }

. ../scripts/config.sh || { error "Could not find config.sh"; }
. certpush.config.sh || { error "Could not find certpush.config.sh"; }

if [[ "$TEST_MODE" == true ]]; then
    CERTBOT_BASE_ARGS+=(--test-cert)
fi

newserver() {
    server="$1"
    if [[ -z "$server" ]]; then
        error "no server name given to newserver()"
    fi

    # Save server-specific hosts for certbot
    server_hosts="${CERTPUSH_SERVERS[$server]}"

    if [[ -z "$server_hosts" ]]; then
        error "Server $server is not defined in CERTPUSH_SERVERS"
    fi

    certbot_args=("${CERTBOT_BASE_ARGS[@]}" "${AUTH_METHOD[@]}" certonly --cert-name "$server")

    for host in "${POOL_NAMES[@]}"; do
        server_hosts+=",$host"
    done

    certbot_args+=("-d" "$server_hosts")
    echo "Will call certbot with args: ${certbot_args[*]}"
    eval "${certbot_args[@]}"
}

renew() {
    certbot_args=("${CERTBOT_BASE_ARGS[@]}" "renew" "--reuse-key")
    echo "Will call certbot with args: ${certbot_args[*]}"
    eval "${certbot_args[@]}"
}

push() {
    server="$1"
    if [[ -z "$1" ]]; then
        error "no server name given to push()"
    fi
	target_path="$(getpath "$1")"

    certfile="$(readlink -f "$CONFIG_DIR/live/$1/fullchain.pem")"
    keyfile="$(readlink -f "$CONFIG_DIR/live/$1/privkey.pem")"
    echo
    if [[ -z "$certfile" || -z "$keyfile" ]]; then
        echo "Certfile or keyfile missing for server $1!"
        return
    fi

    echo "Syncing files for server $1:"
    certfile_path="${SERVERS[$1]}:${target_path}/certpush.pem"
    keyfile_path="${SERVERS[$1]}:${target_path}/certpush.key"

    echo "Syncing $certfile to $certfile_path"
    scp ${OPTIONS[$1]} "$certfile" "$certfile_path"
    echo "Syncing $keyfile to $keyfile_path"
    scp ${OPTIONS[$1]} "$keyfile" "$keyfile_path"
    # TODO: make this configurable
    ssh ${OPTIONS[$1]} "${SERVERS[$1]}" killall -USR1 inspircd
}

push_all() {
    for server in "${!CERTPUSH_SERVERS[@]}"; do
        push "$server"
    done
}

print_usage() {
    echo "Usage:"
    echo "$0 newserver [server name] - generates a certificate for the given server"
    echo "$0 renew - renews all known certificate and pushes them to servers"
    echo "$0 push [server name] - pushes the certificate for the given server via SFTP"
    echo "$0 runcmd [command] [args] - run arbitrary certbot commands under certpush's config directories"
    exit 0
}


CMD="$1"
TARGET="$2"

if [[ -z "$CMD" ]]; then
    print_usage No command given
    exit 1
fi

if [[ "$CMD" == "newserver" ]]; then
    newserver "$2"
    push "$2"

elif [[ "$CMD" == "renew" ]]; then
    renew
    push_all

elif [[ "$CMD" == "runcmd" ]]; then
    shift
    certbot_args=("${CERTBOT_BASE_ARGS[@]}" "$@")
    eval "${certbot_args[@]}"

elif [[ "$CMD" == "push" ]]; then
    if [[ -n "$TARGET" ]]; then
        push "$TARGET"
    else
        push_all
    fi

else
    print_usage "Unknown command"
    exit 1
fi
