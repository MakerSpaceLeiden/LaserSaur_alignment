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
import math

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
	self.power_ = 0.4
        self.returnval = None
        self.X = 0
        self.Y = 0

    def open(self):
        self.ser.close()
        self.ser.open()

    def close(self):
        self.ser.close()

    @property
    def power(self):
    	return self.power_
    
    @power.setter
    def power(self, p):
    	self.power_ = p
    	#add checks etc..
    	try:
    	    self.command = "S{0}".format(int(p*255))
    	except:
    	    print ("Wrong power setting")

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

    def movetoxy(self, x, y, laser=0):
    	if ((x<Const.MINX) or (x>Const.MAXX)): return -1
    	if ((y<Const.MINY) or (1>Const.MAXY)): return -1
	self.command = "G90"
    	self.command = "G{0} X{1} Y{2}".format(laser, x, y)

    def lr(self):
    	self.movetoxy(Const.MAXX, Const.MAXY)

    def ll(self):
        self.movetoxy(Const.MINX, Const.MAXY)

    def ul(self):
        self.movetoxy(Const.MINX, Const.MINY)
        
    def ur(self):
        self.movetoxy(Const.MAXX, Const.MINY)

    def circle(self, r, x, y, N):
    	self.movetoxy(x, y)
    	for i in range(N):
    	    alpha = 1.0*i/N*2.0*3.1415926535
    	    X = r * math.cos(alpha)+x
    	    Y = r * math.sin(alpha)+y
    	    self.movetoxy(X, Y, laser=1)

    def roundtrip(self):
        self.movetoxy(Const.MINX, Const.MINY)
        self.movetoxy(Const.MINX, Const.MAXY)
        self.movetoxy(Const.MAXX, Const.MAXY)
        self.movetoxy(Const.MAXX, Const.MINY)
        self.movetoxy(Const.MINX, Const.MINY)

    def laser(self, dx, dy):
    	#with laser on, move relative dx, dy
        self.command = "G91"
        self.command = "G1 X0 Y0"
        self.command = "G1 X{0} Y{1}".format(dx, dy)

    def leftvertical(self, direction=0):
    	self.power = 0.4
    	dx = 0
    	if direction == 0:
    	    dy = "10"
            self.ul()
        else:
            dy = "-10"
            self.ll()
	self.laser(dx, dy)
        #self.pulse()
        self.command = "G90"
        if direction == 0:
            dy = "-10"
            self.ll()
        else:
            dy = "10"
            self.ul()
        self.laser(dx, dy)
        #self.pulse()
        
    def lowerhorizontal(self, direction=0):
    	self.power = 0.4
	dy = "0"
    	if direction == 0:
    	    dx = "30"
            self.ll()
        else:
            dx = "-30"
            self.lr()
	self.laser(dx, dy)
        #self.pulse()
        self.command = "G90"
        if direction == 0:
            dx = "-30"
            self.lr()
        else:
            dx = "30"
            self.ll()
	self.laser(dx, dy)
        #self.pulse()
    
    def rightvertical(self):
    	self.power = 0.4
        self.ur()
        self.laser(0, 10)
        #self.pulse()
        self.command = "G90"
        self.lr()
	self.laser(0, -10)
	#self.pulse()    
        
    def lowerhorizontal_(self, direction =0):
    	self.power = 0.4
        self.ll()
	self.laser(10,0)
        self.command = "G90"
        self.lr()
	self.laser(-10,0)
        self.command = "G90"
        
    def upperhorizontal(self):
    	self.power = 0.4
        self.ul()
	self.laser(10,0)
        self.command = "G90"
        self.ur()
	self.laser(-10,0)
        self.command = "G90"
        
    def pulse(self):
    	pass
    	#NYI
        #self.command="G4 P0.5"

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
            opts, args = getopt.getopt(self.argv,"hRlrudc:",["ifile=","ofile="])
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
            if opt == '-R':
                print "resetting.."
            	lsxs.reset()
            if opt == '-l':
            	lsxs.leftvertical()
            if opt == '-r':
            	lsxs.rightvertical()
            if opt == '-u':
            	lsxs.upperhorizontal()
            if opt == '-d':
            	lsxs.lowerhorizontal()

if __name__=='__main__':
    instance = Lsxs()
    arghandler = Handleargs(sys.argv[1:])
    arghandler.process(instance)
    #instance.reset()
    s = raw_input()
    instance.close()
