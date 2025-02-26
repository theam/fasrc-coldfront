#!/bin/bash
set -e

trap 'ret=$?; test $ret -ne 0 && printf "failed\n\n" >&2; exit $ret' EXIT

log_info() {
  printf "\n\e[0;35m $1\e[0m\n\n"
}

ARCHTYPE=`uname -m`

source /build/base.config

#------------------------
# Bootstrap LDAP OUs
#------------------------
mkdir -p /container/service/slapd/assets/config/bootstrap/ldif/custom
cat > /container/service/slapd/assets/config/bootstrap/ldif/custom/0-ous.ldif <<EOF
dn: ou=People,dc=example,dc=org
objectClass: organizationalUnit
ou: People

dn: ou=Groups,dc=example,dc=org
objectClass: organizationalUnit
ou: Groups
EOF

#------------------------
# Setup user accounts
#------------------------

idnumber=1001

declare -A realnames
realnames=(
  [jdoe]='John Doe'
  [aandersson]="Anna Andersson"
  [akowalska]="Anna Kowalska"
  [cespanola]="Carmen Espanola"
  [enovakova]="Eva Novakova"
  [hkildong]="Hong Kildong"
  [isidorov]="Ivan Sidorov"
  [jjonsson]="Jon Jonsson"
  [mdupont]="Marie Dupont"
  [mjanos]="Minta Janos"
  [mmustermann]='Max Mustermann'
  [mrossi]="Maria Rossi"
  [nnegidius]="Numerius Negidius"
  [onordmann]="Otto Nordmann"
  [pivanov]="Petr Ivanov"
  [ssvensson]="Sven Svensson"
  [tyamada]="Taro Yamada"
  [wdebruijn]="Willeke de Bruijn"
  [ycohen]="Yossi Cohen"
)

for uid in hpcadmin $USERS
do
    log_info "Adding LDIF for $uid user account with uidnumber $idnumber.."
    passvar="PASSWD_$uid"
    passwd=${!passvar:-ilovelinux}
    fullnamevar="${realnames[$uid]}"
    fullname=${fullnamevar:-$uid}
    cat > /container/service/slapd/assets/config/bootstrap/ldif/custom/1-$uid.ldif <<EOF
dn: cn=${uid},ou=People,dc=example,dc=org
objectClass: person
objectClass: posixAccount
objectClass: inetOrgPerson
gecos: ${fullname}
cn: ${uid}
sn: ${uid}
uid: ${uid}
homeDirectory: /home/${uid}
uidNumber: ${idnumber}
gidNumber: ${idnumber}
mail: ${uid}@example.com
userpassword: ${passwd}
loginShell: /bin/bash

dn: cn=${uid},ou=Groups,dc=example,dc=org
objectClass: posixGroup
objectClass: groupOfMembers
cn: ${uid}
gidNumber: ${idnumber}
member: cn=${uid},ou=People,dc=example,dc=org
EOF
    idnumber=$((idnumber + 1))
done

gidnumber=2001


for gid in $GROUPS
do
    log_info "Adding LDIF for $gid group account with gidnumber $idnumber.."
    cat > /container/service/slapd/assets/config/bootstrap/ldif/custom/1-$uid.ldif <<EOF
dn: cn=${gid},ou=Groups,dc=example,dc=org
objectClass: posixGroup
objectClass: groupOfMembers
cn: ${gid}
gidNumber: ${idnumber}
EOF
    idnumber=$((idnumber + 1))
done
