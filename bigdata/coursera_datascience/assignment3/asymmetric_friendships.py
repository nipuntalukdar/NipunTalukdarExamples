import MapReduce
import sys


mr = MapReduce.MapReduce()


def mapper(record):
    # record]0]: name
    # record[1]: friend
    sortrec  = record[:]
    sortrec.sort()
    mr.emit_intermediate((sortrec[0], sortrec[1]), record)

def reducer(key, list_of_values):
    emit_it = False
    if [ key[0], key[1] ] not in list_of_values:
        emit_it = True
    elif [ key[1] , key[0] ] not in list_of_values:
        emit_it = True
    if emit_it:
        mr.emit((key[0], key[1]))
        mr.emit((key[1], key[0]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  inputdata.close()
