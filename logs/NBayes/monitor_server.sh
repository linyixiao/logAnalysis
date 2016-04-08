slaveConfig="./slaves"
home=`pwd`
for slave in `cat $slaveConfig`
do
	echo "Starting Server on `hostname`"
	ssh $slave "cd $home/; sh monitor_client.sh" &
done

