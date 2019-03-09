#! /usr/bin/python3
""" Module docstring """
import unittest
import logging
import time
from ddt import ddt, data
from volcano.srv104.client import Client104

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] (%(threadName)-10s) %(message)s",
)


@ddt
class ConnectionCase(unittest.TestCase):
    """ simple connection case """

    def __init__(self, testname):
        self.testname = testname
        super(ConnectionCase, self).__init__(testname)

    def setUp(self):
        logging.debug("set up {0}".format(self.testname))
        self.client = Client104("srv104")
        self.client.start()

    def tearDown(self):
        logging.debug("tear down {0}".format(self.testname))
        self.client.stop()

    @data(1, 4, 3, 5, 6, 7, 5, 34, 2)
    def test_connection(self, value):
        """ simple conn test """
        self.assertEqual(self.client.connected, True)

    @unittest.skip("skip test_destroy_opened_connection")
    def test_close_only(self):
        """ Соединяемся, потом закрываем коннект, но не уничтожает соединение
        Тест считается пройденным, если будет изменяться статус соединения """
        self.assertTrue(self.client.connected)
        self.client.close()
        time.sleep(0.4)
        self.assertFalse(self.client.connected)

    @unittest.skip("skip test_destroy_opened_connection")
    def test_destroy_opened_connection(self):
        """ Соединяемся и удаляем объект соединения
            Должно быть без сюрпризов """
        self.assertTrue(self.client.connected)
        self.client.con_destroy()
        self.assertTrue(self.client.connected)
