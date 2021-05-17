#!/bin/bash
set -euo pipefail

user=$(grep $1 -r sp21vm.csv | head -1 | cut -d',' -f3)
newpw=$(grep $1 -r sp21vm.csv | head -1 | cut -d',' -f4)
echo "Confirm new credentials $user:$newpw"
sleep 2
{ echo passwd $user; sleep 3; echo $newpw; sleep 1; echo $newpw; echo passwd -e $user; echo exit; } | ssh -i ../decal_rsa -tt root@$user.decal.xcf.sh


