#!/bin/bash
set -e

trap 'ret=$?; test $ret -ne 0 && printf "failed\n\n" >&2; exit $ret' EXIT

log_info() {
  printf "\n\e[0;35m $1\e[0m\n\n"
}

SLURM_VERSION=${SLURM_VERSION:-21.08.8-2}
WEBSOCKIFY_VERSION=${WEBSOCKIFY_VERSION:-0.11.0}
ARCHTYPE=`uname -m`

source /build/base.config

(groupadd doe_users) || true

is_uid_in_use() {
    local uid="$1"
    if getent passwd | awk -F: -v uid="$uid" '$3 == uid { exit 0 } END { exit 1 }'; then
        return 0  # UID is in use
    else
        return 1  # UID is not in use
    fi
}

# add system users
idnumber=1111
for uid in $USERS
do
    # Find the next available UID
    while is_uid_in_use "$idnumber"; do
        idnumber=$((idnumber + 1))
    done

    if id "$uid" &>/dev/null; then
        log_info "User $uid already exists"
        continue
    fi

    (
        useradd -rm --uid="$idnumber" "$uid"
        log_info "Bootstrapping $uid user account..."
        mkdir -p "/home/$uid"
    ) || (
        log_info "Failed to create user $uid"
    )

    idnumber=$((idnumber + 1))

done

for uid in $DOE_USERS
do
  (
    usermod -a -G doe_users $uid 
  )
done
# end of user addition

