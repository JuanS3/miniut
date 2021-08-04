from miniut.abstract.database import DBAbs
import unittest


class Database(DBAbs):

    __conn = None

    def without_session(self) -> str:
        if self.__conn is None:
            return 'Connection is not available'
        
        return 'miniut'

    @DBAbs.session
    def with_session(self,):
        if self.__conn is None:
            return 'Connection is not available'
        
        return 'miniut'

    def open_cxnx(self):
        self.__conn = 'Open'
    
    def close_cxnx(self):
        self.__conn = None


class TestDatabase(unittest.TestCase):

    def test_without_session(self):
        self.assertEqual(Database().without_session(),'Connection is not available')
    
    def test_with_session(self):
        self.assertEqual(Database().with_session(),'miniut')

    def test_with_and_without_session(self):
        self.assertEqual(Database().without_session(),'Connection is not available')
        self.assertEqual(Database().with_session(),'miniut')
        self.assertEqual(Database().without_session(),'Connection is not available')
