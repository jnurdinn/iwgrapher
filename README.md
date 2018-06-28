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

| No. | Configuration | Info |
| --- | ------------- | ----------- |
| 1.  | id,serial | Unique generated serial number |
| 2.  | id,name | User's name |
| 3.  | id,wint | Wireless card interface |
| 4.  | id,wssid | WiFi SSID |
| 5.  | id,wpass | WiFi password |
| 6.  | influx,host | IP Address for Influxdb server host |
| 7.  | influx,port | Port for Influxdb server host |
| 8.  | influx,user | Username for Influxdb server host |
| 8.  | influx,passwd | User password for Influxdb server host |
| 9.  | influx,db | Database name for Influxdb server host |
