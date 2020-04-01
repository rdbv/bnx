#!/usr/bin/python3

import os
import socket
import queue
import threading
import logging

import time
import argparse

from command import LocalCommand, Command

class LocalCommListener(threading.Thread):

    def __init__(self, deviceListener, sockName = 'bnx_sock'):
        
        self.sockName = sockName
        self.deviceListener = deviceListener

        try:
            os.unlink(sockName)
        except OSError:
            if os.path.exists(sockName):
                raise

        threading.Thread.__init__(self, daemon = True)

    def run(self):

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.sockName)
        self.sock.listen(1)

        while True:
            localComm = LocalCommThread(self.deviceListener, self.sock.accept())
            localComm.start()



class LocalCommThread(threading.Thread):
    def __init__(self, deviceListener, connData):

        self.connData = connData
        self.deviceListener = deviceListener

        threading.Thread.__init__(self, daemon = True)
    
    def parseMessage(self, message):

        if message == b'' or message == b'\n':
            return None

        if message.count(b' ') < 1:
            return LocalCommand(message.replace(b'\n',b''))

        message = message.replace(b'\n',b'')
        data = message.split(b' ')

        target = data[0].decode()
        commands = data[1].decode()

        return Command(target, commands)

    def run(self):
        conn, addr = self.connData
        
        command = self.parseMessage(conn.recv(64))
    
        if command == None:
            pass
        if type(command) == Command:
            response = self.deviceListener.sendCommand(command)

            if response != None:
                conn.send(response)
            else:
                conn.send(b'timeout')
        elif type(command) == LocalCommand:
            print("Local command.")

        conn.close()

