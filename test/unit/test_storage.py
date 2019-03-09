import unittest
from volcano.srv104.tag import ClientStorage, Tag


class TestClientStorageCase(unittest.TestCase):

    """ проверка хранилища тегов """

    def __init__(self, testname):
        super(TestClientStorageCase, self).__init__(testname)

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
        """ Создаем хранилище """
        storage = ClientStorage()
        self.assertIsNotNone(storage)
        self.assertNotIsInstance(storage, TypeError)
        self.assertIsInstance(storage, ClientStorage)

    def test_overparms(self):
        """ Проверка на превышение параметров """
        try:
            storage = ClientStorage(1, 2, 3, 4, 5, 6)
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_add(self):
        """ Создаем тег и добавляем """
        tag = Tag(1, 2)
        storage = ClientStorage()
        self.assertTrue(storage.add(tag))

    def test_addgarbage(self):
        """ Добавляем мусор в хранилище """

        storage = ClientStorage()
        self.assertFalse(storage.add("Something"))

    def test_checkadded(self):
        """ Валидируем то что добавили """
        tag = Tag(1, 2)
        storage = ClientStorage()
        storage.add(tag)
        self.assertEqual(tag, storage.get(tag.ioa))


if __name__ == '__main__':
    unittest.main()
