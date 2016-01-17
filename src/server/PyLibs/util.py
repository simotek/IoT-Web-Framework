
# Utils - Simon Lees simon@simotek.net
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

class CallbackHelper:
    def __init__(self):
        self.__funcs = []

    def register(self, funct):
        self.__funcs.append(funct)

    def unregister(self, funct):
        self.__funcs.remove(funct)

    def invoke(self, *args, **kwargs):
        for func in self.__funcs:
          if args and kwargs:
            func(args, kwargs)
          elif args:
            func(args)
          elif kwargs:
            func(kwargs)
          else:
            func()

class ClientCallbacks:
    def __init__(self):
        self.connect = CallbackHelper()
        self.disconnect = CallbackHelper()
        self.message = CallbackHelper()
