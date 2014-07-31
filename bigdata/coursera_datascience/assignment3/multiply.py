import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    if record[0] == 'a':
        i = 0
        cell = { 'a' : [record[1], record[2], record[3]]}
        while i < 5:
            mr.emit_intermediate((record[1], i), cell)  
            i += 1
    if record[0] == 'b':
        i = 0
        while i < 5:
            cell = { 'b' : [record[1], record[2], record[3]]}
            mr.emit_intermediate((i, record[2]), cell)  
            i += 1

def reducer(key, list_of_values):
    amap = {}
    bmap = {}
    sum = 0
    for elem in list_of_values:
        if 'a' in elem:
            amap[(elem['a'][0], elem['a'][1])] = elem['a'][2]
        elif 'b' in elem:
            bmap[(elem['b'][0], elem['b'][1])] = elem['b'][2]
    for k, v in amap.items():
        if ((k[1], key[1])) in bmap:
            sum += v * bmap[(k[1], key[1])]
    mr.emit((key[0], key[1], sum))
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  inputdata.close()
