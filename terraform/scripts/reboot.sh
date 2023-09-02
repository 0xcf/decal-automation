#!/bin/bash
set -euo pipefail

if [ "$#" = 1 ]; then
  username=$1
  dir=$(dirname "$0")
  ssh -i "$dir/../../data/decal_root" -o "StrictHostKeyChecking=no" "root@$username.decal.xcf.sh" "reboot now"
else
	echo "Usage: $0 <ocfusername>"
fi
