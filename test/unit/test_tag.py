import unittest
from volcano.srv104.tag import Tag


class TestTagCase(unittest.TestCase):

    """ проверка модуля тегов """

    def __init__(self, testname):
        super(TestTagCase, self).__init__(testname)

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

    def test_noparams(self):
        """ Создаем тег без параметров. не должно создаться. """
        try:
            tag = Tag()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_okparams(self):
        """ Создаем тег с параметрами. Должен создаться """
        self.assertNotIsInstance(Tag(1, 2), TypeError)
        self.assertIsInstance(Tag(1, 2), Tag)

    def test_validation(self):
        """ Валидируем на отсутствие/присутствие none """
        self.assertTrue(Tag(1, 2).validate())
        self.assertFalse(Tag(None, None).validate())

    def test_istagobject(self):
        """ создаем тег с параметрами, проверяем что они не None """
        tag = Tag(1, 2)
        self.assertIsNotNone(tag)
        self.assertTrue(tag.validate())
        self.assertIsInstance(tag, Tag)

    def test_overparams(self):
        """ Проверка на превышение параметров """
        try:
            tag = Tag(1, 2, 3, 4, 5, 6)
        except Exception as e:
            self.assertRaises(TypeError, e)


if __name__ == '__main__':
    unittest.main()
