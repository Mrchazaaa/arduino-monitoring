# make sure that environment.json file is present and contains ThingsSpeak config keys and Google Sheets config keys

echo "installing dependencies"

pip3 install -r requirements.txt

echo "update lora receiver service"

cp ./lora-receiver.service /etc/systemd/system

systemctl daemon-reload

echo "restart lora receiver service"

systemctl stop lora-receiver.service
systemctl start lora-receiver.service
systemctl enable lora-receiver.service

echo "killing loki container"

docker kill loki-container

echo "spinning up loki container"

docker-compose up -d