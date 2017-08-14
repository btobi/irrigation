#!/bin/bash
pkill -f irrogation.py
pkill -f web.py

nohup python irrogation.py &
nohup python web.py &

