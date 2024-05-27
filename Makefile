
SERVICE_NAME = "dusty.service"

logs:
	sudo journalctl -u $(SERVICE_NAME) -f

stop:
	sudo systemctl stop $(SERVICE_NAME)

status:
	sudo systemctl status $(SERVICE_NAME)

