#!/bin/bash
set -e

if [ "$1" = "slurmdbd" ]
then
    echo "DOCKERFILE entrypoint.sh: slurmdbd"
    echo "---> Starting SSSD ..."
    # Sometimes on shutdown pid still exists, so delete it
    rm -f /var/run/sssd.pid
    /sbin/sssd --logger=stderr -d 2 -i 2>&1 &

    echo "---> Starting the MUNGE Authentication service (munged) ..."
    gosu munge /usr/sbin/munged

    echo "---> Starting sshd on the slurmdbd..."
    /usr/sbin/sshd -e

    echo "---> Starting the Slurm Database Daemon (slurmdbd) ..."

    {
        . /etc/slurm/slurmdbd.conf
        until echo "SELECT 1" | mysql -h $StorageHost -u$StorageUser -p$StoragePass 2>&1 > /dev/null
        do
            echo "-- Waiting for database to become active ..."
            sleep 2
        done
    }
    echo "-- Database is now active ..."

    exec gosu slurm /usr/sbin/slurmdbd -Dv
    echo "-- Passes gosu slurm slurmdbd ..."
fi

if [ "$1" = "slurmctld" ]
then
    echo "DOCKERFILE entrypoint.sh: slurmctld"
    echo "---> Starting SSSD ..."
    # Sometimes on shutdown pid still exists, so delete it
    rm -f /var/run/sssd.pid
    /sbin/sssd --logger=stderr -d 2 -i 2>&1 &

    echo "---> Starting the MUNGE Authentication service (munged) ..."
    gosu munge /usr/sbin/munged

    echo "---> Starting sshd on the slurmctld..."
    /usr/sbin/sshd -e

    echo "---> Waiting for slurmdbd to become active before starting slurmctld ..."

    until 2>/dev/null >/dev/tcp/slurmdbd/6819
    do
        echo "-- slurmdbd is not available.  Sleeping ..."
        sleep 2
    done
    echo "-- slurmdbd is now active ..."

    echo "---> Starting the Slurm Controller Daemon (slurmctld) ..."
    exec gosu slurm /usr/sbin/slurmctld -Dv
    echo "-- Passes gosu slurm slurmctld ..."
fi

if [ "$1" = "slurmd" ]
then
    echo "DOCKERFILE entrypoint.sh: slurmd"
    echo "---> Starting SSSD ..."
    # Sometimes on shutdown pid still exists, so delete it
    rm -f /var/run/sssd.pid
    /sbin/sssd --logger=stderr -d 2 -i 2>&1 &

    echo "---> Starting the MUNGE Authentication service (munged) ..."
    gosu munge /usr/sbin/munged

    echo "---> Starting sshd on the slurmd..."
    /usr/sbin/sshd -e

    echo "---> Waiting for slurmctld to become active before starting slurmd..."

    until 2>/dev/null >/dev/tcp/slurmctld/6817
    do
        echo "-- slurmctld is not available.  Sleeping ..."
        sleep 2
    done
    echo "-- slurmctld is now active ..."

    echo "---> Starting pmcd on the slurmd..."
    /usr/libexec/pcp/lib/pmcd start-systemd

    echo "---> Starting pmlogger on the slurmd.."
    /usr/libexec/pcp/lib/pmlogger start-systemd

    echo "---> Starting the Slurm Node Daemon (slurmd) ..."
    exec /usr/sbin/slurmd -Dv
fi

