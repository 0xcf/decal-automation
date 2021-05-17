#!/usr/bin/python3
# coding=utf-8
import sys, csv
from textwrap import dedent
from ocflib.misc.mail import send_mail

def send(email, username, hostname, password):
    print(email)    
    message = dedent("""
        Hi {username},

        Your student virtual machine for the Linux SysAdmin Decal is ready. You will need this machine to complete some of your labs. Please note the following login information:

        Host: {username}.decal.xcf.sh
        Username: {username}
        Temporary Password: {password}

        You can login to this machine with `ssh {username}@{hostname}`, after which you’ll be prompted to enter your password. You should see a prompt to change your temporary password after your first login. We recommend selecting a strong password to secure your VM appropriately. 
        
        These VMs were graciously provided for the DeCal by DigitalOcean.

        Let us know if you have any questions or issues,

        Linux SysAdmin DeCal Staff
        """).strip()

    send_mail(
        email,
        '[Linux SysAdmin DeCal] Your Student Virtual Machine Information',
        message.format(
            username=username,
            hostname=hostname,
            password=password
        ),
        cc='decal+vms@ocf.berkeley.edu',
        sender='decal@ocf.berkeley.edu',
    )


def mass_send(filename):
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lc = 0
        for row in csv_reader:
            send(row["email"], row["username"], row["username"] + '.decal.xcf.sh', row["password"])
            lc += 1

        print("Processed {lc} lines".format(lc=lc))
   
print("Reading from file {filename}".format(filename=sys.argv[1]))
mass_send(sys.argv[1])