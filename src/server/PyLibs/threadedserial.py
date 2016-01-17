
# Threaded Serial - Simon Lees simon@simotek.net
# Copyright (C) 2015 Simon Lees
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import threading
import time
import serial


class  ThreadedSerial(threading.Thread):

  def __init__(self, port=None, baud=None):
    # First set up thread related  code
    threading.Thread.__init__(self)
    self.__dataLock = threading.RLock()
    self.__stopRunning = False
    self.__finished =  True

    # now set up serial related code
    self.__serialPort = port
    self.__serialBaud = baud
    self.__serialRecieveFunc = None
    self.__serialConnection = None

  def __del__(self):
    if self.__stopRunning:
      return
    self.__dataLock.acquire()
    self.__stopRunning = True
    self.__dataLock.release()

    waiting = True

    while waiting:
      if self.__dataLock.acquire(False):
        if self.__finished == True:
          waiting = False

        self.__dataLock.release()
      else:
        # if can't get a lock wait for it
        time.sleep(0.2)

  # This method takes a function as a paramater,
  # that function should take 1 paramater which will be passed a line of serial data
  def setSerialRecieveFunction(self, RecvFunc):
    self.__dataLock.acquire()
    self.__serialRecieveFunc = RecvFunc
    self.__dataLock.release()

  def setSerialConfig(self, port, baud):
    self.__serialPort = port
    self.__serialBaud = baud

  def create(self):
    # Create Serial connection - use a long timeout of 999 as its running in a thread and could
    # really wait forever for readline
    # TBD: handle exception
    self.__dataLock.acquire()
    self.__serialConnection = serial.Serial(self.__serialPort, self.__serialBaud, timeout=None)
    self.__dataLock.release()

  # writes data to the serial port, automatically re encodes data to
  def write(self, data):
    self.__serialConnection.write(data.encode('ascii'))
    self.__serialConnection.flush()

  # overloads the theads run class to provide non blocking Seral responses
  # @note create should be called before start
  def run(self):

    while True:
      # take out lock for access to stop running
      # Use a non blocking lock, there is no harm in looping more times here while waiting for
      # something else to unlock
      if self.__dataLock.acquire():
        # if its time to stop running stop
        if self.__stopRunning == True:
          ## do cleanup here

          self.__dataLock.release()
          return

        self.__dataLock.release()

      # this code blocks until it recieves a new line char
      read = self.__serialConnection.readline()

      decoded = str(read.decode('utf-8', errors='ignore').rstrip().replace('\n', '').replace('\r', ''))

      print ("serialIn:decoded")
      # check whatever you need to check here
      if self.__serialRecieveFunc is not None:
        # Call the function passing it the line as a parami
        self.__serialRecieveFunc(decoded)
      time.sleep(0.01)

  def stop(self):
    self.__dataLock.acquire()
    self.__stopRunning = True
    self.__dataLock.release()
