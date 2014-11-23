#!/usr/bin/python
import os
import time
from glob import glob
from html import HTML
from os import path
import matplotlib.pyplot as plt

TOPDIR = '/home/geet/data/'
INPUTDIRS = '/home/geet/data/input/'
LASTRUNTIMEFILE = '/home/geet/data/time'
STATDIR = '/home/geet/stats/'
LINESTARTS = "ingesting document:"


def extract_stats(fpath, outdir, legend):
    statmap = {}
    lines = []
    threadids = []
    statdirthis = STATDIR + outdir
    fpaths = fpath.split('/')
    cat = fpaths[len(fpaths) - 1].replace('.txt', '')
    statdirthis = STATDIR + outdir + '/' + cat
    if not path.exists(statdirthis):
        os.makedirs(statdirthis)

    with open(fpath) as f:
        lines = f.readlines()
    for line in lines:
        line = line.lstrip()
        if not line.startswith(LINESTARTS):
            continue
        line = line.replace(LINESTARTS, '').replace(':', ' ')
        sels = line.split()
        if len(sels) != 3:
            continue
        threadid = int(sels[0])
        intid = int(sels[1])
        count = int(sels[2])
        if threadid not in statmap:
            statmap[threadid] = {}
            threadids.append(threadid)
        if intid not in statmap[threadid]:
            statmap[threadid][intid] = count
    cumulative = {}
    startth = 0
    h = HTML('html')
    t = h.table(border='1')
    r = t.tr
    r.td('Thread#')
    r.td('2 minute Intervals#')
    r.td('Doc count')
    for threadid in sorted(statmap):
        startth += 1
        for intid in sorted(statmap[threadid]):
            intcount = statmap[threadid][intid]
            if (intid - 2) in statmap[threadid]:
                intcount -= statmap[threadid][intid - 2]
            r = t.tr
            r.td(str(startth))
            r.td(str(intid))
            r.td(str(intcount))
            if intid not in cumulative:
                cumulative[intid] = intcount
            else:
                cumulative[intid] += intcount
    fp = open(statdirthis + '/allthreads.html', 'w')
    fp.write("%s" % (h))
    fp.close()
    h = None

    # Print cumulative
    xcols = []
    ycols = []
    h = HTML('html')
    t = h.table(border='1')
    r = t.tr
    r.td('2 minute Intervals#')
    r.td('Total Doc count')
    r.td('Doc/Second')
    for intid in sorted(cumulative):
        xcols.append(intid)
        ycols.append(float(cumulative[intid]) / 120.0)
        r = t.tr
        r.td(str(intid))
        r.td(str(cumulative[intid]))
        r.td("%0.2f" % (float(cumulative[intid]) / 120.0))
    fp = open(statdirthis + '/cumulative.html', 'w')
    fp.write("%s" % (h))
    fp.close()
    h = None
    plt.ylabel('doc/sec')
    plt.xlabel('2 min intervals')
    plt.plot(xcols, ycols)
    plt.savefig(statdirthis + '/cumulativegraph.png')
    plt.close()
    legend[cat] = cumulative


def draw_legend(legend, outdir):
    plt.gca().set_color_cycle(['red', 'green',
                              'blue', 'yellow', 'black', 'indigo'])
    plt.xlabel('doc/sec')
    plt.xlabel('2 min intervals')
    legends = []
    for cat in legend:
        xcols = []
        ycols = []
        legends.append(cat)
        for intid in sorted(legend[cat]):
            xcols.append(intid)
            ycols.append(float(legend[cat][intid]) / 120.0)
            plt.plot(xcols, ycols)
    plt.legend(legends)
    plt.savefig(STATDIR + outdir + '/cumulativegraph.png')
    plt.close()


def extract_stat_in_dir(dirpath):
    pathels = dirpath.split('/')
    legend = {}
    outdir = pathels[len(pathels) - 1]
    for f in glob(dirpath + '/*.txt'):
        extract_stats(f, outdir, legend)
    draw_legend(legend, outdir)
    legend = None


def main():
    lastruntime = 0
    try:
        statvals = os.stat(LASTRUNTIMEFILE)
        lastruntime = statvals.st_mtime
    except OSError, e:
        print e
    fp = open(LASTRUNTIMEFILE, 'w')
    fp.write("%d" % (time.time()))

    for d in glob(INPUTDIRS + '*'):
        if not os.path.isdir(d):
            continue
        curdir = d
        statvals = os.stat(curdir)
        if statvals.st_mtime >= lastruntime:
            extract_stat_in_dir(curdir)

if __name__ == '__main__':
    main()
