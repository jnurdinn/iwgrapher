#!/usr/bin/env python
# iwgrapher
# juan4life - maman@bengkrad.com v 0.1
# Parses output from iwlist various output into grafana interface

import sys
import subprocess
import time

interface = "wlp2s0"

#SSID
def get_SSID(cell):
    return matching_line(cell,"ESSID:")[1:-1]

#
def get_MAC(cell):
	return matching_line(cell,"Address:")

#Signal Quality (In Percentages)
def get_sQuality(cell):
    quality = matching_line(cell,"Quality=").split()[0].split('/')
    return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"

#Channel
def get_channel(cell):
	return matching_line(cell,"Channel:")

#Signal Power (In dB)
def get_sPower(cell):
	return matching_line(cell, "Quality=").split("Signal level=")[1]

#Types of Encription
def get_encrypt(cell):
	enc=""
	if matching_line(cell,"Encryption key:") == "off":
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
rules={"SSID":get_SSID,
       "Quality":get_sQuality,
       "Channel":get_channel,
       "Encryption":get_encrypt,
       "MAC":get_MAC,
       "Power":get_sPower
       }

# Sort Cells, based on best signal quality
def sort_cells(cells):
	sortby = "Quality"
	reverse = True
	cells.sort(None, lambda el:el[sortby],reverse)

# Sets of columns and ordering
columns=["SSID","MAC","Quality","Encryption"]

#Returns first matching list of lines
def matching_line(lines, keyword):
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
def parse_cell(cell):
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

#initials
def init(table):
    counter = 0
    a = []
    for line in table:
        for el in line:
            #initial data
            if (counter < 24):
                counter = counter + 1
                if (counter == 5):
                    a.append(el)
                if (counter == 6):
                    a.append(el)
    return a

def init_cells(cells):
    table=[columns]
    for cell in cells:
        cell_properties=[]
        for column in columns:
            cell_properties.append(cell[column])
        table.append(cell_properties)
    return init(table)

#Main Program, prints table from iwlist command
def main():
    stats = 0

    while 1:

        cells=[[]]
        parsed_cells=[]

        proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()

        for line in out.split("\n"):
            cell_line = match(line,"Cell ")
            if cell_line != None:
                cells.append([])
                line = cell_line[-27:]
            cells[-1].append(line.rstrip())

        cells=cells[1:]

        count = 0
        for cell in cells:
            parsed_cells.append(parse_cell(cell))
            count = count + 1

        sort_cells(parsed_cells)

        #state the initial network card
        if stats == 0 :
            a = init_cells(parsed_cells)
            print("Yang ingin dicek : " + a[0] + " " + a[1])
            stats = 1

        len_cells = len(parsed_cells)-1

        net_card = [""]

        i = 0
        found = 0
        while (i < len_cells) & (found == 0):
            if (parsed_cells[i]["SSID"] == a[0]) & (parsed_cells[i]["MAC"] == a[1]) & (found == 0):
                net_card[0] = parsed_cells[i]["SSID"] + "|" + parsed_cells[i]["MAC"] + "|" +  parsed_cells[i]["Encryption"]
                print(net_card[0] + "|" + parsed_cells[i]["Quality"])
                found = 1
            i = i + 1
        if (found == 0):
            print("Card not found")

main()
