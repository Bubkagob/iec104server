import logging
from ctypes import CFUNCTYPE, POINTER, CDLL
from ctypes import c_bool, c_void_p, c_int, c_char_p

lib104 = CDLL('/usr/local/lib/liblib60870.so')


# connection_request_handler proto
connection_request_handler_proto = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    POINTER(c_void_p),
    c_int
)
# CS104_Connection_destroy
lib104.CS104_Connection_destroy.argtypes = [c_void_p]
lib104.CS104_Connection_destroy.restype = c_void_p

# CS104_Connection_connect
lib104.CS104_Connection_connect.argtypes = [c_void_p]
lib104.CS104_Connection_connect.restype = c_bool

# Thread_sleep
lib104.Thread_sleep.argtypes = [c_int]
lib104.Thread_sleep.restype = c_void_p

# CS104_Connection_create
lib104.CS104_Connection_create.argtypes = [c_char_p, c_int]
lib104.CS104_Connection_create.restype = c_void_p

# CS104_Connection_setConnectionHandler
lib104.CS104_Connection_setConnectionHandler.argtypes = [c_void_p, c_void_p, c_int]
lib104.CS104_Connection_setConnectionHandler.restype = c_void_p


class Client104():

    def __init__(self):
        self.ip: bytes = "127.0.0.1".encode()
        self.port: int = 2404
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.connection = lib104.CS104_Connection_create(self.ip, self.port)

        # set interrogation handler
        self.con_handler = connection_request_handler_proto(self.connection_req_handler)
        lib104.CS104_Connection_setConnectionHandler(self.connection, self.con_handler, c_int())
        lib104.CS104_Connection_connect(self.connection)
        self.logger.debug("Client Connected")

    def stop(self):
        self.logger.debug("Stopping client")
        lib104.CS104_Connection_destroy(self.connection)

    def connection_req_handler(self, parameter, connection, event):
        if int(event) == 0:
            self.logger.debug("Connection established {0}".format(event))
        elif int(event) == 1:
            self.logger.debug("Connection closed {0}".format(event))
            self.stop()
        elif int(event) == 2:
            print(str(event), "Connection startDT CON RECEIVED")
        elif int(event) == 3:
            print(str(event), "Connection stopDT CON RECEIVED")
        return True
