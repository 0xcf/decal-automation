 #!/bin/bash
  2 # set -euo pipefail
  3 onevm() {
  4         { echo 'echo 'Match User $1' >> /etc/ssh/sshd_config' ; echo 'echo 'PasswordAuthenticati    on yes' >> /etc/ssh/sshd_config'; sleep 3; echo systemctl restart ssh; echo exit; } | ssh -o "St    rictHostKeyChecking=no" -i decal_rsa -tt root@$1.decal.xcf.sh
  5 }
  6 export -f onevm
  7 if [ $# -le 0 ] || [ $# -ge 3 ]; then
  8         printf "Allows password authentication for all VM's USERNAME@USERNAME.decal.xcf.sh.\nUsa    ge: ./ssh-passwd-allow USERNAME\n-f: Specify a CSV file with format (email, fullname, username,     password) to batch allow all.\n"
  9 elif [ $# -eq 1 ]; then
 10         onevm $1
 11 else
 12         cat $2 | cut -d ',' -f2 | tail -n+2 | xargs -L1 bash -c 'onevm "$@"' _
 13 fi
