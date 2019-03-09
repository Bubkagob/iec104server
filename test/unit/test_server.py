import unittest
from volcano.srv104.server import Server104


class TestServerCase(unittest.TestCase):

    """ Тесты самого сервера """

    def __init__(self, testname):
        super(TestServerCase, self).__init__(testname)

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creating(self):
        """ Создаем сервер без конфигурации """
        try:
            storage = Server104()
        except Exception as e:
            self.assertRaises(TypeError, e)


if __name__ == '__main__':
    unittest.main()
