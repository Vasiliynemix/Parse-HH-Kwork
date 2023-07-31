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

sudo apt install git

cd /home/nemix

git clone https://github.com/Vasiliynemix/Parse-HH-Kwork.git

# заменить .env.example на .env
mv .env.example .env
# заменить данные в .env

sudo apt install python3.10-venv

cd /home/nemix/FSM_example_bot

python3 -m venv venv

source venv/bin/activate

sudo apt install python3-pip

pip install -r requirements.txt

which firefox

wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz

tar -xvzf geckodriver*

chmod +x geckodriver

sudo mv geckodriver /usr/bin/
cd /usr/bin
sudo chown root:root geckodriver

pip3 install selenium

sudo nano ~/.bashrc
    export PATH=$PATH:"/usr/bin/firefox"
    export PATH=$PATH:"/usr/bin/geckodriver"

sudo reboot

python3 -m src.bot




