#!/usr/bin/env/ python2

from timeout import Timeout
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 52002

print "UDP listening IP:", UDP_IP
print "UDP listening port:", UDP_PORT

def receive(sec):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    with Timeout(sec):
      sock.bind((UDP_IP, UDP_PORT))
      data, addr = sock.recvfrom(1024)
      return data
  except Timeout.Timeout:
    return None