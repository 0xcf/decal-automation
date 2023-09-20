#!/bin/bash
set -euo pipefail

if [ "$#" = 1 ]; then
  username=$1
  dir=$(dirname "$0")
  read -p "New password for $username: " newpw
  { echo passwd $username; sleep 3; echo $newpw; sleep 1; echo $newpw; echo passwd -e $username; echo exit; } | ssh -i "$dir/../../data/decal_root" -o "StrictHostKeyChecking=no" "root@$username.decal.xcf.sh"
else
	echo "Usage: $0 <ocfusername>"
fi
