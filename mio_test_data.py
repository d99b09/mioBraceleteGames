import socket
import time
from threading import Thread
import json


class Mio_API_get_test_data(Thread):
    def __init__(self):
        super(Mio_API_get_test_data, self).__init__()
        self.last_msg = json.dumps({'x': 0, 'y': 0, 's': 0})
        self.is_open = False
        self.msg = '0'
        self.sleep_time = 0
        self.decode_message1 = {'x': 0, 'y': 0, 's': 0}  # new decode fun
        self.decode_message2 = {'x': 0, 'y': 0, 's': 0}  # new decode fun

        self.msg_whiting = False

    def test_tact(self, m1: dict, m2: dict, t: float):
        self.decode_message1 = m1
        self.decode_message2 = m2
        message = {'r': m1, 'l': m2}
        msg = json.dumps(message)
        print(f'Messege:{msg}')
        self.last_msg = msg
        time.sleep(t)
        return msg

    def run(self) -> None:
        while True:
            send_msg = self.test_tact({'x': 0, 'y': 0, 's': 0}, {'x': 0, 'y': 0, 's': 0}, 0.1)
            self.you_send_def(send_msg)
            send_msg = self.test_tact({'x': 800, 'y': 0, 's': 0}, {'x': 122, 'y': 0, 's': 0},  0.1)
            self.you_send_def(send_msg)

    def you_send_def(self, send_msg):
        client = socket.socket()
        client.connect(("192.168.1.130", 8888))
        client.send(send_msg.encode())
        client.close()
        pass

    def get_last_msg(self):
        return self.last_msg

    def set_port(self, port: str):
        pass

    def get_decode_message(self):
        return self.decode_message

    def band_connect(self, cmd):
        pass


if __name__ == '__main__':
    dater = Mio_API_get_test_data()
    dater.start()
