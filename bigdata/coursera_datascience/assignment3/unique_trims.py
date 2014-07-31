import MapReduce
import sys


mr = MapReduce.MapReduce()


def mapper(record):
    # record]0]: sequence id
    # record[1]: neucleotides
    mr.emit_intermediate(record[1][: len(record[1]) -10], 1)

def reducer(key, list_of_values):
        mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  inputdata.close()
