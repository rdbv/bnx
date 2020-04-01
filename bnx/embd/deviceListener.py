#!/usr/bin/python3

import os
import socket
import queue
import threading
import logging

import time

import argparse

from datetime import datetime
from command import Command

class DeviceListenerThread(threading.Thread):

    def __init__(self, ifc = '0.0.0.0', port = 8888, photoPath = '/home/void/servers/bnx/photos/'):

        self.photoPath = photoPath
        self.connData = ((ifc, port))
        self.devices = {}

        threading.Thread.__init__(self, daemon = True)
    
    def sendCommand(self, command):
        if command.device in self.devices:
            self.devices[command.device][0].put(command)
            try:
                return self.devices[command.device][1].get(timeout=5)
            except:
                return None
    def getCommand(self, id):
        try:
            return self.devices[id][0].get(timeout = 1)
        except:
            return None

    def addDevice(self, device):
        if device in self.devices:
            logging.info('Device %s already connected', device)
            return False

        self.devices[device] = [queue.Queue(), queue.Queue()]
        return True
    
    def dropDevice(self, device):
        del self.devices[device]
    
    def listDevices(self):
        for name, device in self.devices:
            print(name)

    def run(self):
        logging.info("DeviceListener started")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.connData)
        sock.listen(1)

        while True:
            deviceThread = DeviceThread(sock.accept(), self)
            deviceThread.start()

class DeviceThread(threading.Thread):

    def __init__(self, connData, deviceManager):
        self.connData = connData
        self.deviceManager = deviceManager

        threading.Thread.__init__(self, daemon = True)
    
    def respond(self, data):
        self.deviceManager.devices[self.myId][1].put(data)

    def run(self):

        conn, addr = self.connData
        conn.settimeout(3)

        try:
            self.myId = conn.recv(32).decode().replace('\n','')
        except socket.timeout:
            logging.info('Timeout on ident')
            return

        self.name = 'Device-%s' % self.myId

        logging.info('Connected %s:%s ID:%s', addr[0], addr[1], self.myId)

        if not self.deviceManager.addDevice(self.myId):
            conn.close()
            return

        while True:
            command = self.deviceManager.getCommand(self.myId)
            
            if not self.pingDevice(conn):
                logging.info('Connection dropped (%s)', self.myId)
                break
             
            if command != None:
                if command.getCommand() == 'g':
                    if not self.fetchPhoto(conn, command):
                        break

        self.deviceManager.dropDevice(self.myId)
        conn.close()

            
    def fetchPhoto(self, conn, command):
        logging.info('Fetching photo from %s', self.myId) 
        conn.send(command.getDeviceCommand())
        data = b''
        while True:

            try:
                chunk = conn.recv(1024)
            except socket.timeout:
                return False

            if chunk.find(b'\r\n\r\n') != -1:
                chunk.replace(b'\r\n\r\n',b'')
                data += chunk
                break

            data += chunk
                    
        f = open(self.deviceManager.photoPath + datetime.now().strftime("%d-%m-%Y-%H:%M")+'.jpg', 'wb')
        f.write(data)
        f.close()
        
        logging.info('Photo fetched %s', self.myId)

        self.respond(b'ok')

        return True

    def pingDevice(self, conn, params = None):
        conn.send(b'p')        
        try:
            reply = conn.recv(8)
        except socket.timeout:
            return False 
        return reply == b'1'



