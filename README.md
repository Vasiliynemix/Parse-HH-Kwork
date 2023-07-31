apt update && apt upgrade

useradd -m -s /bin/bash -G sudo nemix

passwd nemix

apt install ufw

sudo ufw status verbose

ufw app list

ufw allow ssh

ufw enable

ufw status

su - nemix