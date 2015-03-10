import sys 
import os
import re
import time
import subprocess

descriptors = []
diskstats = {}
lastupdate_time = 0
metric_elems = {'rrqm_sec' : 'Number', 'wrqm_sec'  : 'Number', 'read_sec' : 'Number' , 'write_sec':
        'Number' , 'read_sector_kb_sec' : 'KB/Sec',
        'write_sector_kb_sec' : 'KB/Sec','avgrq-sz' : 'Length' , 'avgqu-sz' : 'Length', 'await' :
        'millisec', 'r_awit' : 'millisec', 'w_await' : 'millisec','svctm' : 'millisec',
        'percentutil' : '%'}


def get_disk_stats():
    global diskstats
    diskstats = {}
    output = subprocess.Popen(['iostat' , '-x', '-d', '1' , '-N', '4'] , stdout=subprocess.PIPE ).communicate()[0]
    lastupdate_time = time.time()
    linestemp = re.split('\n+', output)
    linetempc = len(linestemp)
    i = 0
    lastdevice_i = 0
    while i < linetempc:
        if linestemp[i].startswith('Device:'):
            lastdevice_i = i
        i += 1
    i  = lastdevice_i
    lines = []
    while i < linetempc:
        lines.append(linestemp[i])
        i += 1
    device_found = False
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line.startswith('Device:'):
            device_found = True
            continue
        if not device_found:
            continue
        elems = re.split('\s+' , line)
        if len(elems) != 14:
            continue
        diskstats[elems[0]] = {'rrqm_sec' : elems[1], 'wrqm_sec' : elems[2], 'read_sec' : elems[3], 
                'write_sec' : elems[4], 'read_sector_kb_sec' : elems[5], 'write_sector_kb_sec' :
                elems[6], 'avgrq-sz' : elems[7], 'avgqu-sz' : elems[8], 'await' : elems[9], 
                'r_awit' : elems[10], 'w_await' : elems[11], 'svctm' : elems[12], 'percentutil' : elems[13]}

def diskstatfun(name):
    if time.time() > (lastupdate_time + 10):
        get_disk_stats()
    device, metrc = name.split('__')
    if device not in diskstats:
        return -11111.1111
    return float(diskstats[device][metrc])
    
def metric_init(params):
    global descriptors
    get_disk_stats()
    if 'disks' in params:
        disks = params['disks']
        alldisks = re.split(',+', disks)
        for dsk in alldisks:
            dsk = dsk.strip()
            if dsk == '':
                continue
            for metric_name in metric_elems:
                unittype = metric_elems[metric_name]
                dsc = {'name': dsk + '__' + metric_name,
                    'call_back': diskstatfun,
                    'time_max': 90,
                    'value_type': 'float',
                    'units': unittype,
                    'slope': 'both',
                    'format': '%f',
                    'description': 'Disk I/O ',
                    'groups': 'Disk I/O Example'}
                descriptors.append(dsc)
        return descriptors
    def metric_cleanup():
        pass

if __name__ == '__main__':
    params = {'disks': 'scd0,sda'}
    metric_init(params)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %6.2f' % (d['name'], v)
