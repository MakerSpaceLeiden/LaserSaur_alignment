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

class Const(object):
	MINX = 10
	MINY = 10
	MAXX = 1100
	MAXY = 500

class Lsxs(object):

    def __init__(self):
        self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=57600)
	self.open()
	self.speed = 2000

    def open(self):
        self.ser.close()
        self.ser.open()

    def close(self):
        self.ser.close()


    @property
    def speed(self):
   	return self.speed

    @speed.setter
    def speed(self, spd):
    	self.speed = spd
    	self.command = "F{0}".format(self.speed)
    	
    def reset(self):
        self.command = "G30"

    def home(self):
    	self.movetoxy(Const.MINX, Const.MINY)

    def movetoxy(self, x, y):
    	if ((x<Const.MINX) OR (x>Const.MAXX)) return -1
    	if ((y<Const.MINY) OR (1>Const.MAXY)) return -1
    	self.command = "G0 X{0} Y{1}".format(x, y)

    def lr(self):
    	self.movetoxy(Const.MAXX, Const.MAXY)

    def ll(self):
        self.movetoxy(Const.MINX, Const.MAXX)

    def ul(self):
        self.movetoxy(Const.MINX, Const.MINY)
        
    def ur(self):
        self.movetoxy(Const.MINX, Const.MAXX)

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

if __name__=='__main__':
    instance = Lsxs()
    instance.reset()
    instance.close()
