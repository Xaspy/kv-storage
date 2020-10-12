import unittest
from kvs_mech import KeyValueStorage
import kvs_mech


class TestKeyValueStorage(unittest.TestCase):
    def setUp(self):
        self.db = KeyValueStorage('test', 3)

    def test_set_get_value(self):
        self.db.set('first', 'info')
        result = self.db.get('first')
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, 'info')

    def test_delete_item(self):
        self.db.set('first', 'info')
        self.db.delete('first')
        result = self.db.list()
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, [])

    def test_get_key_list(self):
        self.db.set('first', 'info')
        self.db.set('second', 'notes')
        self.db.set('third', 'recipe')
        result = self.db.list()
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, ['first', 'second', 'third'])

    def test_unload_item_from_mem(self):
        self.db.set('first', 'info')
        self.db.set('second', 'notes')
        self.db.set('third', 'recipe')
        self.db.set('fourth', 'files')
        result = list(self.db.data.keys())
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, ['second', 'third', 'fourth'])

    def test_load_regular_items_to_mem(self):
        self.db.set('first', 'info')
        self.db.set('second', 'notes')
        self.db.set('third', 'recipe')
        self.db.set('fourth', 'files')
        self.db.set('fifth', 'philosophy')
        self.db.get('first')
        self.db.get('second')
        result = list(self.db.data.keys())
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, ['fifth', 'first', 'second'])

    def test_get_three_part_file(self):
        self.db.set('first', '1234567890987654321012345')
        result = self.db.get('first')
        part_1 = self.db.get('first', 1)
        part_2 = self.db.get('first', 2)
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, '1234567890')
        self.assertEqual(part_1, '9876543210')
        self.assertEqual(part_2, '12345')

    def test_large_file_not_in_mem(self):
        self.db.set('first', '1234567890987654321012345')
        result = list(self.db.data.keys())
        kvs_mech.delete_data_base('test')
        self.assertEqual(result, [])

    def test_list_of_dbs(self):
        db_1 = KeyValueStorage('test1', 3)
        result = kvs_mech.get_list_of_db()
        kvs_mech.delete_data_base('test')
        kvs_mech.delete_data_base('test1')
        self.assertEqual(result, ['test', 'test1'])


if __name__ == "__main__":
    unittest.main()
