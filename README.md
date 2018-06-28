# iwgrapher
This is program written in Python script that is used to parse Wifi signal strength using iwlist which is stored in influx db and visualized in Grafana. This script is intended to run at startup, so it uses Crontab routine and Shell Script. This script also set the default access point that can be configured.

## Prerequisites
In order to run, this script requires:
1. Python
2. Influxdb
3. Grafana Server

## Installation
