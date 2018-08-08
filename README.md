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

| Waktu | Kualitas Sinyal (%) | RTT (ms) | Waktu | Kualitas Sinyal (%) | RTT (ms) | Waktu | Kualitas Sinyal (%) | RTT (ms) | Waktu | Kualitas Sinyal (%) | RTT (ms) |
|:--------:|:-------------------:|:--------:|:--------:|:-------------------:|:--------:|:--------:|:-------------------:|:--------:|:--------:|:-------------------:|:--------:|
| 16:26:03 | 73 | 49.1 | 16:26:53 | 76 | 10.3 | 16:27:43 | 73 | 5.65 | 16:28:33 | 71 | 11 |
| 16:26:08 | 73 | 88.5 | 16:26:58 | 76 | 4.68 | 16:27:48 | 76 | 7.08 | 16:28:38 | 71 | 3.16 |
| 16:26:13 | 66 | 14.4 | 16:27:03 | 74 | 4.49 | 16:27:53 | 73 | 8.71 | 16:28:43 | 77 | 20.1 |
| 16:26:18 | 70 | 6.94 | 16:27:08 | 71 | 7.77 | 16:27:58 | 73 | 8.64 | 16:28:48 | 76 | 3.58 |
| 16:26:23 | 74 | 5.98 | 16:27:13 | 77 | 15.5 | 16:28:03 | 73 | 8.21 | 16:28:53 | 77 | 9 |
| 16:26:28 | 69 | 5.84 | 16:27:18 | 69 | 3.88 | 16:28:08 | 66 | 3.72 | 16:28:58 | 69 | 3.74 |
| 16:26:33 | 76 | 7.82 | 16:27:23 | 71 | 18.1 | 16:28:13 | 74 | 5.57 | 16:29:03 | 71 | 5.24 |
| 16:26:38 | 79 | 7 | 16:27:28 | 71 | 11.6 | 16:28:18 | 69 | 10.4 | 16:29:08 | 76 | 4.52 |
| 16:26:43 | 76 | 6.69 | 16:27:33 | 69 | 7.62 | 16:28:23 | 69 | 7.94 |  |  |  |
| 16:26:48 | 76 | 8.59 | 16:27:38 | 76 | 7.76 | 16:28:28 | 69 | 6.82 | RERATA | 72.76316 | 11.20105 |
