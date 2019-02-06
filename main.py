import signal
import argparse
from twisted.internet import reactor
from server.app import AppConfig, App


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    reactor.stop()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description='VC to IEC61850 adapter')

    parser.add_argument('--config',
                        dest='config',
                        default='config.xml',
                        help='configuration file',
                        )
    args = parser.parse_args()

    cfg = AppConfig(reactor, args.config)
    app = App(cfg)
    app.start()
    reactor.addSystemEventTrigger('before', 'shutdown', app.stop)
    reactor.run()


if __name__ == '__main__':
    main()
