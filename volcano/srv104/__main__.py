import logging
import argparse
import signal
from twisted.internet import reactor

from pv.connector.twisted import TwistedTransport
from pv.connector.transport import Transport
from pv.client.twisted import TwistedTimerFactory
from pv.client.timer import Timers
from pv.client.base import Client, ClientEvents, ClientConfig

from volcano.srv104.server import Server104
from volcano.srv104.libiec import QualityDescriptor
from volcano.srv104.xml import ServerConfigFromXml, IOPoolFromXml, ClientConfigFromXml
from volcano.srv104.tag import IO


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    reactor.stop()


class AppConfig:
    """ Config object for App """

    def __init__(self, out_reactor, file='config.xml'):
        self.file = file
        self.logger = None
        self.reactor = out_reactor


class App:
    """ Main App """

    def __init__(self, config):
        self.logger = config.logger
        self._client = None
        self._server = None
        self._tags = None
        self._config = config
        self._reactor = config.reactor
        # self._storage = IOStorageFromXml(self._config.file).data
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
        cfg = ClientConfigFromXml(self._config.file).data
        cfg.transport = Transport(
            TwistedTransport,
            self._reactor,
            cfg.host,
            cfg.port,
            cfg.reconnect_timeout)
        cfg.timers = Timers(TwistedTimerFactory, self._reactor)
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
        except Exception as general_exception:
            self.logger.debug("Trouble with update storage {0}".format(general_exception))

    def _init_stage1(self, res):
        if not res.success:
            self.error('Subscribe error: unconfirmed tags \n{0}'.format(res.result['rejected']))
        else:
            self._client.subscribe(self._tags)

    def _init_stage2(self, task):
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
        if message:
            self.logger.debug("ERROR: {}".format(message))
        self.stop()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description='VC to IEC61850 adapter')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser.add_argument('--core_host', help='Volcano core host',
                        default='volcano')
    parser.add_argument('--config', dest='config', default='config.xml',
                        help='configuration file', )
    args = parser.parse_args()
    cfg = AppConfig(reactor, args.config)
    cfg.logger = logger
    logger.debug("volcano_core host port: {0}".format(args.core_host))
    app = App(cfg)
    app.start()
    reactor.addSystemEventTrigger('before', 'shutdown', app.stop)
    reactor.run()


if __name__ == '__main__':
    main()
