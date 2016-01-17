###############################################################################
#
# Copyright (c) 2016, Simon Lees simon@simotek.net
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#* Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
#* Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################

from PyLibs.websocketserver import ThreadedWebSocketServer, ServerCallbacks

import time

class Printer:
    def __init__(self):
        print ("create")

    def cn():
        print ("Connected CB")

    def dn ():
        print ("Disconnected CB")

    def m(Message):
        print ("Msg Recieved: "+ str(Message))


if __name__ == '__main__':

    pnt = Printer

    callbacks = ServerCallbacks()

    callbacks.connect.register(pnt.cn)
    callbacks.disconnect.register(pnt.dn)
    callbacks.message.register(pnt.m)

    server = ThreadedWebSocketServer("ws://127.0.0.1:8702", callbacks)

    server.start()

    time.sleep(4)

    while True:
        server.broadcastMessage("Broadcast")

        time.sleep(1)
