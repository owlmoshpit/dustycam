# DustyCam

An open source camera to quickly capture quantified information. 


## Build Your Own DustyCam
Here's what you need to get started.

- Raspberry Pi 5
- Raspberry Pi Camera Module HQ
- 3D Printed Case


## Install On Your Pi

First, clone the repository.
```bash
git clone https://github.com/owlmoshpit/dustycam
cd dustycam
```

Create a virtual environment and install the package.
```bash
python3 -m venv env
source env/bin/activate

pip install -e .

## Setup pi to take photos when there is motion.

```
crontab -e
```
Then add this line to the bottom of the file.

```
@reload  /home/dusty/env/bin/python /home/dusty/dustycam/dustycam/test_motion.py
```

## Run DustyCam
```bash
dustycam
```
