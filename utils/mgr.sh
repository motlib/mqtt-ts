#!/bin/bash
#
# This script manages the mqtt-ts installation on remote nodes. It
# updates the application from github distributes new configuration
# files and reloads the service to enable the new configuration.
#
# The script logs in tpo all nodes by ssh, so it's best to use ssh
# public-key authentication and load your private key with ssh-add,
# before starting the script.
#

# The nodes to process
NODES="bpi1 rpi1 rpi2 rpi3"

# Node for rrd graphing
RRDNODE=bpi1

# The install path (must be the same on all nodes).
INSTPATH=/opt/mqtt-ts


# Update the application with git pull.
function do_app_update {
    NODE=$1

    echo "Updating application on ${NODE}."
    ssh root@${NODE} "cd ${INSTPATH}; git pull"
}


# Update the mqtt-pub configuration. 
function do_mqtt_pub {
    NODE=$1
    
    # The name of the configuration file to distribute
    CFG=mqtt-pub.yaml

    echo "Deploying configuration."
    scp ../cfg/${CFG} root@${NODE}:${INSTPATH}/cfg

    echo "Reloading service mqtt-pub."
    ssh root@${NODE} "service mqtt-pub restart"    
}


# Update the mqtt-rrd configuration
function do_mqtt_rrd {
    NODE=$1
    
    CFG=mqtt-rrd.yaml

    echo "Deploying configuration."
    scp ../cfg/${CFG} root@${NODE}:${INSTPATH}/cfg

    echo "Restarting service mqtt-pub."
    ssh root@${NODE} "service mqtt-rrd restart"     

    echo "Sleeping before checking log file..."
    sleep 3

    echo "Here comes the log file (last 20 lines)."
    ssh root@${NODE} "tail /var/log/mqtt-rrd.log"
}


ACTION=$1

case $ACTION in
    mqtt_rrd)
	do_$ACTION ${RRDNODE}
	;;

    app_update|mqtt_pub)
	for NODE in ${NODES}
	do
	    do_${ACTION} ${NODE}
	done

	;;
    *)
	echo "Please provide an action: mqtt_rrd, mqtt_pub, app_update"
	exit 1
	;;
esac