if [ "$1" = "frontend" ]
then
    echo "DOCKERFILE entrypoint.sh: frontend"
    echo "---> Starting SSSD ..."
    # Sometimes on shutdown pid still exists, so delete it
    rm -f /var/run/sssd.pid
    /sbin/sssd --logger=stderr -d 2 -i 2>&1 &

    echo "---> Starting the MUNGE Authentication service (munged) ..."
    gosu munge /usr/sbin/munged

    until scontrol ping | grep UP 2>&1 > /dev/null
    do
        echo "-- Waiting for slurmctld to become active ..."
        sleep 2
    done

    accts=$(sacctmgr list -P associations cluster=hpc format=Account,Cluster,User,Fairshare | wc -l)
    if [[ $accts -eq 3 ]]; then
        echo "Creating slurm associations.."
        sacctmgr -i add account staff Cluster=hpc Description=staff
        sacctmgr -i add user hpcadmin DefaultAccount=staff AdminLevel=Admin
        sacctmgr -i add account sfoster Cluster=hpc Description="PI account sfoster"
        sacctmgr -i add user sfoster DefaultAccount=sfoster
        sacctmgr -i add user astewart DefaultAccount=sfoster

        # create parent accounts
        sacctmgr -i add account name=doe_lab fairshare=10
        sacctmgr -i add account name=doe_dev fairshare=10
        sacctmgr -i add account name=doe_fellows fairshare=10
        sacctmgr -i add account name=doe_grads fairshare=10
        sacctmgr -i add account name=doe_mustermann_lab fairshare=10
        sacctmgr -i add account name=doe_negidius_lab fairshare=10
        sacctmgr -i add account name=doe_sidorov_lab fairshare=10
        sacctmgr -i add account name=doe_yamada_lab fairshare=10
        # Create independent lab accounts
        sacctmgr -i add account name=mustermann_lab fairshare=10
        sacctmgr -i add account name=negidius_lab fairshare=10
        sacctmgr -i add account name=sidorov_lab fairshare=10
        sacctmgr -i add account name=yamada_lab fairshare=10

        # User 'jdoe' with default account 'doe_lab'
        sacctmgr -i add user jdoe DefaultAccount=doe_lab fairshare=3
        # User 'aandersson' with default account 'yamada_lab'
        sacctmgr -i add user aandersson DefaultAccount=yamada_lab fairshare=3
        # User 'akowalska' with default account 'mustermann_lab'
        sacctmgr -i add user akowalska DefaultAccount=mustermann_lab fairshare=3
        sacctmgr -i add user name=akowalska account=doe_dev fairshare=3
        # User 'cespanola' with default account 'doe_lab'
        sacctmgr -i add user cespanola DefaultAccount=doe_lab fairshare=3
        sacctmgr -i add user name=cespanola account=doe_fellows fairshare=3
        # User 'hkildong' with default account yamada_lab'
        sacctmgr -i add user hkildong DefaultAccount=yamada_lab fairshare=3
        sacctmgr -i add user name=hkildong account=doe_yamada_lab fairshare=3
        # User 'isidorov' with default account 'sidorov_lab'
        sacctmgr -i add user isidorov DefaultAccount=sidorov_lab fairshare=3
        sacctmgr -i add user name=isidorov account=doe_grads fairshare=3
        # User 'mjanos' with default account 'doe_yamada_lab'
        sacctmgr -i add user mjanos DefaultAccount=yamada_lab fairshare=3
        sacctmgr -i add user name=mjanos account=doe_yamada_lab fairshare=3
        # User 'mmustermann' with default account 'mustermann_lab'
        sacctmgr -i add user mmustermann DefaultAccount=mustermann_lab fairshare=3
        sacctmgr -i add user name=mmustermann account=doe_mustermann_lab fairshare=3
        sacctmgr -i add user name=mmustermann account=doe_dev fairshare=3
        # User 'mdupont' with default account 'mustermann_lab'
        sacctmgr -i add user name=mdupont DefaultAccount=doe_mustermann_lab fairshare=3
        # User 'mrossi' with default account 'doe_fellows'
        sacctmgr -i add user mrossi DefaultAccount=doe_fellows fairshare=3
        # User nnegidius with default account 'negidius_lab'
        sacctmgr -i add user nnegidius DefaultAccount=negidius_lab fairshare=3
        sacctmgr -i add user name=nnegidius account=doe_negidius_lab fairshare=3
        # User 'onordmann' with default account 'doe_fellows'
        sacctmgr -i add user onordmann DefaultAccount=doe_fellows fairshare=3
        # User 'tyamada' with default account 'yamada_lab'
        sacctmgr -i add user tyamada DefaultAccount=yamada_lab fairshare=3
        sacctmgr -i add user name=tyamada account=doe_lab fairshare=3

        echo "creating Groups..."
        # Create group 'doe_users'
        groupadd doe_users

        scontrol reconfigure
    fi

    echo "---> Starting sshd on the frontend..."
    /usr/sbin/sshd -D -e

fi

exec "$@"
