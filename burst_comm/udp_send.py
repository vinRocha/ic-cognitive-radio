#!/usr/bin/env/ python2

import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 52001

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_continuous(MESSAGE):
  while True:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(3)
  return

def send(MESSAGE):
  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
  return
