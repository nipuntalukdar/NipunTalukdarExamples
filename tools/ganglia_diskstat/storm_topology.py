import re
import pickle
import copy
from time import time
from thrift import Thrift
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from stormpy.storm import Nimbus, ttypes

descriptors = list()
topology = ''
serialfile_dir = '/tmp'
topology_summary_cols_map = {'status' : 'Status', 'num_workers' : 'Worker Count', \
        'num_executors' : 'Executor count', 'uptime_secs': 'Uptime', 'num_tasks' : 'Task count'}

spout_stats = {'Executors' : ['Count', '%u'], 'Tasks' : ['Count', '%u'],
                'Emitted' : ['Count', '%u'], 
                'Transferred' : ['Count', '%u'], 
                'Complete Latency' : ['ms', '%f'],
                'Acked' : ['Count', '%u'],
                'Failed' : ['Count', '%f']}

bolt_stats = {'Executors' : ['Count', '%u'], 'Tasks' : ['Count', '%u'],
                'Emitted' : ['Count', '%u'], 
                'Executed' : ['Count', '%u'], 
                'Transferred' : ['Count', '%u'], 
                'Execute Latency' : ['ms', '%f'],
                'Process Latency' : ['ms', '%f'],
                'Acked' : ['Count', '%u'],
                'Failed' : ['Count', '%f']}

overall = { 'Executor count' : ['Count' , '%u'],
            'Worker count' : ['Count', '%u'],
            'Task count' : ['Count', '%u'],
            'Uptime secs' : ['Count', '%u'] }

boltspoutstats = {}
overallstats = {}
component_task_count = {}
component_exec_count = {}
lastchecktime = 0
maxinterval = 4
bolt_array = []
spout_array = []


def normalize_stats(stats):
    pass
def freshen():
    global lastchecktime
    if time() > (lastchecktime + maxinterval):
        lastchecktime = time()
        boltspoutstats.clear()
        overallstats.clear()
        component_task_count.clear()
        component_exec_count.clear()
        get_topology_stats(topology)
        savedlastchecktime = 0
        tmpsavestats = None
        inf = open('/tmp/save_stats_for' + topology + '.pk', 'rb')
        if inf is not None:
            try:
                tmpsavestats = pickle.load(inf)
                savedlastchecktime = pickle.load(inf)
            except EOFError as e:
                pass
            inf.close()
        of = open('/tmp/save_stats_for' + topology + '.pk', 'wb')
        if of is not None:
            pickle.dump(boltspoutstats, of)
            pickle.dump(lastchecktime, of)
            of.close()
        if overallstats['Uptime secs'] > (lastchecktime - savedlastchecktime):
            if tmpsavestats is not None:
                for bolt in bolt_array:
                    if bolt in tmpsavestats and bolt in boltspoutstats:
                        stats_new = boltspoutstats[bolt]
                        stats_old = tmpsavestats[bolt]
                        for key in bolt_stats:
                            if key == 'Execute Latency' or key == 'Process Latency': continue
                            if key not in tmpsavestats: continue
                            if key not in boltspoutstats: continue
                            stats_new[key] -= stats_old[key]
                for spout in spout_array:
                    if spout in tmpsavestats and spout in boltspoutstats:
                        stats_new = boltspoutstats[spout]
                        stats_old = tmpsavestats[spout]
                        for key in spout_stats:
                            if key == 'Complete Latency': continue
                            if key not in stats_new: continue
                            if key not in stats_old: continue
                            stats_new[key] -= stats_old[key]
                normalize_stats(boltspoutstats, lastchecktime - savedlastchecktime)
            else:
                normalize_stats(boltspoutstats, overallstats['Uptime secs'])
        else:
            normalize_stats(boltspoutstats, overallstats['Uptime secs'])
                
def get_avg(arr):
    if len(arr) < 1:
        return 0
    return sum(arr) / len(arr)

def callback_boltspout(name):
    freshen()
    bolt, statname = name.split('_')
    return boltspoutstats[bolt][statname]

def callback_overall(name):
    freshen()
    return overallstats[name]

def update_task_count(component_name, count):
    if component_name not in component_task_count:
        component_task_count[component_name] = 0
    component_task_count[component_name] += count
    
def update_exec_count(component_name, count):
    if component_name not in component_exec_count:
        component_exec_count[component_name] = 0
    component_exec_count[component_name] += count

def update_whole_num_stat_special(stats, store, boltname, statname):
    if  boltname not in store: 
        store[boltname] = {}
    if statname not in store[boltname]:
        store[boltname][statname] = 0
    for k in stats:
        if k == '__metrics' or k == '__ack_init' or k == '__ack_ack': continue
        store[boltname][statname] += stats[k]

def update_whole_num_stat(stats, store, boltname, statname):
    if  boltname not in store: 
        store[boltname] = {}
    if statname not in store[boltname]:
        store[boltname][statname] = 0
    for k in stats:
        store[boltname][statname] += stats[k]

def update_avg_stats(stats, store, boltname, statname):
    if  boltname not in store: 
        store[boltname] = {}
    if statname not in store[boltname]:
        store[boltname][statname] = []
    for k in stats:
        store[boltname][statname].append(stats[k])

