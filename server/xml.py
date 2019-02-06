from lxml import objectify

from server.io import IOStorage, IO
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


class IOStorageFromXml():

    def __init__(self, file):
        self._root = objectify.parse(file).getroot()
        assert isinstance(self._root, objectify.ObjectifiedElement)

        self.data = IOStorage()
        try:
            tags_list = self._root.Session.Connection.Slave
            self.data = self._get_tags(tags_list)

        except:
            pass

    def _get_tags(self, list):
        if list.tag is None:
            return None

        tags = IOStorage()
        for io in list.iterchildren():
            new_io = IOStorageFromXml._parse_element(io)
            if new_io.validate():
                tags.insert(new_io)
            else:
                self.error = XmlError(
                    'Invalid tag #{}'.format(tags.count + 1))
                return IOStorage()

        return tags

    @staticmethod
    def _parse_element(el):
        format = el.get("Format")
        type = IEC608705TypeID.from_string(el.tag, format)
        name = el.get("Name")
        group = el.get("Groupe")
        ioa = el.get("ObjectAddr")

        return IO(type, format, name, group, ioa)
