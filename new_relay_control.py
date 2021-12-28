# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import serial
from time import sleep

'''
2路继电器开关控制函数，单独继电器开关控制和全部开关控制
'''
class relay(object):
    def __init__(self):
        self.relay_all_on_order = ['02 05 00 00 FF 00 8C 09', '02 05 00 01 FF 00 DD C9', '02 0F 00 00 00 08 01 FF FE C0']
        self.relay_all_off_order = ['02 05 00 00 00 00 CD F9', '02 05 00 01 00 00 9C 39', '02 0F 00 00 00 08 01 00 BE 80']
        self.relay1 = 1
        self.relay2 = 2
        self.all_relay = 3
        self.port = '/dev/ttyAMA0'
        
    def relay_send(self, send_order):

       if self.port:
           relay_serial = serial.Serial(self.port, 9600)
           GPIO.setmode(GPIO.BCM)
           GPIO.setup(17, GPIO.OUT)
           if not relay_serial.isOpen():
               relay_serial.Open()
           while True:
               GPIO.output(17, GPIO.HIGH)
               sleep(0.01)
               relay_serial.write(bytes.fromhex(send_order))
               #relay_serial.write(bytes(send_order))
               sleep(0.01)
               GPIO.output(17, GPIO.LOW)
               count = relay_serial.inWaiting()
               if count > 0:
                   GPIO.output(17, GPIO.LOW)
                   sleep(0.01)
                   recv = relay_serial.read(count)
                   GPIO.output(17, GPIO.HIGH)
                   sleep(0.01)
                   print("recv: ", recv)
                   # recv_bytes = binascii.b2a_hex(recv)
                   # recv_str = binascii.b2a_hex(recv_bytes).decode('utf-8')
                   recv_str = str(recv.hex())
                   print("recv_str: ", recv_str)
                   print("recv_str: ", recv_str)
                   if recv_str == "00":
                       print("error")
                   else:
                       return recv_str
                   return recv_str
               sleep(0.5)
               #relay_serial.close()

    def ALL_ON(self):
        send_order = self.relay_all_on_order[self.all_relay - 3]
        print(send_order)
        get_return = self.relay_send(send_order)
        print("继电器控制: ALL_RELAY_ON")
        return get_return

    def ALL_OFF(self):
        send_order = self.relay_all_off_order[self.all_relay - 3]
        get_return = self.relay_send(send_order)
        print("继电器控制: ALL_RELAY_OFF")
        return get_return

    def RELAY1_ON(self):
        send_order = self.relay_all_on_order[self.relay1  - 1]
        get_return = self.relay_send(send_order)
        print("继电器控制: RELAY1_ON")
        return get_return

    def RELAY1_OFF(self):
        send_order = self.relay_all_off_order[self.relay1 - 1]
        get_return = self.relay_send(send_order)
        print("继电器控制: RELAY1_OFF")
        return get_return

    def RELAY2_ON(self):
        send_order = self.relay_all_on_order[self.relay2 - 1]
        get_return = self.relay_send(send_order)
        print("继电器控制: RELAY2_ON")
        return get_return

    def RELAY2_OFF(self):
        send_order = self.relay_all_off_order[self.relay2 - 1]
        get_return = self.relay_send(send_order)
        print("继电器控制: RELAY2_OFF")
        return get_return

# if __name__ == "__main__":
    # relay = relay()
    # relay.port = '/dev/ttyAMA0'
    




