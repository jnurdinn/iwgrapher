# iwgrapher
This is program written in Python script that is used to parse Wifi signal strength using iwlist which is stored in influx db and visualized in Grafana. This script is intended to run at startup as a daemon service, so you may use Crontab routine to launch the Shell Script. This script may also set the default access point (wpa_supplicant) that can be configured manually to make things easier for doing SSH.

## Prerequisites
In order to run, this script requires:
1. Python (https://www.python.org/) | Library required : influxdb
2. Influxdb Server (https://www.influxdata.com/)
3. Grafana Server (https://grafana.com/)

## Installation
1. Clone the project using this command : `git clone https://github.com/mamanberliansyah/iwgrapher`
2. Edit config file `config.json`, here's complete list for configuration :
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
