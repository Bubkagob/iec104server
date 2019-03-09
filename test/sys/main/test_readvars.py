#! /usr/bin/python3
""" Module docstring """
import unittest
import threading
import time
import logging
from ddt import ddt, data, file_data, unpack
from volcano.srv104.client import Client104
from volcano.test.volcano_client import VolcanoClient


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] (%(threadName)-10s) %(message)s",
)


@ddt
class MainCase(unittest.TestCase):
    """ Запись чтение MSP """

    def __init__(self, testname):
        super(MainCase, self).__init__(testname)

    @classmethod
    def setUpClass(self):
        self.client = Client104("srv104")
        self.client.start()
        # self.vc = VolcanoClient("127.0.0.1", 8091)
        self.vc = VolcanoClient()
        self.vc.salute()
        self.client.send_gi()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(self):
        self.vc.safe_close()
        self.client.stop()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unpack
    @file_data('msp1_data.json')
    def test_msp1(self, name, ioa, value):
        """ m_sp_nc_1 test """
        self.vc.set_tag(name, value)
        time.sleep(0.2)
        obj_value = self.client.storage.get(ioa).value
        self.assertEqual(bool(value), obj_value)

    @unpack
    @file_data('mme13_data.json')
    def test_mme13(self, name, ioa, value):
        """ m_me_nc_1 test """
        self.vc.set_tag(name, value)
        time.sleep(0.2)
        obj_value = self.client.storage.get(ioa).value
        self.assertAlmostEqual(float(value), obj_value, places=4)
