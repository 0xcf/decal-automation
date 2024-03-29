#!/usr/bin/python3
# coding=utf-8
import csv
from os import path
from textwrap import dedent
from ocflib.misc.mail import send_mail

def send(email, username, hostname, password):
    print(email)
    message = dedent("""
        Hi {username},

        Your student virtual machine for the Linux SysAdmin Decal is ready. You will need this machine to complete some of your labs. Please note the following login information:

        Host: {hostname}
        Username: {username}
        Temporary Password: {password}

        If you're not on eduroam you'll need to use the Berkeley VPN to connect to your VM: https://security.berkeley.edu/services/bsecure/bsecure-remote-access-vpn

        You can login to this machine with `ssh {username}@{hostname}`, after which you’ll be prompted to enter your password. You should see a prompt to change your temporary password after your first login, it will first ask you to enter your temporary password again and then ask you to type in your new password and confirm it. We recommend selecting a strong password to secure your VM appropriately.

        If you have any questions or issues logging in (notably permission denied: publickey or port 22: connection refused), please make a private post on Ed or reply to this email with your OCF username.

        Best,
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
            send(row["email"], row["username"], f'{row["username"]}.decal.ocfhosted.com', row["password"])
            lc += 1

        print("Processed {lc} lines".format(lc=lc))

filename = path.join(path.dirname(__file__), 'data', 'students.csv')

print("Reading from file {filename}".format(filename=filename))
mass_send(filename)
