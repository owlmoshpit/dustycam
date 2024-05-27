sudo apt update
sudo apt upgrade -y

#OpenCV dependencies
sudo apt install ffmpeg libsm6 libxext6 -y

#General python dependencies
sudo apt install gcc python3-dev -y

#Install virtual env in an user independent location
sudo mkdir -p /opt/dusty
sudo chown -R $(whoami):$(whoami) /opt/dusty/
cd /opt/dusty/
python3 -m venv --source-packages env


#activate the virtual env
source /opt/dusty/env/bin/activate

# Clone repo and install dependencies
cd ~/
git clone git@github.com:owlmoshpit/dustycam.git
pip install -e dustycam/