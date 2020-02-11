import asyncio
import io

import serial_asyncio


class Output(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        # print('port opened', transport)
        transport.serial.rts = False

    def data_received(self, data):
        sio = io.TextIOWrapper(io.BytesIO(data))
        self.buffer.append(sio.readline())
        # print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def eof_received(self):
        print(self.buffer)

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')


loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(
    loop, Output, '/dev/ttyS0', baudrate=9600)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
