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
import sys

class Lsxs(object):

    def __init__(self):
        self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=57600)
	self.open()
        self.minx = 10
        self.miny = 10
        self.maxx = 1100
        self.maxy = 500

    def open(self):
        self.ser.close()
        self.ser.open()

    def close(self):
        self.ser.close()

    def reset(self):
        self.ser.write("G30\r\n")

    def home(self):
        self.ser.write("G0 X{0} Y{1}".format(self.minx, self.miny))

    def lr(self):
        self.ser.write("G0 X{0} Y{1}\r\n".format(self.maxx, self.maxy))

    def ll(self):
        self.ser.write("G0 X{0} Y{1}\r\n".format(self.minx, self.maxy))

    def ul(self):
        self.ser.write("G0 X{0} Y{1}\r\n".format(self.minx, self.miny))

    def ur(self):
        self.ser.write("G0 X1100 Y10\r\n")

    def leftvertical(self):
        self.ul()
        self.pulse()
        self.ll()
        self.pulse()
    
    def lowerhorizontal(self):
        self.ll()
        self.pulse()
        self.lr()
        self.pulse()

    def pulse(self):
        self.command="G4 P0.5"

    @property
    def command(self):
        return "enter a gcode command"

    @command.setter
    def command(self,str):
        self.ser.write(str+"\r\n")

class Handleargs(object):
    #http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    def __init__(self, argv):
        self.argv = argv

    def process(self):
        try:
            opts, args = getopt.getopt(self.argv,"hd:",["ifile=","ofile="])
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
                pass
                #sys.exit(1)

if __name__=='__main__':
    arghandler = Handleargs(sys.argv[1:])
    arghandler.process()
    instance = Lsxs()
    instance.reset()
    instance.close()


