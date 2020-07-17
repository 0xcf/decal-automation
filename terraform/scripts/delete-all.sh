#!/bin/bash

echo "This script deletes all DigitalOcean droplets associated with the account you are authenticated for."
echo "Quit within 5 seconds if you do not want this!"
sleep 5

if [[ $(doctl auth list) == "" ]]; then
    echo "You are not authed with DO!"
fi

hosts=$(doctl compute droplet list | sed '1d' | sed 's/\n/ /g' | awk '{print $1}')

if [[ hosts == "" ]]; then
    echo "No hosts to delete, you're done."
fi

yes 'y' | doctl compute droplet delete $hosts