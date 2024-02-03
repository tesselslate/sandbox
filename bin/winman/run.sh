#!/usr/bin/bash
Xephyr -br -ac -noreset -screen 800x600 :1 &
sleep 0.2
DISPLAY=:1 out/winman
pkill Xephyr
