from lxml import objectify

from server.informationobject import IO, IOPool
from server.lib104 import IEC608705TypeID, Server104Config


class XmlError:
    """ Класс для хранения информации об ошибке """

    def __init__(self, message=None):
        self.message = message

    def ok(self):
        """ Нет ошибки"""
        return self.message is None


class ServerConfigFromXml():
    def __init__(self, file):
        self._root = objectify.parse(file).getroot()
        assert isinstance(self._root, objectify.ObjectifiedElement)
        session = self._root.Session
        connection = self._root.Session.Connection
        self.data = Server104Config()
        try:
            self.data.ip_address = str(connection.get("IpAddr"))
            self.data.port = int(connection.get("TcpPort"))
            self.data.t0 = int(session.get("T0"))
            self.data.t1 = int(session.get("T1"))
            self.data.t2 = int(session.get("T2"))
            self.data.t3 = int(session.get("T3"))
            self.data.k = int(session.get("K"))
            self.data.w = int(session.get("W"))
            self.data.cot_size = int(session.get("TransmCauseSize"))
        except:
            pass


class IOPoolFromXml():
    def __init__(self, file):
        self._root = objectify.parse(file).getroot()
        assert isinstance(self._root, objectify.ObjectifiedElement)

        self.pool = IOPool()

        try:
            self.pool = self._parse_elements(
                self._root.Session.Connection.Slave)

        except:
            pass

    def _parse_elements(self, slave_node):
        io_pool = IOPool()
        for io in slave_node.iterchildren():
            new_io = IOPoolFromXml._parse_io(io)
            if new_io.validate():
                io_pool.add(new_io)
            else:
                self.error = XmlError(
                    'Invalid tag #{}'.format(io_pool.count + 1))
                return IOPool()

        return io_pool

    @staticmethod
    def _parse_io(line):
        ioa = line.get("ObjectAddr")
        type = IEC608705TypeID.from_node(line)
        name = line.get("Name")
        group = line.get("Groupe")
        return IO(int(ioa), int(type), str(name), int(group))
