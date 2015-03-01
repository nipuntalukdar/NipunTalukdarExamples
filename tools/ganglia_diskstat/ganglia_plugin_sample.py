import sys
import os
import random

descriptors = list()
firstparam_max = 1000
secondparam_max = 1000

def callback_fun1(name):
    '''
    Returns a random number between 1 and firstparam_max
    '''
    random.seed()
    return random.randint(1, firstparam_max)

def callback_fun2(name):
    '''
    Returns a random number between 5 and secondparam_max
    '''
    random.seed()
    return random.randint(5,secondparam_max)

def metric_init(params):
    global descriptors, firstparam_max, secondparam_max
    if 'firstparam' in params:
        firstparam_max = int(params['firstparam'])
        d = {'name': 'firstparam',
                'call_back': callback_fun1,
                'time_max': 90,
                'value_type': 'uint',
                'units': 'Count',
                'slope': 'both',
                'format': '%u',
                'description': 'Sample metric',
                'groups': 'Sample'}
        descriptors.append(d)
    
    if 'secondparam' in params:
        secondparam_max = int(params['secondparam'])
        d = {'name': 'secondparam',
                'call_back': callback_fun2,
                'time_max': 90,
                'value_type': 'uint',
                'units': 'Count',
                'slope': 'both',
                'format': '%u',
                'description': 'Sample metric',
                'groups': 'Sample'}
        descriptors.append(d)
    return descriptors

    def metric_cleanup():
        '''
        We don't need any cleanup :) :)
        '''
        pass


# This routine is for debugging purpose only and not used by gmond
# To debug the output, run as below:
# $ python ganglia_plugin_sample.py
if __name__ == '__main__':
    params = {'firstparam': 100, 'secondparam' : 500}
    metric_init(params)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print '%s --> %u' % (d['name'], v)
