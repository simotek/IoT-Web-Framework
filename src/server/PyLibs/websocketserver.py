# Based off a test app with the following license
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import asyncio

import threading
from urllib.parse import urlparse
from .util import CallbackHelper

class ServerCallbacks:
    def __init__(self):
        self.connect = CallbackHelper()
        self.disconnect = CallbackHelper()
        self.message = CallbackHelper()

class ThreadedServerProtocol(WebSocketServerProtocol):

  def onConnect(self, request):
    print("Client connecting: {0}".format(request.peer))

  def onOpen(self):
    print("WebSocket connection open.")
    self.factory.register(self)

  def onMessage(self, payload, isBinary):
    if isBinary:
      print("Binary message received: {0} bytes".format(len(payload)))
    else:
      print("Text message received: {0}".format(payload.decode('utf8')))
      self.factory.onMessage(payload.decode('utf8'))

    # echo back message verbatim
    # self.sendMessage(payload, isBinary)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def onClose(self, wasClean, code, reason):
    print("WebSocket connection closed: {0}".format(reason))

class ThreadedServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, callbacks, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.__callbacks = callbacks
        self.__clients = []

    def register(self, client):
        if client not in self.__clients:
            print("registered client {}".format(client.peer))
            self.__clients.append(client)
            self.__callbacks.connect.invoke()

    def unregister(self, client):
        if client in self.__clients:
            print("unregistered client {}".format(client.peer))
            self.__clients.remove(client)
            self.__callbacks.disconnect()

    def onMessage(self, message):
        self.__callbacks.message.invoke(message)

    def broadcastMessage(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.__clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))

class  ThreadedWebSocketServer(threading.Thread):

  def __init__(self, url, callbacks):
    # First set up thread related  code
    threading.Thread.__init__(self)
    self.__url = url
    self.callbacks = callbacks

    self.__loop = asyncio.get_event_loop()

    self.__factory = ThreadedServerFactory(self.__url, self.callbacks, debug=False)
    self.__factory.protocol = ThreadedServerProtocol

  def broadcastMessage(self, msg):
    self.__factory.broadcastMessage(msg)

  def run(self):
    asyncio.set_event_loop(self.__loop)

    parsed = urlparse(self.__url)

    ipaddr = parsed.netloc.replace("ws://","").split(':', 1)[0]
    print ("Serving on: "+ipaddr+"-"+str(parsed.port))

    coro = self.__loop.create_server(self.__factory, "0.0.0.0", parsed.port)
    server = self.__loop.run_until_complete(coro)

    try:
        self.__loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        self.__loop.close()
