#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2018 Andreas Fognini
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#This code is implemented for python 3

import serial
import time
import random

class ElConRoM(object):
    """Implements an interface to communicate with the PCBMotor controller.

    :param string com_port: Serial communcation port path.
    """
    def __init__(self, com_port='/dev/ttyUSB0'):
        self.ENCODER_STEPS_PER_REVENUE = 5760
        self.ser = serial.Serial(port=com_port, baudrate=19200, timeout=1)
        self.motor_nbr = 1
        self._position_in_steps = 0.0

    def send(self, cmd):
        """Send the commands to the controller.
        Sends the commands and receives the controller's reply which is returned.

        :param string cmd: Command for the PCBMotors

        :return:
            Reply from the motor controller.

        :rtype: string
        """
        self.ser.flushInput()
        self.ser.write((cmd+'\r').encode())
        self.ser.flush()
        s = ""
        while True:
            s += self.ser.read().decode("utf-8")
            if ">>" in s:
                break
        return s

    def abs_position_steps(self, s):
        """Move to absolute position in units of steps.

        :param float s: Position in steps. Is rounded to integer while processing.
        """

        self.send("g"+str(int(s)))
        self._position_in_steps =+ s

    def abs_position_degrees(self, s):
        """Move to absolute position in degrees.

        :param float s: Position in degrees.
        """
        steps = int(s/360.0*self.ENCODER_STEPS_PER_REVENUE)
        self.send("g"+str(steps))
        self._position_in_steps =+ steps

    def steps_to_degrees(self, s):
        """Convert steps to degrees.

        :param float s: Number of steps.

        :return:
            Number of degrees.
        :rtype: float
        """
        return s/float(self.ENCODER_STEPS_PER_REVENUE)*360.0

    def degrees_to_steps(self, d):
        """Convert degrees to steps.

        :param float d: Number of degrees.

        :return:
            Number of steps.

        :rtype: float
        """
        return d/360.0*float(self.ENCODER_STEPS_PER_REVENUE)

    def rel_position(self, s):
        """Move relative in units of steps.

        :param float s: Number of steps. Converted to integer in function.
        """

        self.send("s"+str(int(s)))
        self._position_in_steps += s

    def query_position(self):
        """Query position.

        The position is not queried from the controller but from bookkeeping of the sent steps.
        Therefore, not to accurate.

        :return:
            The absolute position in steps.

        :rtyep: float
        """
        pos = self._position_in_steps
        return pos

    def speed(self, scale):
        """Set speed.

        The speed of clock and counter clockwise rotation is adjusted to the same value.

        :param int scale: 0..255
        """

        #Clockwise speed
        self.send("cw"+str(int(scale)))

        #Counter clockwise speed
        self.send("ccw"+str(int(scale)))

    def number(self, m=1):
        """
        Select motor to address.

        One controller can controll several motors. By stating the number a specific motor is selected. Note: Counting starts at 1.

        :param int m: The Motor's number which should be controlled.
        """

        self.motor_nbr = m
        self.send("m"+str(int(m)))

    def home(self):
        """Home motor.
        Homes the motor by finding the home marker. Sets this position to zero.
        """
        self.send('bi,bcr,z')
        self._position_in_steps=0

    def verbocity(self, state):
        """Set verbocity.

        :param bool state: Verbocity active when True.
        """
        if state:
            self.send("q-")
        else:
            self.send("q+")


if __name__ =="__main__":
    #Simple example of moving motor 1 to random postions.
    motor = ElConRoM()
    motor.verbocity(False)
    motor.number(1)

    motor.home()

    for i in range(1000):
        steps=int((random.random())*5000/2.0)
        motor.abs_position_steps(steps)
        motor.abs_position_steps(0)
        time.sleep(1)
