from server.io import IO, IOStorage
from server.xml import IOStorageFromXml, ServerConfigFromXml

from server.lib104 import Server104, QualityDescriptor

from pv.client.base import Client, ClientEvents, ClientConfig
from pv.client.timer import Timers
from pv.client.twisted import TwistedTimerFactory
from pv.connector.transport import Transport
from pv.connector.twisted import TwistedTransport


class AppConfig:
    def __init__(self, reactor, file='config.xml'):
        self.file = file
        self.log = None
        self.reactor = reactor


class App:
    def __init__(self, config):
        self._client = None
        self._server = None
        self._tags = None
        self._config = config
        self._reactor = config.reactor
        self._storage = IOStorageFromXml(self._config.file).data

    def start(self):
        print("Hello!")
        # reader = XmlReader(self._config.file)
        # if not reader.validate():
        #     self.error('Invalid config file. {0}'.format(reader.error.message))
        self._tags = [k for (k, _) in self._storage.items()]
        self._start_server()
        self._start_client()

    def _start_server(self):
        srv_cfg = ServerConfigFromXml(self._config.file).data
        self._server = Server104(srv_cfg)
        self._server.tags = self._storage
        self._server.start()

    def _start_client(self):
        cfg = ClientConfig()
        cfg.host = "127.0.0.1"
        cfg.port = 8091
        cfg.events = ClientEvents()
        cfg.transport = Transport(
            TwistedTransport,
            self._reactor,
            cfg.host,
            cfg.port,
            cfg.reconnect_timeout)

        cfg.timers = Timers(TwistedTimerFactory, self._reactor)
        cfg.name = "PeavyTextClient"

        cfg.events.handshake = self._handshake
        cfg.events.find = lambda task: self._init_stage1(
            task)
        cfg.events.subscribe = lambda task: self._init_stage2(
            task)
        cfg.events.update = self._update
        self._client = Client(cfg)
        self._server.vclient = self._client
        self._client.start()

    def _handshake(self):
        """ Коннект установлен и ответ на приветсвие был получен """
        self._client.find(self._tags)

    def _update(self, res):
        print("Update")
        name = res.result['tag']
        value = res.result['v']
        time = res.result['t']
        qual = res.result['q']

        try:
            io = self._storage.get(name)
            io.value = (0 if value is None else value)
            io.quality = qual
            io.timestamp = time
            self._storage.update(io)
        except Exception as e:
            print("Trouble with update storage", e)

        try:
            io = self._storage.get(name)
            self._server.send(io)
        except Exception as e:
            print("Trouble with write to clients", e)

    def _init_stage1(self, res):
        """ Поиск тэгов завершен """
        if not res.success:
            self.error('Subscribe error: unconfirmed tags \n{0}'.format(res.result['rejected']))
        else:
            self._client.subscribe(self._tags)

    def _init_stage2(self, task):
        """ Подписка на тэги завершена """
        if not task.success:
            self.error('Subscribe error. Please check tag existence')
        else:
            print('Subscribe done')

    def stop(self):
        """ Останов """
        try:
            self._server.stop()
        except:
            pass
        try:
            self._reactor.stop()
        except:
            pass

    def error(self, message):
        """ Отработка ошибки"""
        if message:
            print('ERROR: {}'.format(message))
        self.stop()
