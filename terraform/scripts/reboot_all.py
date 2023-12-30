#!/usr/bin/env python3

from os import path

students_file = path.join(path.dirname(__file__), '..', '..', 'data', 'students.csv')

import csv, subprocess

with open(students_file) as csv_students:
    csv_reader = csv.DictReader(csv_students)
    for row in csv_reader:
        try:
          subprocess.run(['sudo', 'virsh', 'reboot', f'decalvm-{row["username"]}'])
        except subprocess.CalledProcessError as e:
           print(f'error rebooting decalvm-{row["username"]}! {e}')
