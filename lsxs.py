#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lsxs.py
#  
#  some convenience functions for laser alignment
#
#  Copyright 2016 marcell marosvolgyi
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.import serial
import serial
import sys, getopt
import time

class Dummyserial(object):
	
    def __init__(self):
    	pass
    
    def open(self):
    	pass
    
    def close(self):
    	pass
    
    def write(self, dummyarg):
    	pass

    def readlines(self):
        return "DCX4.995Y5.005V14.11"

class Post(object):

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        mylsxs = args[0]
        #lines = mylsxs.ser.readlines()
        #actual postprocessor here:
        #mylsxs.returnval = lines
        return self.function(*args, **kwargs)

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self(instance, *args, **kwargs)
        wrapper.__doc__ = self.function.__doc__
        wrapper.__name__ = self.function.__name__
        return wrapper

class Const(object):
    MINX = 10
    MINY = 10
    MAXX = 1100
    MAXY = 500

class Lsxs(object):

    def __init__(self):
    	try:
            self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=57600)
        except:
            self.ser = Dummyserial()
	self.open()
	self.speed_ = 2000
        self.returnval = None
        self.X = 0
        self.Y = 0

    def open(self):
        self.ser.close()
        self.ser.open()

    def close(self):
        self.ser.close()


    @property
    def speed(self):
   	return self.speed_

    @speed.setter
    def speed(self, spd):
    	self.speed_ = spd
    	self.command = "F{0}".format(self.speed)
    	
    def reset(self):
        self.command = "G30"

    def home(self):
    	self.movetoxy(Const.MINX, Const.MINY)

    def movetoxy(self, x, y):
    	if ((x<Const.MINX) or (x>Const.MAXX)): return -1
    	if ((y<Const.MINY) or (1>Const.MAXY)): return -1
	self.command = "G90"
    	self.command = "G0 X{0} Y{1}".format(x, y)

    def lr(self):
    	self.movetoxy(Const.MAXX, Const.MAXY)

    def ll(self):
        self.movetoxy(Const.MINX, Const.MAXY)

    def ul(self):
        self.movetoxy(Const.MINX, Const.MINY)
        
    def ur(self):
        self.movetoxy(Const.MAXX, Const.MINY)

    def roundtrip(self):
        self.movetoxy(Const.MINX, Const.MINY)
        self.movetoxy(Const.MINX, Const.MAXY)
        self.movetoxy(Const.MAXX, Const.MAXY)
        self.movetoxy(Const.MAXX, Const.MINY)
        self.movetoxy(Const.MINX, Const.MINY)

    def leftvertical(self):
        self.ul()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X0 Y10"
        #self.pulse()
        self.command = "G90"
        self.ll()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X0 Y-10"
        #self.pulse()
    
    def rightvertical(self):
        self.ur()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X0 Y10"
        #self.pulse()
        self.command = "G90"
        self.lr()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X0 Y-10"
        #self.pulse()    
        
    def lowerhorizontal(self):
        self.ll()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X10 Y0"
        self.command = "G90"
        self.lr()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X-10 Y0"
        self.command = "G90"
        
def upperhorizontal(self):
        self.ul()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X10 Y0"
        self.command = "G90"
        self.ur()
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X-10 Y0"
        self.command = "G90"
        
    def pulse(self):
        self.command="G4 P0.5"

    @property
    def command(self):
        return "enter a gcode command"

    @command.setter
    #@Post
    def command(self,str):
        self.ser.write(str+"\r\n")

    #@Post
    def status(self):
        self.ser.write("?\r\n")
        time.sleep(1)
        line = self.ser.read(self.ser.inWaiting())
        print line
        self.returnval = line
        
    def state(self):
        self.status()

    def report(self):
    	s = self.returnval
        try:
            self.X = s.split("X")[1].split("Y")[0]
            self.Y = s.split("Y")[1].split("V")[0]
        except:
            pass

class Handleargs(object):
	
    #http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    def __init__(self, argv):
        self.argv = argv

    def process(self, lsxs):
        try:
            opts, args = getopt.getopt(self.argv,"hrc:",["ifile=","ofile="])
        except getopt.GetoptError:
             print 'lsxs.py -c <gcode command> '
             sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                f=open('help.txt', 'r')
                for line in f.readlines():
                    print line,
                f.close()
                sys.exit()
            if opt == '-c':
                #arg
                lsxs.command = arg
                print "executed command: {0}".format(arg)
                s = raw_input("press enter>")
                #sys.exit(1)
            if opt == '-r':
                print "resetting.."
            	lsxs.reset()

if __name__=='__main__':
    instance = Lsxs()
    arghandler = Handleargs(sys.argv[1:])
    arghandler.process(instance)
    instance.reset()
    instance.close()
