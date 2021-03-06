#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
from ikabot.helpers.botComm import *

def create_handler(s):
	def _handler(signum, frame):
		raise Exception('Señal recibida número {:d}'.format(signum))
	return _handler

def setSignalsHandlers(s):
	signals = [signal.SIGHUP, signal.SIGQUIT, signal.SIGABRT, signal.SIGTERM]
	for sgn in signals:
		signal.signal(sgn, create_handler(s))

def setInfoSignal(s, info): # el proceso explica su funcion por stdout
	info = 'información del proceso {}:\n{}'.format(os.getpid(), info)
	def _sendInfo(signum, frame):
		sendToBot(info)
	signal.signal(signal.SIGUSR1, _sendInfo) # kill -SIGUSR1 pid
