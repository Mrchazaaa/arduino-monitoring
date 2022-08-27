# make sure that environment.json file is present and contains ThingsSpeak config keys and Google Sheets config keys

pip3 install -r requirements.txt

python3 /home/pi/workspace/arduino-monitoring/PiServer/PiServer.py

cp ./lora-receiver.service /etc/systemd/system

systemctl daemon-reload

systemctl stop lora-receiver.service
systemctl start lora-receiver.service
systemctl enable lora-receiver.service
