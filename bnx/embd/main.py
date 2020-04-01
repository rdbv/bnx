#!/usr/bin/python3

import time
import logging
import argparse

from deviceListener import DeviceListenerThread, DeviceThread
from localListener import LocalCommListener

def getArgs():
    p = argparse.ArgumentParser()

    p.add_argument("-r", action='store_true')
    p.add_argument("-p", type=int, default=8888)
    p.add_argument("-i", type=str, default='0.0.0.0')

    return p.parse_args()


args = getArgs()

logging.basicConfig(level=logging.DEBUG)
logging.info('Daemon starting')

deviceListener = DeviceListenerThread()
localListener = LocalCommListener(deviceListener)

deviceListener.start()
localListener.start()

while True:
    time.sleep(0.5)
