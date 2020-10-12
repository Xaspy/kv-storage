import unittest
from kvs_http import app
import kvs_http
import time
from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname


class TestHttpServer(unittest.TestCase):
    port = 0
    p = Process()

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()

    def test_get_empty_list_of_dbd(self):
        resp = self.client.get('/api/list')
        self.assertEqual(resp.data.decode('utf-8'), '[]')

    def test_create_database(self):
        self.client.post('/api/db_01')
        resp = self.client.get('/api/list')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp.data.decode('utf-8'), '[\'db_01\']')

    def test_set_item_in_db(self):
        self.client.post('/api/db_01')
        self.client.post('/api/db_01/i_01', data='info')
        resp = self.client.get('/api/db_01/i_01')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp.data.decode('utf-8'), 'info')

    def test_delete_item_in_db(self):
        self.client.post('/api/db_01')
        self.client.post('/api/db_01/i_01', data='info')
        self.client.get('/api/db_01/delete/i_01')
        resp = self.client.get('/api/db_01/list')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp.data.decode('utf-8'), '[]')

    def test_delete_database(self):
        self.client.post('/api/db_01')
        self.client.get('/api/delete/db_01')
        resp = self.client.get('/api/list')
        self.assertEqual(resp.data.decode('utf-8'), '[]')

    def test_partition_get(self):
        self.client.post('/api/db_01')
        self.client.post('/api/db_01/i_01', data='abcdefghijklmnopqrstyvwxyz')
        resp_1 = self.client.get('/api/db_01/i_01')
        resp_2 = self.client.get('/api/db_01/i_01/0')
        resp_3 = self.client.get('/api/db_01/i_01/1')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp_1.data.decode('utf-8'),
                         resp_2.data.decode('utf-8'))
        self.assertNotEqual(resp_1.data.decode('utf-8'),
                            resp_3.data.decode('utf-8'))

    def test_partition_set(self):
        self.client.post('/api/db_01')
        self.client.post('/api/db_01/i_01', data='abc')
        self.client.post('/api/db_01/i_01', data='def')
        resp = self.client.get('/api/db_01/i_01')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp.data.decode('utf-8'), 'abcdef')

    def test_partition_set_and_get(self):
        self.client.post('/api/db_01')
        self.client.post('/api/db_01/i_01', data='abcdef')
        self.client.post('/api/db_01/i_01', data='ghijkl')
        resp_1 = self.client.get('/api/db_01/i_01')
        resp_2 = self.client.get('/api/db_01/i_01/1')
        self.client.get('/api/delete/db_01')
        self.assertEqual(resp_1.data.decode('utf-8'), 'abcdefghij')
        self.assertEqual(resp_2.data.decode('utf-8'), 'kl')

    def test_start_server(self):
        for i in range(10):
            self.port = 5000 + i
            self.p = Process(target=kvs_http.start_server, args=(self.port,))
            self.p.start()
            time.sleep(1)
            if self.p.is_alive():
                break
        target = "localhost"
        target_ip = gethostbyname(target)
        s = socket(AF_INET, SOCK_STREAM)
        result = s.connect_ex((target_ip, self.port))
        s.close()
        self.assertTrue(result == 0)
        self.p.terminate()


if __name__ == '__main__':
    unittest.main()
