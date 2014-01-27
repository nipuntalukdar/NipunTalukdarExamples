'''
It is a tool to generate and manage storm clusters

@author: Nipun Talukdar
'''

import yaml
import sys
import os


def process_element(key, value, confmap):
    if key == 'zkserver':
        process_zk_servers(value, confmap)
        
    elif key == 'zkport':
        process_zk_port(value, confmap)
        
    elif key == 'nimbus':
        process_nimbus_host(value, confmap)
        
    elif key == 'stormlocal':
        process_storm_localdir(value, confmap)
        
    elif key == 'javalibpath':
        process_java_libpath(value, confmap)
        
    elif key == 'drpcservers':
        process_drpcservers(value, confmap)
    elif key == 'supervisorports':
        process_supervisor_ports(value, confmap)
    else:
        print 'Invalid key ' + key
        sys.exit(1)

def process_supervisor_ports(ports, confmap):   
    if 'supervisor.slots.ports' in confmap:
        return
    allports = ports.split(',')
    uniques = set([])
    for port in allports:
        port = port.strip()
        if port == '':
            continue
        port = int(port)
        if (port < 0) or (port > 65534):
            continue
        uniques.add(port)   
    if len(uniques) == 0:
        print "Invalid value passed for supervisor ports"
        sys.exit(1)
    confmap['supervisor.slots.ports'] = list(uniques)
    
        
def process_drpcservers(servers, confmap):   
    if 'drpc.servers' in confmap:
        return
    allservers = servers.split(',')
    uniques = set([])
    for server in allservers:
        server = server.strip()
        if server == '':
            continue
        uniques.add(server)
    if len(uniques) == 0:
        print "Invalid value passed for drpc serve list"
        sys.exit(1)
    confmap['drpc.servers'] = list(uniques)
        
def process_java_libpath(path, confmap):
    if not 'java.library.path' in confmap:
        confmap['java.library.path'] = path
            
def process_storm_localdir(path, confmap):
    if not 'sstorm.local.dir' in confmap:
        confmap['storm.local.dir'] = path                
        
def process_zk_port(port, confmap):
    if not 'storm.zookeeper.port' in confmap:
        confmap['storm.zookeeper.port'] = port

def process_nimbus_host(host, confmap):
    if not 'nimbus.host' in confmap:
        confmap['nimbus.host'] = host
            
def process_zk_servers(servers, confmap):
    allservers = servers.split(',')
    uniques = set([])
    for server in allservers:
        server = server.strip()
        if server == '':
            continue
        uniques.add(server)
    if len(uniques) == 0:
        print "Invalid value passed for zookeeper serve list"
        sys.exit(1)
    if not 'storm.zookeeper.servers' in confmap:
        confmap['storm.zookeeper.servers'] = list(uniques)


def main():
    if (len(sys.argv) < 2):
        print "Input file name is not given"
        sys.exit(1)
    f = None
    lines = []
    try:
        f = open(sys.argv[1])
        lines = f.readlines()
        f.close()
    except IOError as e:
        if not f == None:
            f.close()
        else:
            print e
        sys.exit(1)
    f.close()
    storm = {}
    required_keys = set(['zkserver', 'zkport', 'stormlocal', \
                        'javalibpath', 'drpcservers', 'nimbus', \
                        'supervisorports' ])
    
    for line in lines:
        line = line.strip()
        if line.find('#') == 0:
            continue
        parts = line.split('=')
        if len(parts) != 2:
            print 'Invalid input ' + line
            sys.exit(1)
        parts[0] = parts[0].strip()
        parts[1] = parts[1].strip()
        if parts[0] == '' or parts[1] == '':
            print 'Invalid input ' + line
            sys.exit(1)
        if not parts[0] in required_keys:
            print 'Invalid key ' + parts[0]
            sys.exit(1)
        process_element(parts[0], parts[1], storm)
        
    x = yaml.dump(storm, default_flow_style=False, width=80, indent=4)
    
    if not 'supervisor.slots.ports' in storm:
        print 'Supervisor ports missing'
        sys.exit(1)
    if not 'storm.zookeeper.servers' in storm:
        print 'Zookeeper server is missing'
        sys.exit(1)
    if not 'nimbus.host' in storm:
        print 'Nimbus server is missing'
        sys.exit(1)
    
    f = open('storm.yaml'  , 'w')
    f.write(x)
    f.close()

#call main    
main()
