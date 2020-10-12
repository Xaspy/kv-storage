import time
import unittest
from kvs import ArgParseHandler, serv_info_path
from kvs_http import start_server
from multiprocessing import Process


class TestHttpClient(unittest.TestCase):
    p = Process()

    @classmethod
    def setUpClass(cls):
        for i in range(10):
            cls.port = 5000 + i
            cls.p = Process(target=start_server, args=(cls.port,))
            cls.p.start()
            time.sleep(1)
            if cls.p.is_alive():
                break
            ArgParseHandler.save_connect_info('address',
                                              '127.0.0.1',
                                              serv_info_path)
            ArgParseHandler.save_connect_info('port',
                                              cls.port,
                                              serv_info_path)

    def test_create_db(self):
        resp1 = ArgParseHandler.post_request_db(serv_info_path, 'db_01')
        resp2 = ArgParseHandler.get_request_db(serv_info_path, 'list')
        resp3 = ArgParseHandler.get_request_db(serv_info_path, 'delete/db_01')
        self.assertEqual(resp1, 'Database "db_01" successfully created')
        self.assertEqual(resp3, '"db_01" was successfully deleted')
        self.assertEqual(resp2, '[\'db_01\']')

    def test_delete_db(self):
        resp1 = ArgParseHandler.post_request_db(serv_info_path, 'db_01')
        resp2 = ArgParseHandler.get_request_db(serv_info_path, 'delete/db_01')
        resp3 = ArgParseHandler.get_request_db(serv_info_path, 'list')
        self.assertEqual(resp1, 'Database "db_01" successfully created')
        self.assertEqual(resp2, '"db_01" was successfully deleted')
        self.assertEqual(resp3, '[]')

    def test_get_list_db(self):
        resp1 = ArgParseHandler.post_request_db(serv_info_path, 'db_01')
        ArgParseHandler.post_request_db(serv_info_path, 'db_02')
        ArgParseHandler.post_request_db(serv_info_path, 'db_03')
        resp4 = ArgParseHandler.get_request_db(serv_info_path, 'list')
        resp5 = ArgParseHandler.get_request_db(serv_info_path, 'delete/db_01')
        ArgParseHandler.get_request_db(serv_info_path, 'delete/db_02')
        ArgParseHandler.get_request_db(serv_info_path, 'delete/db_03')
        self.assertEqual(resp1, 'Database "db_01" successfully created')
        self.assertEqual(resp5, '"db_01" was successfully deleted')
        self.assertEqual(resp4, '[\'db_01\', \'db_02\', \'db_03\']')

    def test_set_get_del_elem_db(self):
        resp1 = ArgParseHandler.post_request_db(serv_info_path, 'db_01')
        resp2 = ArgParseHandler.save_connect_info('db_01',
                                                  'selected_db',
                                                  serv_info_path)
        resp3 = ArgParseHandler.post_request_db(serv_info_path,
                                                'db_01/e_01',
                                                '123')
        resp4 = ArgParseHandler.get_request_db(serv_info_path, 'db_01/e_01')
        resp5 = ArgParseHandler.get_request_db(serv_info_path,
                                               'db_01/delete/e_01')
        resp6 = ArgParseHandler.get_request_db(serv_info_path, 'delete/db_01')
        self.assertEqual(resp1, 'Database "db_01" successfully created')
        self.assertEqual(resp2, 'Successfully selected "db_01"')
        self.assertEqual(resp3, 'Successfully set key "e_01" in db "db_01"')
        self.assertEqual(resp4, '123')
        self.assertEqual(resp5, 'Element with key "e_01" in "db_01" '
                                'db was successfully deleted')
        self.assertEqual(resp6, '"db_01" was successfully deleted')

    def test_list_elem_db(self):
        resp1 = ArgParseHandler.post_request_db(serv_info_path, 'db_01')
        resp2 = ArgParseHandler.save_connect_info('db_01',
                                                  'selected_db',
                                                  serv_info_path)
        resp3 = ArgParseHandler.post_request_db(serv_info_path,
                                                'db_01/e_01',
                                                '123')
        resp4 = ArgParseHandler.post_request_db(serv_info_path,
                                                'db_01/e_02',
                                                '456')
        resp5 = ArgParseHandler.post_request_db(serv_info_path,
                                                'db_01/e_03',
                                                '789')
        resp6 = ArgParseHandler.get_request_db(serv_info_path, 'db_01/list')
        resp7 = ArgParseHandler.get_request_db(serv_info_path, 'delete/db_01')
        self.assertEqual(resp1, 'Database "db_01" successfully created')
        self.assertEqual(resp2, 'Successfully selected "db_01"')
        self.assertEqual(resp3, 'Successfully set key "e_01" in db "db_01"')
        self.assertEqual(resp4, 'Successfully set key "e_02" in db "db_01"')
        self.assertEqual(resp5, 'Successfully set key "e_03" in db "db_01"')
        self.assertEqual(resp6, '[\'e_01\', \'e_02\', \'e_03\']')
        self.assertEqual(resp7, '"db_01" was successfully deleted')

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()


if __name__ == '__main__':
    unittest.main()
