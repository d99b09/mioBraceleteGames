import socket
import time
from threading import Thread
import serial
import json

class Mio_API_get_data(Thread):
    def __init__(self):
        super(Mio_API_get_data, self).__init__()
        self.ser = serial.Serial()
        self.ser.port = 'COM6'
        self.ser.baudrate = 115200
        self.decode_message1 = {'x': 0, 'y': 0, 's': 0}  # new decode fun
        self.decode_message2 = {'x': 0, 'y': 0, 's': 0}  # new decode fun
        print('init')


    def string_to_json(self, line):
        decode_line = line.decode()
        s_list = decode_line.split(',')[:-1]
        i_list = []
        for i in s_list:
            try:
                i_list.append(int(i))
            except:
                pass
        if i_list[1]:
            self.decode_message1['y'] = i_list[2]
            self.decode_message1['x'] = i_list[3]
        else:
            self.decode_message2['x'] = -i_list[2]
            self.decode_message2['y'] = i_list[3]
        # elif i_list[0] == 144:
        #     self.decode_message1['s'] = i_list[4]
        # elif i_list[0] == 145:
        #     self.decode_message2['s'] = i_list[4]
        return self.decode_message1, self.decode_message2

    def run(self) -> None:
        while True:
            try:
                print(f'Trying to open port {self.ser.port}')
                self.ser.open()
                print('ser opened ')
                line = self.ser.readline()
                print(f'Data: {line}')
                while True:
                    line = self.ser.readline()
                    print(line)

                    try:
                        m1, m2 = self.string_to_json(line)
                        message = {'r': m1, 'l': m2}
                        print(message)
                        msg = json.dumps(message)
                        self.send_msg(msg)
                    except:
                        pass
            except:
                time.sleep(3)
                self.ser.close()

    def send_msg(self, msg):
        self.client = socket.socket()
        self.client.connect(('localhost', 8888))
        self.client.send(msg.encode())
        self.client.close()


if __name__ == '__main__':
    dater = Mio_API_get_data()
    dater.start()