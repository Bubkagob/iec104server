from server.informationobject import IO
from server.xml import ServerConfigFromXml, IOPoolFromXml

from server.lib104 import QualityDescriptor
from server.slave import Server104

from pv.client.base import Client, ClientEvents, ClientConfig
from pv.client.timer import Timers
from pv.client.twisted import TwistedTimerFactory
from pv.connector.transport import Transport
from pv.connector.twisted import TwistedTransport


class AppConfig:
    def __init__(self, reactor, file='config.xml'):
        self.file = file
        self.logger = None
        self.reactor = reactor


class App:
    def __init__(self, config):
        self.logger = config.logger
        self._client = None
        self._server = None
        self._tags = None
        self._config = config
        self._reactor = config.reactor
        #self._storage = IOStorageFromXml(self._config.file).data
        self._pool = IOPoolFromXml(self._config.file).pool

    def start(self):
        self.logger.debug("start app")
        # reader = XmlReader(self._config.file)
        # if not reader.validate():
        #     self.error('Invalid config file. {0}'.format(reader.error.message))
        self._tags = self._pool.subscribe_list()
        # self._tags = [k for (k, _) in self._storage.items()]
        self._start_server()
        self._start_client()

    def _start_client(self):
        cfg = ClientConfig()
        cfg.host: str = "127.0.0.1"
        cfg.port: int = 8091
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

    def _start_server(self):
        srv_cfg = ServerConfigFromXml(self._config.file).data
        self._server = Server104(srv_cfg)
        self._server.pool = self._pool
        self._server.start()

    def _handshake(self):
        """ Коннект установлен и ответ на приветсвие был получен """
        self._client.find(self._tags)

    def _update(self, res):
        name = res.result['tag']
        value = res.result['v']
        time = res.result['t']
        qual = res.result['q']
        self.logger.debug(
            "update tag {0}, value {1}, time {2}, quality {3}".format(
                name, value, time, qual))

        try:
            io = self._pool.get_io_by_name(name)
            io.value = (0 if value is None else value)
            io.quality = qual
            io.timestamp = time
            self._pool.update(io)
            self._server.send(io)
        except Exception as e:
            self.logger.debug("Trouble with update storage {0}".format(e))

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
            self.logger.debug("Subscribe done")

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
            self.logger.debug("ERROR: {}".format(message))
        self.stop()
