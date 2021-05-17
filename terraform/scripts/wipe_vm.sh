if [ "$#" = 1 ]; then
	cp sp21vm.csv sp21backup.csv
	trap 'cp sp21backup.csv sp21vm.csv' SIGINT 
	grep -v "$1" sp21vm.csv > sp21temp.csv
	mv sp21temp.csv sp21vm.csv
	./terraform apply
	cp sp21backup.csv sp21vm.csv
	./terraform apply
else
	echo "Usage: wipe_vm.sh <ocfusername>"
fi
