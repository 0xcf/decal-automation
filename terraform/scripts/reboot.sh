curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <APIKEY>" -d '{"type":"reboot"}' "https://api.digitalocean.com/v2/droplets/$1/actions"
