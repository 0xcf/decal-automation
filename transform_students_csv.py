# take csv from google forms and turn it into one that can be accepted by terraform with all the parameters

infile = './data/students.in.csv'
outfile = './data/students.csv'

import csv, secrets, subprocess

with open(outfile) as csv_outfile:
    outfile_linecount = sum(1 for _ in csv_outfile)
    if outfile_linecount > 0:
        continue_processing = input(f'{outfile} already has content! this file will be overwritten by the script. do you want to continue? [yN] ')
        if continue_processing.lower() not in ['y', 'yes']:
            print('aborting')
            exit(1)

with open(infile) as csv_infile:
    with open(outfile, 'w') as csv_outfile:
        csv_reader = csv.DictReader(csv_infile)
        csv_writer = csv.DictWriter(csv_outfile, fieldnames=['id', 'username', 'password', 'hashed_password', 'email'])
        csv_writer.writeheader()
        i = 0
        for row in csv_reader:
            password = secrets.token_urlsafe(8)
            try:
                hashed_password = subprocess.run(
                    ['mkpasswd', '-m', 'sha-512', '-R', '4096', password],
                    check=True,
                    capture_output=True,
                    text=True
                ).stdout
                hashed_password = hashed_password.strip() # remove leading and trailing whitespace
            except subprocess.CalledProcessError as e:
                print(f'error hashing password! {e}')
                exit(1)
            student = {
                'id': i + 2, # ids are how we derive IPs and they must start at 2
                'username': row['username'],
                'email': row['email'],
                'password': password,
                'hashed_password': hashed_password
            }
            csv_writer.writerow(student)
            i += 1

    print(f'processed {i} students')
