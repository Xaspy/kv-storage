import os
import argparse
import urllib3
from sys import platform
from multiprocessing import Process
from kvs_http import start_server


path_to_script = os.path.dirname(os.path.abspath(__file__))
serv_info_path = os.path.join(path_to_script, 'server_info')
DESCRIPTION = 'This is Key-Value Local Storage. ' \
              'Script can save data in keys, load ' \
              'data between disc and memory. ' \
              'Version - 1.0 by Xaspy'


def create_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-sa', '--set_address', nargs=1,
                        help='set address to connect db')
    parser.add_argument('-sp', '--set_port', nargs=1,
                        help='set port to connect db')
    parser.add_argument('-cs', '--check_selected', action='store_true',
                        help='check selected address and port')
    parser.add_argument('-c', '--create', nargs=1,
                        help='create the database')
    parser.add_argument('-dd', '--delete_database', nargs=1,
                        help='delete the database')
    parser.add_argument('-ld', '--list_databases', action='store_true',
                        help='list of existing databases')
    parser.add_argument('-sd', '--select_database', nargs=1,
                        help='select the database to work with')
    parser.add_argument('-s', '--set', nargs=2,
                        help='set value with key in selected database')
    parser.add_argument('-g', '--get', nargs='+',
                        help='get value by key in selected database')
    parser.add_argument('-d', '--delete', nargs=1,
                        help='delete item by key in selected database')
    parser.add_argument('-l', '--list', action='store_true',
                        help='get list of items in selected database')
    parser.add_argument('-ss', '--start_server', nargs=1,
                        help='starts local server with chosen port'
                             '(write "exit" to shut down server)')
    return parser


def main():
    parser = create_parser()
    namespace = parser.parse_args()

    ss = namespace.start_server
    if ss:
        port = int(ss[0])
        p = Process(target=start_server, args=(port,))
        p.start()
        os.system('cmd')
        p.terminate()

    set_addr = namespace.set_address
    if set_addr:
        prints = ArgParseHandler.save_connect_info(set_addr[0],
                                                   'address',
                                                   serv_info_path)
        print(prints)

    set_port = namespace.set_port
    if set_port:
        prints = ArgParseHandler.save_connect_info(set_port[0],
                                                   'port',
                                                   serv_info_path)
        print(prints)

    check_selected = namespace.check_selected
    if check_selected:
        data = ArgParseHandler.get_server_data(serv_info_path,
                                               ['address',
                                                'port',
                                                'selected_db'])
        if isinstance(data, dict):
            print('Selected: \nDB - "{0}" \nADDRESS - "{1}", PORT - "{2}"'
                  .format(data['selected_db'], data['address'], data['port']))
        else:
            print(data)

    create_db = namespace.create
    if create_db:
        db_name = str(create_db[0])
        prints = ArgParseHandler.post_request_db(serv_info_path, db_name)
        print(prints)

    del_db = namespace.delete_database
    if del_db:
        db_name = str(del_db[0])
        prints = ArgParseHandler.get_request_db(serv_info_path,
                                                'delete/{0}'.format(db_name))
        print(prints)

    list_db = namespace.list_databases
    if list_db:
        prints = ArgParseHandler.get_request_db(serv_info_path, 'list')
        print(prints)

    sel_db = namespace.select_database
    if sel_db:
        prints = ArgParseHandler.save_connect_info(sel_db[0],
                                                   'selected_db',
                                                   serv_info_path)
        print(prints)

    set_kv = namespace.set
    if set_kv:
        db_name = ArgParseHandler.get_selected_db_name(serv_info_path)
        key = set_kv[0]
        value = set_kv[1]
        prints = ArgParseHandler.post_request_db(serv_info_path,
                                                 '{0}/{1}'.format(db_name,
                                                                  key),
                                                 value)
        print(prints)

    del_kv = namespace.delete
    if del_kv:
        db_name = ArgParseHandler.get_selected_db_name(serv_info_path)
        key = del_kv[0]
        prints = ArgParseHandler.get_request_db(serv_info_path,
                                                '{0}/delete/{1}'.format(
                                                    db_name, key))
        print(prints)

    get_kv = namespace.get
    if get_kv:
        db_name = ArgParseHandler.get_selected_db_name(serv_info_path)
        key = get_kv[0]
        part = 0
        if len(get_kv) > 1:
            part = int(get_kv[1])
        prints = ArgParseHandler.get_request_db(serv_info_path,
                                                '{0}/{1}/{2}'.format(
                                                    db_name, key, part))
        print(prints)

    list_kv = namespace.list
    if list_kv:
        db_name = ArgParseHandler.get_selected_db_name(serv_info_path)
        prints = ArgParseHandler.get_request_db(serv_info_path,
                                                '{0}/list'.format(
                                                    db_name))
        print(prints)

    starts = namespace.start_server
    if starts:
        prints = ArgParseHandler.start_own_server(int(starts[0]))
        print(prints)


class ArgParseHandler:
    @staticmethod
    def start_own_server(port):
        p = Process(target=start_server, args=(port,))
        p.start()
        if platform == "win32":
            os.system('cmd')
            p.terminate()
        return 'Server is turned off'

    @staticmethod
    def save_connect_info(info, name, path_to_server):
        try:
            path = os.path.join(path_to_server, name)
            result = ArgParseHandler._save_data(info, path)
            return result
        except Exception as e:
            return e

    @staticmethod
    def post_request_db(path_to_server, action, data=0):
        try:
            db_info = ArgParseHandler.get_server_data(path_to_server,
                                                      ['address', 'port'])
            http = urllib3.PoolManager()
            result = http.request('POST', 'http://{0}:{1}/api/{2}'
                                  .format(db_info['address'],
                                          db_info['port'],
                                          action), fields={'value': data})
            return result.data.decode('utf-8')
        except Exception as e:
            print(e)

    @staticmethod
    def get_request_db(path_to_server, action):
        try:
            data = ArgParseHandler.get_server_data(path_to_server,
                                                   ['address', 'port'])
            http = urllib3.PoolManager()
            result = http.request('GET', 'http://{0}:{1}/api/{2}'
                                  .format(data['address'],
                                          data['port'],
                                          action))
            return result.data.decode('utf-8')
        except Exception as e:
            print(e)

    @staticmethod
    def get_server_data(path, files: list):
        try:
            result = dict()
            for file in files:
                with open(os.path.join(path, file), 'r') as f:
                    result[file] = f.read()
            return result
        except Exception as e:
            return e

    @staticmethod
    def get_selected_db_name(path):
        try:
            db_name = ArgParseHandler.get_server_data(
                path, ['selected_db']
            )['selected_db']
            return db_name
        except Exception as e:
            print(e)

    @staticmethod
    def _save_data(data, path):
        try:
            with open(path, 'w') as f:
                f.write(data)
            return 'Successfully selected "{}"'.format(data)
        except Exception as e:
            return e


if __name__ == '__main__':
    main()
