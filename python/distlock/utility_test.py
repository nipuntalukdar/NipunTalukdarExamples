from struct import pack, unpack
import utility


def test1():
    msg = utility.get_lockDetail_msg(1, 'abcdef')
    print type(msg)
    ex = utility.unpack_protocol_msg(msg)
    if ex is None:
        print 'Could not decode protocol message'
    else:
        print ex

test1()
