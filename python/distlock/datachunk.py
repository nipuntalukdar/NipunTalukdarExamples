#!/usr/bin/env python

from io import BytesIO
from struct import pack, unpack


class DataChunk:
    
    def __init__(self):
        self.times = 0
        self.expect_new = True
        self.current_msg_len = 0
        self.current_buffer = BytesIO()

    def handle_msg(self, data):
        self.handle_chunk(data)
    
    def handle_chunk(self, data):
        self.times += 1
        print len(data)
        
    def process_chunk(self, data):
        datalen = len(data)
        if self.expect_new:
            if datalen >= 4:
                self.current_msg_len = unpack('i', data[0:4])[0]
                if (self.current_msg_len + 4) == datalen:
                    # We got the entire packet 
                    self.handle_msg(data[4:])
                    return
                elif (self.current_msg_len + 4) > datalen:
                    # We need some more bytes
                    self.current_buffer.write(data[4:])
                    self.expect_new = False
                else:
                    # We may have got more than one message
                    start = 4
                    while True:
                        self.handle_msg(data[start : start + self.current_msg_len])
                        start = start + self.current_msg_len
                        if start == datalen:
                            # We finished all the bytes and there is no incomplete messages
                            # in the bytes
                            self.expect_new = True
                            self.current_msg_len = -1
                            self.current_buffer = BytesIO()
                            break
                        if 4 <= (datalen - start):
                            self.current_msg_len = unpack('i', data[start : start + 4])[0]
                            start += 4
                            if (datalen - start) >= self.current_msg_len:
                                # we have this message also in this buffer
                                continue
                            else:
                                # This message is incomplete, wait for the next chunk
                                self.expect_new = False
                                self.current_buffer = BytesIO()
                                self.current_buffer.write(data[start:])
                                break
                        else:
                            # we don't even know the size of the current buffer
                            self.current_msg_len = -1
                            self.current_buffer = BytesIO()
                            self.current_buffer.write(data[start:])
                            self.expect_new = False
                            break
            else:
                # We haven't even received 4 bytes of data for this brand new 
                # packet
                self.expect_new = False
                self.current_buffer = BytesIO()
                self.current_buffer.write(data)
                self.current_msg_len = -1
        else:
            # Not a new message
            start = 0
            if self.current_msg_len == -1:
                # try to get the message len
                if datalen >= (4 - self.current_buffer.tell()):
                    #get the length of the data
                    start = 4 - self.current_buffer.tell()
                    self.current_buffer.write(data[0: start])
                    self.current_buffer.seek(0)
                    self.current_msg_len = unpack('i', self.current_buffer.read())[0]
                    self.current_buffer = BytesIO()
                else:
                    # Till now even the size of the data is not known
                    self.current_buffer.write(data)
                    return
            while start < datalen:
                if self.current_buffer is None:
                    self.current_buffer = BytesIO()
                if self.current_msg_len == -1:
                    if (datalen - start) < 4:
                        self.current_buffer.write(data[start:])
                        break
                    elif (datalen - start) == 4:
                        self.current_msg_len = unpack('i', data[start:])[0]
                        break
                    else:
                        self.current_msg_len = unpack('i', data[start: start + 4])[0]
                        start += 4
                if (datalen - start) >= (self.current_msg_len - self.current_buffer.tell()):
                    consume = self.current_msg_len -  self.current_buffer.tell()
                    self.current_buffer.write(data[start: start + consume])
                    start += consume
                    self.current_msg_len = - 1
                    self.current_buffer.seek(0)
                    self.handle_msg(self.current_buffer.read())
                    self.current_buffer = BytesIO()
                    if start == datalen:
                        self.expect_new = True
                else:
                    self.current_buffer.write(data[start:])
                    break
