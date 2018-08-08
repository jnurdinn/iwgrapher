# iwgrapher
A program written in Python script that is used to parse information of Wifi signal strength using iwlist which is stored in influx db and visualized in Grafana. This script is intended to run at startup as a daemon service, so you may use Crontab routine to launch the Shell Script. This script may also set the default access point (wpa_supplicant) that can be configured manually to make things easier for doing SSH. I was intended to write this script for Raspberry Pi, but you can use it in any other device as long as it has Wifi Network Card.

## Prerequisites
In order to run, this script requires:
1. Python (https://www.python.org/) | Library required : influxdb
2. Influxdb Server (https://www.influxdata.com/)
3. Grafana Server (https://grafana.com/)

## Installation
1. Clone the project using this command : <br />`git clone https://github.com/mamanberliansyah/iwgrapher` <br />
2. Edit config file `config.json`, here's complete list for configuration :

| No. | Configuration | Info |
| --- | ------------- | ----------- |
| 1.  | id,serial | Unique generated serial number |
| 2.  | id,name | User's name |
| 3.  | id,wint | Wireless card interface |
| 4.  | id,wssid | WiFi SSID |
| 5.  | id,wpass | WiFi password |
| 6.  | id,pollRate | Data parsing rate in second |
| 7.  | id,location | Monitor location spot |
| 8.  | influx,host | IP Address for Influxdb server host |
| 9.  | influx,port | Port for Influxdb server host |
| 10.  | influx,user | Username for Influxdb server host |
| 11. | influx,passwd | User password for Influxdb server host |
| 12. | influx,db | Database name for Influxdb server host |
| 13. | influx,retentionActive | Database retention policy active |
| 14. | influx,retentionName | Database retention name |
| 15. | influx,retentionDuration | Database retention duration |
| 16. | influx,retentionReplication | Database retention replication type |

3. Run the program to see if it works : `sudo python iwgrapher.py` <br />
The program will print table contain informations about time, MAC Address, Encryption Type, Signal Strength, Signal Quality, and SSID. <br />

4. To visualize parsed data, you need to add recently made query into metrics on Grafana. Here's a complete tutorial to help you how to do it : http://docs.grafana.org/guides/getting_started/ 

5. If you want to run this script everytime you start the device, you may want to use Crontab routine to launch included shell script (launch.sh). Type this command : `$ sudo Crontab -e` <br /> Add the following line : <br /> `@reboot sleep 5 && sh /home/pi/iwgrapher/launcher.sh >/home/pi/iwgrapher/logs/cronlog 2>&1` <br /> 

6. To see if it works, reboot your device by typing in : `sudo reboot` <br /> If it won't start, you can always check the log file to see what's wrong (It's located on logs/cronlog)


| Waktu | Kualitas Sinyal (%) | RTT (ms) | Waktu | Kualitas Sinyal (%) | RTT (ms) | Waktu | Kualitas Sinyal (%) | RTT (ms) |
|:--------:|:-------------------:|:--------:|:--------:|:-------------------:|:--------:|:--------:|:-------------------:|:--------:|
| 15:37:44 | 79 | 8.84 | 15:38:34 | 81 | 7.64 | 15:40:14 | 76 | 3.64 |
| 15:37:49 | 81 | 11.1 | 15:38:39 | 84 | 5.37 | 15:40:19 | 84 | 67.8 |
| 15:37:54 | 80 | 7.19 | 15:38:44 | 79 | 0 | 15:40:24 | 84 | 115 |
| 15:37:59 | 80 | 11.6 | 15:38:49 | 73 | 21.3 | 15:40:29 | 74 | 15.9 |
| 15:38:04 | 86 | 7.72 | 15:38:54 | 77 | 10.4 | 15:40:34 | 80 | 13.2 |
| 15:38:09 | 81 | 3.23 | 15:38:59 | 79 | 9.87 | 15:40:39 | 84 | 14.3 |
| 15:38:14 | 77 | 7.33 | 15:39:04 | 79 | 8.41 | 15:40:44 | 81 | 3.82 |
| 15:38:19 | 87 | 10.8 | 15:39:09 | 77 | 22.3 | 15:40:49 | 84 | 3.54 |
| 15:38:24 | 81 | 7.22 | 15:39:14 | 77 | 18.2 |  |  |  |
| 15:38:29 | 84 | 6.85 | 15:39:19 | 76 | 5.81 | Rerata | 80.7105 | 13.255 |
||||||||:--------:|
