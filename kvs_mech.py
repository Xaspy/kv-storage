import json
import os
import sys
import shutil
import math
import kvs_exceptions as exceptions
import kvs_item as item


ITEM_MAX_SIZE = 10


class KeyValueStorage:
    def __init__(self, name, limit=10000, is_new=True):
        path_to_script = os.path.dirname(os.path.abspath(__file__))
        if is_new:
            _create_new_info(name, path_to_script)
            path_to_script = os.path.join(path_to_script, 'dbs')
            self.path = os.path.join(path_to_script, str(name))
            os.mkdir(self.path)
            self.data = {}
            self.existence_and_usage = {}
            self.limit = limit
        else:
            _check_info(name, path_to_script)
            path_to_script = os.path.join(path_to_script, 'dbs')
            self.path = os.path.join(path_to_script, str(name))
            self.existence_and_usage = {}
            self._fill_existence_and_usage()
            self.data = {}
            self.limit = limit

    def set(self, key, value, is_add=False):
        """
        Setting data by key in disc and memory if the limit is NOT exceeded
        and only in disc if the limit is exceeded
        :param key: Key of item
        :param value: Value of item
        :param is_add: Bool which tell us about partition adding to key
        """
        if len(self.data) < self.limit:
            self._save_new_item(key, value, is_add)
        else:
            self._unload_rarely_item()
            self._save_new_item(key, value, is_add)

    def get(self, key, part=0):
        """
        Getting data from an element by key
        :param key: Key of item
        :param part: Part of the item to getting
        :return: Value from item by key
        """
        try:
            self.existence_and_usage[key].use()
        except KeyError:
            raise exceptions.NotExistenceError('This key does not exist')
        if self._is_there_less_usage(key) and self.limit <= len(self.data):
            self._unload_rarely_item()
            self._load_regular_item()
        elif len(self.data) < self.limit:
            self._load_regular_item()

        if self.existence_and_usage[key].is_data_in_mem:
            return self.data[key]
        else:
            path_to_item = os.path.join(self.path, str(key))
            item_size = os.path.getsize(path_to_item)
            if item_size > ITEM_MAX_SIZE:
                i = math.ceil(item_size / ITEM_MAX_SIZE)
                with open(path_to_item, 'r', encoding='utf-8') as f:
                    for j in range(i):
                        data_from_disc = f.read(ITEM_MAX_SIZE)
                        if j == part:
                            break
            return data_from_disc

    def delete(self, key):
        """
        Delete item from disc and memory
        :param key: Key of item to delete
        """
        path_to_item = os.path.join(self.path, str(key))
        os.remove(path_to_item)
        if self.existence_and_usage[key].is_data_in_mem:
            del self.data[key]
        del self.existence_and_usage[key]

    def list(self):
        self._fill_existence_and_usage()
        return list(self.existence_and_usage.keys())

    def _fill_existence_and_usage(self):
        for key in os.listdir(self.path):
            if key not in self.existence_and_usage:
                self.existence_and_usage[key] = item.InformationOfItem(False)

    def _save_new_item(self, key, value, is_add=False):
        """
        Save new item in disc and memory
        :param key: Key of item
        :param value: Value of item
        """
        if not is_add:
            if len(value) <= ITEM_MAX_SIZE:
                self.data[key] = value
                self.existence_and_usage[key] = item.InformationOfItem(True)
            else:
                self.existence_and_usage[key] = item.InformationOfItem(False)
        path_to_item = os.path.join(self.path, str(key))
        if is_add:
            self.existence_and_usage[key].use()
            if key in self.data.keys():
                if len(self.data[key]) + len(value) > ITEM_MAX_SIZE:
                    self.existence_and_usage[key] = item\
                        .InformationOfItem(False)
                    del self.data[key]
                else:
                    self.data[key] += value
            with open(path_to_item, 'a', encoding='utf-8') as f:
                f.write(value)
        else:
            with open(path_to_item, 'w', encoding='utf-8') as f:
                f.write(value)

    def _unload_item(self, key):
        self.existence_and_usage[key].unload_to_disc()
        del self.data[key]

    def _unload_rarely_item(self):
        """
        Load rarely item to disc
        """
        if len(self.existence_and_usage) > 0:
            rarity = sys.maxsize
            key = ''
            for iter_key in self.existence_and_usage:
                if self.existence_and_usage[iter_key].is_data_in_mem and\
                        self.existence_and_usage[iter_key].usage_freq <\
                        rarity:
                    rarity = self.existence_and_usage[iter_key].usage_freq
                    key = iter_key

            self.existence_and_usage[key].unload_to_disc()
            del self.data[key]

    def _load_regular_item(self):
        """
        Load regular item to memory
        """
        path_to_item = ''
        if len(self.existence_and_usage) > 0:
            rarity = 0
            key = ''
            for iter_key in self.existence_and_usage:
                path_to_item = os.path.join(self.path, str(iter_key))
                item_size = os.path.getsize(path_to_item)
                if not self.existence_and_usage[iter_key].is_data_in_mem\
                        and self.existence_and_usage[iter_key]\
                        .usage_freq > rarity and \
                        item_size <= ITEM_MAX_SIZE:
                    rarity = self.existence_and_usage[iter_key].usage_freq
                    key = iter_key

            if key == '':
                return

            with open(path_to_item, 'r', encoding='utf-8') as f:
                data_from_disc = f.read()
            self.existence_and_usage[key].load_to_mem()
            self.data[key] = data_from_disc

    def _is_there_less_usage(self, key):
        """
        Is there less used item in memory
        """
        if len(self.existence_and_usage) > 0:
            for iter_key in self.existence_and_usage:
                if iter_key != key and \
                        self.existence_and_usage[iter_key].is_data_in_mem\
                        and self.existence_and_usage[iter_key].usage_freq < \
                        self.existence_and_usage[key].usage_freq:
                    return True
            return False


