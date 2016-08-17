import socket
'''
    leader_takes an array of (host, port) tuples and returns leader, array-of-followers,
    array-of-down-hosts
'''
def leader_detect(hostports):
    sk = None
    leader = None
    followers = []
    down = []
    for hp in hostports:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sk.connect(hp)
            sk.send(b'isro')
            resp = sk.recv(1024)
            if resp == r'rw':
                leader = hp
            else:
                followers.append(hp)
                
        except Exception as e:
            down.append(hp)
        if sk:
            sk.close()
    return leader, followers, down

## Sample run....
leader, followers, downs = leader_detect([('zk-serveer1-host', 2181), ('zkserver-2-host', 2181)])
print 'leader: {}, followers:{}, downs: {}'.format(leader, followers, downs)
