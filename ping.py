import shlex, os, subprocess, time
from subprocess import check_output

strs = subprocess.check_output(shlex.split('ip r l'))
gateway = strs.split('default via')[-1].split()[0]
ip  = strs.split('src')[-1].split()[0]
print ('IP : ') + ip
print ('Gateway : ') + gateway

while 1:
    response = check_output("ping -c 1 " + gateway + "| awk -F = 'FNR==2 {print substr($4,1,length($4)-3)}'", shell=True)
    print float(response)
    time.sleep(3)
