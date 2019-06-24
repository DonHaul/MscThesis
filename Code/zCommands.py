import threading
import cv2
import Queue as queue
import datetime
import time

import open3d

from libs import *

import rospy

def worker(invoker,stop):

    x=""

    while True:

        x= raw_input("Enter command")

        commands = x.split()
        invoker.execute(commands[0],commands[1:])


        if stop():
            break




"""
Encapsulate a request as an object, thereby letting you parameterize
clients with different requests, queue or log requests, and support
undoable operations.
"""

import abc
import time


class Invoker:
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
            self._commands = {}
            self._history = []

    @property
    def history(self):
        return self._history

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name,*args):
        if command_name in self._commands.keys():
            self._history.append((time.time(), command_name,args))
            self._commands[command_name].execute(args)
        else:
            print("Command  not recognised")


class Command(object):
    """
    Declare an interface for executing an operation.
    """
    #__metaclass__ = abs.ABCMeta

    def __init__(self, receiver):
        self._receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass




class Receiver:
    """
    Know how to perform the operations associated with carrying out a
    request. Any class may serve as a Receiver.
    """

    def help(self,*args):
        print("No one is here to help you")

    def help1(self,*args):
        print("No one is here to help you",args)

    def help2(self,*args):
        print("No one is here to help you",args[0],args[1])

class CalculateRotations(Command):
    
    def __init__(self, posescalculator):
        self._posescalc = posescalculator

    def execute(self,*args):
        self._posescalc.CalcRthenStartT()

class CalculateTranslations(Command):
    
    def __init__(self, state ):
        self._state = state

    def execute(self,*args):
        statev.posescalculator.CalcT()
        rospy.signal_shutdown("Successful T")
        statev.stop_threads=True

class HelpCommand(Command):
    """A Command object, which implemets the ICommand interface"""

    def __init__(self, light):
        self._light = light

    def execute(self,*args):
        self._light.help(args)

class Help1Command():
    """A Command object, which implemets the ICommand interface"""

    def __init__(self, light):
        self._light = light

    def execute(self,*args):
        print(args)
        self._light.help1(args)





def Start(statev,stop):
    print("Starting Commandline")

    receiver = Receiver()


    invoker = Invoker()
    invoker.register("R",CalculateRotations(statev.posescalculator))
    invoker.register("T",CalculateTranslations(statev))
    invoker.register("help",HelpCommand(receiver))


    t1 = threading.Thread(target=worker,args=(invoker,stop,))
    t1.start()