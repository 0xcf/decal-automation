uname=$1
scp -i decal_rsa -o "StrictHostKeyChecking=no" sshd_config root@$uname.decal.xcf.sh:/etc/ssh/sshd_config
ssh -i decal_rsa -o "StrictHostKeyChecking=no" root@$uname.decal.xcf.sh "systemctl restart sshd"