def get_topology_stats(toplogyname):
    try:
        transport = TSocket.TSocket('127.0.0.1' , 6627)
        framedtrasp = TTransport.TFramedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(framedtrasp)
        client = Nimbus.Client(protocol)
        framedtrasp.open()

        ret = client.getClusterInfo()
        for tsummary in ret.topologies:
            if tsummary.name == toplogyname:
                overallstats['Executor count'] = tsummary.num_executors
                overallstats['Task count'] = tsummary.num_tasks
                overallstats['Worker count'] = tsummary.num_workers
                overallstats['Uptime secs'] = tsummary.uptime_secs
                tinfo = client.getTopologyInfo(tsummary.id)
                for exstat in tinfo.executors:
                    stats = exstat.stats
                    update_whole_num_stat_special(stats.emitted["600"], boltspoutstats,
                            exstat.component_id, 'Emitted')
                    update_whole_num_stat_special(stats.transferred["600"], boltspoutstats,
                            exstat.component_id, 'Transferred')

                    numtask = exstat.executor_info.task_end - exstat.executor_info.task_end + 1
                    update_task_count(exstat.component_id, numtask)
                    update_exec_count(exstat.component_id, 1)
                    if stats.specific.bolt is not None:
                        update_whole_num_stat(stats.specific.bolt.acked["600"], boltspoutstats,
                                exstat.component_id, 'Acked')
                        update_whole_num_stat(stats.specific.bolt.failed["600"], boltspoutstats,
                                exstat.component_id, 'Failed')
                        update_whole_num_stat(stats.specific.bolt.executed["600"], boltspoutstats,
                                exstat.component_id, 'Executed')
                        update_avg_stats(stats.specific.bolt.process_ms_avg["600"], boltspoutstats,
                                exstat.component_id, 'process_ms_avg')
                        update_avg_stats(stats.specific.bolt.execute_ms_avg["600"], boltspoutstats,
                                exstat.component_id, 'execute_ms_avg')
                    if stats.specific.spout is not None:
                        update_whole_num_stat(stats.specific.spout.acked["600"], boltspoutstats,
                                exstat.component_id, 'Acked')
                        update_whole_num_stat(stats.specific.spout.failed["600"], boltspoutstats,
                                exstat.component_id, 'Failed')
                        update_avg_stats(stats.specific.spout.complete_ms_avg["600"], boltspoutstats,
                                exstat.component_id, 'complete_ms_avg')
        
        if '__acker' in boltspoutstats:
            del boltspoutstats['__acker']
        for key in boltspoutstats:
            if 'complete_ms_avg' in boltspoutstats[key]:
                avg = get_avg(boltspoutstats[key]['complete_ms_avg'])
                boltspoutstats[key]['Complete Latency'] = avg
            if 'process_ms_avg' in boltspoutstats[key]:
                avg = get_avg(boltspoutstats[key]['process_ms_avg'])
                boltspoutstats[key]['Process Latency'] = avg
            if 'execute_ms_avg' in boltspoutstats[key]:
                avg = get_avg(boltspoutstats[key]['execute_ms_avg'])
                boltspoutstats[key]['Execute Latency'] = avg

        for key in component_task_count:
            if key in boltspoutstats:
                boltspoutstats[key]['Tasks'] = component_task_count[key]
        for key in component_exec_count:
            if key in boltspoutstats:
                boltspoutstats[key]['Executors'] = component_exec_count[key]

        framedtrasp.close()

    except Exception as e:
        print e

def metric_init(params):
    global descriptors
    global topology
    groupname = 'Storm Topology'
    if 'topology' in params and len(params['topology']):
        groupname =  params['topology']
    else:
        return
    topology = groupname
    if 'spouts' in params:
        global spout_array
        spout_array = re.split('[,]+', params['spouts'])
        for spout in spout_array:
            for statname in spout_stats:
                d = {'name' : spout + '_' + statname, 'call_back' : callback_boltspout,
                    'time_max': 90,
                    'value_type': spout_stats[statname][0],
                    'units': 'Count',
                    'slope': 'both',
                    'format': spout_stats[statname][1],
                    'description': '',
                    'groups': groupname}
                descriptors.append(d)

    if 'bolts' in params:
        global bolt_array
        bolt_array = re.split('[,]+', params['bolts'])
        for bolt in bolt_array:
            for statname in bolt_stats:
                d = {'name' : bolt + '_' + statname, 'call_back' : callback_boltspout,
                    'time_max': 90,
                    'value_type': bolt_stats[statname][0],
                    'units': 'Count',
                    'slope': 'both',
                    'format': bolt_stats[statname][1],
                    'description': '',
                    'groups': groupname}
                descriptors.append(d)

    for key in overall:
        d = {'name' : key, 'call_back' : callback_overall,
            'time_max': 90,
            'value_type': overall[key][0],
            'units': 'Count',
            'slope': 'both',
            'format': overall[key][1],
            'description': '',
            'groups': groupname} 
        descriptors.append(d)

if __name__ == '__main__':
    params = {'spouts': 'SampleSpoutTwo', 'bolts' : 'boltc', 'topology' : 'SampleTopology'}
    metric_init(params)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print d['name'], v
