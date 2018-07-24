#!/usr/bin/env python
# iwgrapher.py
# Jungman Berliansyah N - maman@bengkrad.com v 0.1
# Parses output from iwlist output into grafana interface

from influxdb import InfluxDBClient
from collections import OrderedDict
from subprocess import check_output

import sys, subprocess, time, datetime, json, os, shlex

#Loads config.json
with open('json/config.json') as json_data_file:
    data = json.load(json_data_file)

#Connect to default wifi based on config.json
def wifiConnect():
    connWifi = 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\nnetwork={\n      ssid="' + data['id']['wssid'] + '"\n	psk="' + data['id']['wpass'] + '"\n}'
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(connWifi)
        f.close()
    os.system("ip link set wlan0 down")
    os.system("ip link set wlan0 up")

#SSID
def getSSID(cell):
    return matchingLine(cell,"ESSID:")[1:-1]

#MAC Address
def getMAC(cell):
	return matchingLine(cell,"Address:")

#Signal Quality (In Percentages)
def getsQuality(cell):
    quality = matchingLine(cell,"Quality=").split()[0].split('/')
    return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"

#Signal Power (In dB)
def getsPower(cell):
	return matchingLine(cell, "Quality=").split("Signal level=")[1]

#Types of Encription
def getEncrypt(cell):
	enc=""
	if matchingLine(cell,"Encryption key:") == "off":
		enc="Open"
	else:
		for line in cell:
			matching = match(line,"IE:")
			if matching!=None:
				wpa=match(matching,"WPA Version ")
				if wpa!=None:
					enc="WPA v." + wpa
		if enc=="":
			enc="WEP"
	return enc

# Here's a dictionary of rules that will be applied to the description of each
# cell. The key will be the name of the column in the table. The value is a
# function defined above.
rules={"SSID":getSSID,
       "Quality":getsQuality,
       "Encryption":getEncrypt,
       "MAC":getMAC,
       "Power":getsPower
       }

# Sets of columns and ordering
columns=["SSID","MAC","Quality","Encryption"]

#Returns first matching list of lines
def matchingLine(lines, keyword):
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

#If the first part of line matches keyword, returns EoL. Otherwise returns None
def match(line,keyword):
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

#Applies rules to the bunch of text descriving a cell and returns the corresponding dictionary
def parseCell(cell):
    parsedCell={}
    for key in rules:
        rule=rules[key]
        parsedCell.update({key:rule(cell)})
    return parsedCell

def printCell(cell,i):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    network = str(time_now) + " " + cell[i]["MAC"] + " " + cell[i]["Encryption"]  + " " + cell[i]["Power"] + " " + cell[i]["Quality"] + " " + cell[i]["SSID"]
    print(network)

#Prints table and parses to grafana via fluxdb
def parsedb():

    #start sync with influxdb
    client = InfluxDBClient(data['influx']['host'], data['influx']['port'], data['influx']['user'], data['influx']['passwd'], data['influx']['db'])
    client.create_database(data['influx']['db'])
    client.create_retention_policy( data['influx']['retentionName'], data['influx']['retentionDuration'], int(data['influx']['retentionReplication']), default=data['influx']['retentionActive'])
    cells=[[]]
    parsedCells=[]
    #command start
    proc = subprocess.Popen(["iwlist", data['id']['wint'], "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()

    for line in out.split("\n"):
        cellLine = match(line,"Cell ")
        if cellLine != None:
            cells.append([])
            line = cellLine[-27:]
        cells[-1].append(line.rstrip())

    cells=cells[1:]

    count = 0
    for cell in cells:
        parsedCells.append(parseCell(cell))
        count = count + 1
    lenCells = len(parsedCells)-1

    #Print and parse wifi datas to graph

    #parsing ping to gateway
    client = InfluxDBClient(data['influx']['host'], data['influx']['port'], data['influx']['user'], data['influx']['passwd'], data['influx']['db'])
    client.create_database(data['influx']['db'])
    ping_parse = check_output("ping -c 1 " + data['id']['gateway'] + "| awk -F = 'FNR==2 {print substr($4,1,length($4)-3)}'", shell=True)
    if ping_parse == ('\n'):
        floated = 0.00
    else :
        floated = float(ping_parse.strip('\n'))
    time_parse = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_pings_body = [
                {
                    "measurement": "pings",
                    "tags": {
                        "SSID": data['id']['wssid'],
                        "IP" : data['id']['ip'],
                        "Gateway": data['id']['gateway']
                    },
                    "time": time_parse,
                    "fields": {
                        "value": floated
                    }
                }
            ]
    client.write_points(json_pings_body)

    #parsing signal strength
    i = 0
    while (i < lenCells):
        if (parsedCells[i] != {}):
            printCell(parsedCells,i)
            quality_parse = float(parsedCells[i]["Quality"].strip('%'))
            time_parse = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            json_signal_body = [
                            {
                                "measurement": "signals",
                                "tags": {
                                    "SSID": parsedCells[i]["SSID"],
                                    "MAC": parsedCells[i]["MAC"],
                                    "Encrypt" : parsedCells[i]["Encryption"]
                                },
                                "time": time_parse,
                                "fields": {
                                    "value": quality_parse
                                }
                            }
                        ]
            client.write_points(json_signal_body)
        i = i + 1

# Extract serial from cpuinfo file
def getSerial():
  cpuserial = ""
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[16:26]
    f.close()
  except:
    cpuserial = "ERROR000000"

  memserial = ""
  try:
    f = open('/sys/block/mmcblk0/device/cid','r')
    for line in f:
        memserial = line[0:32]
    f.close()
  except:
    memserial = "ERROR000000000000000000000000"
  serial = cpuserial+memserial
  return serial

# Retrieve IP Address & Default Gateway
def getAddress(param):
    strs = subprocess.check_output(shlex.split('ip r l'))
    ip  = strs.split('src')[-1].split()[0]
    gateway = strs.split('default via')[-1].split()[0]
    if param == 0 :
        return ip
    else :
        return gateway

# Rewrite old conf
def writeConf():
    sortedID = OrderedDict([('serial',getSerial()),
                            ('name',data['id']['name']),
                            ('wint',data['id']['wint']),
                            ('wssid',data['id']['wssid']),
                            ('wpass',data['id']['wpass']),
                            ('ip',getAddress(0)),
                            ('gateway',getAddress(1)),
                            ('pollRate',data['id']['pollRate'])])
    sortedInflux = OrderedDict([('user',data['influx']['user']),
                                ('passwd',data['influx']['passwd']),
                                ('host',data['influx']['host']),
                                ('port',data['influx']['port']),
                                ('db',data['influx']['db']),
                                ('retentionActive',data['influx']['retentionActive']),
                                ('retentionName',data['influx']['retentionName']),
                                ('retentionDuration',data['influx']['retentionDuration']),
                                ('retentionReplication',data['influx']['retentionReplication'])])
    data['id'] = sortedID
    data['influx'] = sortedInflux
    outfile = open('json/config.json', "w")
    outfile.write(json.dumps(data, indent=4, sort_keys=False))
    outfile.close()

def main():
    writeConf()
    wifiConnect()
    while 1 :
        with open('json/restart.json') as json_data_file:
            restart = json.load(json_data_file)
            json_data_file.close()
        if(restart['isRestart'] == 'True'):
            writeConf()
            wifiConnect()
            restart['isRestart'] = "False"
            outrst = open('json/restart.json', "w")
            outrst.write(json.dumps(restart))
            outrst.close()
        parsedb()
        time.sleep(int(data['id']['pollRate']))

main()
