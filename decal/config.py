import configargparse

p = configargparse.ArgParser(default_config_files=['~/decalconf'])

p.add('--config', is_config_file=True, help='config file path (default: ~/decalconf)')
p.add('--db-host', required=True)
p.add('--db-user', required=True)
p.add('--db-pass', required=True)
p.add('--db-dbname', required=True)
p.add('--semester', required=True)
p.add('--google-creds-path', required=True)

config = p.parse_args()
