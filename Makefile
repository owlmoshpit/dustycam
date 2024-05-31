
SERVICE_NAME = "dusty.service"

logs:
	sudo journalctl -u $(SERVICE_NAME) -f

start:
	sudo systemctl start $(SERVICE_NAME)

restart:
	sudo systemctl restart $(SERVICE_NAME)

stop:
	sudo systemctl stop $(SERVICE_NAME)

status:
	sudo systemctl status $(SERVICE_NAME)

