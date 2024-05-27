cd /opt/dusty
sudo cp /dustycam/dustycam/assets/dusty.service /etc/systemd/system/dusty.service

sudo systemctl daemon-reload

sudo systemctl enable dusty.service
sudo systemctl start dusty.service
sudo systemctl status dusty.service