def get_list_of_db():
    """
    Get list of databases
    :return: List of all dbs
    """
    path_to_script = os.path.dirname(os.path.abspath(__file__))
    path_to_info = os.path.join(path_to_script, 'kv_storage_sys')
    path_to_info = os.path.join(path_to_info, 'kv_storage_info')
    if os.path.exists(path_to_info):
        with open(path_to_info, 'r', encoding='utf-8') as file_to_load:
            list_of_names = json.load(file_to_load)
        return list_of_names
    else:
        raise exceptions.NotExistenceError(
            'Information about databases does not exist'
        )


def _create_new_info(name, path_to_script):
    list_of_names = list()
    path_to_info = os.path.join(path_to_script, 'kv_storage_sys')
    path_to_info = os.path.join(path_to_info, 'kv_storage_info')
    if os.path.exists(path_to_info):
        with open(path_to_info, 'r', encoding='utf-8') as file_to_load:
            list_of_names = json.load(file_to_load)
        if name in list_of_names:
            raise exceptions.ExistenceError('Database "{}" already exist'
                                            .format(name))
    list_of_names.append(name)
    with open(path_to_info, 'w', encoding='utf-8') as file_to_save:
        json.dump(list_of_names, file_to_save)


def _check_info(name, path_to_script):
    path_to_info = os.path.join(path_to_script, 'kv_storage_sys')
    path_to_info = os.path.join(path_to_info, 'kv_storage_info')
    if os.path.exists(path_to_info):
        with open(path_to_info, 'r', encoding='utf-8') as file_to_load:
            list_of_names = json.load(file_to_load)
        if name not in list_of_names:
            raise exceptions.NotExistenceError('Database "{}" does not exist'
                                               .format(name))


def delete_data_base(name):
    """
    Delete full data base by name
    :param name: Name of database whose you delete
    """
    path_to_script = os.path.dirname(os.path.abspath(__file__))
    path_to_info = os.path.join(path_to_script, 'kv_storage_sys')
    path_to_info = os.path.join(path_to_info, 'kv_storage_info')
    path_to_script = os.path.join(path_to_script, 'dbs')
    if os.path.exists(path_to_info):
        with open(path_to_info, 'r', encoding='utf-8') as file_to_load:
            list_of_names = json.load(file_to_load)
        if name not in list_of_names:
            raise exceptions.NotExistenceError('Database "{}" does not exist'
                                               .format(name))
    else:
        raise exceptions.NotExistenceError(
            'Information about databases does not exist'
        )
    list_of_names.remove(name)
    with open(path_to_info, 'w', encoding='utf-8') as file_to_save:
        json.dump(list_of_names, file_to_save)
    path_to_db = os.path.join(path_to_script, str(name))
    shutil.rmtree(path_to_db)


if __name__ == '__main__':
    pass
