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

class Lsxs(object):

    def __init__(self):
        self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=57600)
	self.open()

    def open(self):
        self.ser.close()
        self.ser.open()

    def close(self):
        self.ser.close()

    def home(self):
        self.ser.write("G0 X10 Y10")
    
    def reset(self):
        self.ser.write("G30\r\n")

    def lr(self):
        self.ser.write("G0 X1100 Y500\r\n")

    def ll(self):
        self.ser.write("G0 X10 Y500\r\n")

    def ul(self):
        self.ser.write("G0 X10 Y10\r\n")

    def ur(self):
        self.ser.write("G0 X1100 Y10\r\n")

    def leftvertical(self):
        self.command("G0 X10 Y10")
        self.command("G4 P0.5")
        self.command("G0 F2000 X10 Y500")
        self.command("G4 P0.5")
    
    def lowerhorizontal(self):
        self.command("G0 X10 Y500")
        self.command("G4 P0.5")
        self.command("G0 X1100 Y500")
        self.command("G4 P0.5")

    def command(self,str):
        self.ser.write(str+"\r\n")

if __name__=='__main__':
    instance = Lsxs()
    instance.reset()
    instance.close()


