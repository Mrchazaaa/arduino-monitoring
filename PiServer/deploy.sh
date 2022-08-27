# make sure that environment.json file is present and contains ThingsSpeak config keys and Google Sheets config keys

pip3 install -r requirements.txt

cp ./lora-receiver.service /etc/systemd/system

systemctl daemon-reload

systemctl stop lora-receiver.service
systemctl start lora-receiver.service
systemctl enable lora-receiver.service
