import unittest
from kvs_item import InformationOfItem


class TestInformationOfItem(unittest.TestCase):
    def setUp(self):
        self.items = {
            'first': InformationOfItem(True),
            'second': InformationOfItem(True),
            'third': InformationOfItem(True)
        }

    def test_unload_item_to_disc(self):
        self.items['first'].unload_to_disc()
        self.assertEqual(self.items['first'].is_data_in_mem, False)

    def test_load_item_to_mem(self):
        self.items['first'].unload_to_disc()
        self.items['first'].load_to_mem()
        self.assertEqual(self.items['first'].is_data_in_mem, True)

    def test_usage_frequency(self):
        self.items['first'].use()
        self.items['first'].use()
        self.assertEqual(self.items['first'].usage_freq, 3)

    def test_internal_method_repr(self):
        string = self.items['second'].__repr__()
        self.assertEqual(string, '1 True')

    def test_internal_method_str(self):
        string = self.items['third'].__str__()
        self.assertEqual(string, '1 True')


if __name__ == "__main__":
    unittest.main()
