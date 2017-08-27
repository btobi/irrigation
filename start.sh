#!/bin/bash
pkill -f irrogation.py
pkill -f irrogation_bot.py

echo 'Starting irrogation system'
nohup python irrogation.py &

echo 'Starting telegram bot for irrogation system'
nohup python irrogation_bot.py &

