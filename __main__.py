import signal
import argparse
import logging
from twisted.internet import reactor
from server.app import AppConfig, App

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    reactor.stop()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description='VC to IEC61850 adapter')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser.add_argument('--config',
                        dest='config',
                        default='config.xml',
                        help='configuration file',
                        )
    args = parser.parse_args()

    cfg = AppConfig(reactor, args.config)
    cfg.logger = logger
    app = App(cfg)
    app.start()
    reactor.addSystemEventTrigger('before', 'shutdown', app.stop)
    reactor.run()


if __name__ == '__main__':
    main()
