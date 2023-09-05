#
# Copyright (c) 2023 Sylvain Martin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
Simple Qt objects to bridge Qt and ZMQ in the case of a request-reply pattern
(REQ/REP):
https://zeromq.org/socket-api/?language=python&library=pyzmq#request-reply-pattern

be careful, the server/client is not secure in any way


Classes:
    - ZMQError: Communication error with the ZMQ server
    - ZMQTimeout: Communication Timeout with the ZMQ server
    - ZMQClient: A simple object to bridge Qt and ZMQ in the case of a client agent (REP)
    - ZMQServer: A simple object to bridge Qt and ZMQ in the case of a server agent (REP)

Requirements:
    - pyzmq
    - pyqt5
"""
__all__ = ['ZMQError', 'ZMQTimeout', 'ZMQClient', 'ZMQServer']

import zmq
from PyQt5 import QtCore


class ZMQError(IOError):
    """ Communication error with the ZMQ server """
    pass


class ZMQTimeout(ZMQError):
    """ Communication Timeout with the ZMQ server """
    pass


class ZMQClient(QtCore.QObject):
    """ A simple object to bridge Qt and ZMQ in the case of a client agent (REP)

    be careful, the server/client is not secure in any way

    :param endpoint: the protocol, the address and port where the client will connect
    :param parent: the QObject parent
    """

    def __init__(self, endpoint, timeout: int = 1000, parent=None):
        QtCore.QObject.__init__(self, parent=parent)

        context = zmq.Context.instance()
        self.client = context.socket(zmq.REQ)

        self.client.setsockopt(zmq.RCVTIMEO, timeout)
        self.client.setsockopt(zmq.SNDTIMEO, timeout)
        self.client.setsockopt(zmq.LINGER, 1)
        self.client.setsockopt(zmq.IMMEDIATE, 1)

        self.client.setsockopt(zmq.REQ_CORRELATE, 1)
        self.client.setsockopt(zmq.REQ_RELAXED, 1)
        self.client.connect(endpoint)

    def __del__(self):
        self.client.close()

    def ask(self, cmd: str, obj: object = None, timeout: int = 100):
        """
        send a command to the server at ``endpoint`` and wait timeout for an answer

        :param cmd: the command send to the server (as a python string)

        :param obj: The object accompanying the command. can be any python
        object serializable by pickle

        :param timeout: time in milliseconds for the timeout.
        A IOError Exception, is raised if the timeout is reached
        """

        try:
            self.client.send_pyobj([cmd, obj])
        except zmq.Again as e:
            IOError("The server is not reachable")
        except zmq.ZMQError as e:
            IOError("The server error : %s" % e)

        # use poll for timeouts:
        poller = zmq.Poller()
        poller.register(self.client, zmq.POLLIN)
        if poller.poll(timeout):
            msg = self.client.recv_pyobj()
            if isinstance(msg, (list, tuple)):

                if len(msg) > 0:  # there is a cmd
                    cmd = str(msg[0])
                    obj = msg[1] if len(msg) > 1 else None

                    if cmd.strip().lower() == "error":
                        error_msg = "The server sent back an error: %s" % obj
                        ZMQError(error_msg)

                    # return a respond
                    return cmd, obj

                else:  # no topic, it is an error
                    ZMQError("No command string sent back")
            else:  # the object sent back is not a list !
                ZMQError("The answer is not correctly formatted")
        else:
            raise ZMQTimeout("Server request timeout...")


class ZMQServer(QtCore.QObject):
    """ A simple object to bridge Qt and ZMQ in the case of a server agent (REP)

    be careful, the server/client is not secure in any way

    :param address: the protocol, the address and port where the client will connect
    :param parent: the QObject parent
    """

    received = QtCore.pyqtSignal(str, object)
    """ (SIGNAL) emitted when a message is received at the end point """

    def __init__(self, address, parent=None):
        super().__init__(parent=parent)

        self.context = zmq.Context()
        self.server = self.context.socket(zmq.REP)

        self.server.bind(address)

    def __del__(self):
        self.server.close()

    def treat_request(self, cmd: str, obj: object = None) -> tuple[str, object]:
        """
        Treat the request made by the client. This function is made
        to be overloaded by the subclass

        :param cmd: the command send to the server (as a python string)

        :param obj: The object accompanying the command.
        can be any python object serializable by pickle

        :return: the cmd and the object to be sent back to the client
        """
        return cmd, obj

    def loop(self):
        while True:
            msg = self.server.recv_pyobj()

            if isinstance(msg, (list, tuple)):
                if len(msg) > 0:  # there is a cmd
                    cmd = msg[0]
                    obj = msg[1] if len(msg) > 1 else None

                    # send a response
                    self.server.send_pyobj(self.treat_request(cmd, obj))

                else:  # no topic, it is an error
                    print("Server received a bad request ...")
                    self.server.send_pyobj(["error", "No cmd"])

            else:  # the object is not a list, nor a tuple !
                print("Server received a bad request ...")
                self.server.send_pyobj(["error", "The received object is not a tuple or a list"])
