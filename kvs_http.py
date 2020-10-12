from flask import Flask, request
import kvs_mech as kvs
import kvs_exceptions as kvs_e
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

DESCRIPTION = 'Server for Key Value Storage'
DBs = {}

app = Flask(__name__)


@app.route('/api/<db>/<key>', methods=['GET'])
def get_element(db, key):
    try:
        return str(DBs[db].get(key))
    except kvs_e.NotExistenceError as e:
        return 'Error with message: "{}"'.format(e.message)
    except Exception as e:
        return str(e)


@app.route('/api/<db>/<key>/<part>', methods=['GET'])
def get_part_of_element(db, key, part):
    try:
        if part is None:
            return str(DBs[db].get(key))
        else:
            return str(DBs[db].get(key, int(part)))
    except kvs_e.NotExistenceError as e:
        return 'Error with message: "{}"'.format(e.message)
    except Exception as e:
        return str(e)


@app.route('/api/<db>/<key>', methods=['POST'])
def set_element(db, key):
    try:
        is_add = False
        if key in DBs[db].list():
            is_add = True
        if request.data.decode('utf-8') != '':
            value = request.data.decode('utf-8')
        else:
            value = request.form.to_dict()['value']
        DBs[db].set(key, value, is_add)
    except kvs_e.ExistenceError as e:
        return e.message
    except Exception as e:
        return str(e)
    return 'Successfully set key "{0}" in db "{1}"'.format(key, db)


@app.route('/api/<db>/delete/<key>', methods=['GET'])
def del_element(db, key):
    try:
        DBs[db].delete(key)
    except kvs_e.NotExistenceError as e:
        return 'Error with message: "{}"'.format(e.message)
    return 'Element with key "{0}" in "{1}"' \
           ' db was successfully deleted'.format(key, db)


@app.route('/api/<db>/list', methods=['GET'])
def get_elements_list(db):
    try:
        if db not in kvs.get_list_of_db():
            return 'Database "{}" doesnt exist'.format(db)
        if db not in DBs:
            create(db)
        return str(DBs[db].list())
    except Exception as e:
        return str(e)


@app.route('/api/<db>', methods=['POST'])
def create(db):
    try:
        if db not in kvs.get_list_of_db():
            DBs[db] = kvs.KeyValueStorage(name=db)
            return 'Database "{}" successfully created'.format(db)
        else:
            DBs[db] = kvs.KeyValueStorage(name=db, is_new=False)
            return 'Database "{}" successfully upload'.format(db)
    except Exception as e:
        return str(e)


@app.route('/api/list', methods=['GET'])
def get_list():
    try:
        return str(kvs.get_list_of_db())
    except Exception as e:
        return str(e)


@app.route('/api/delete/<db>', methods=['GET'])
def delete_db(db):
    try:
        if db in DBs:
            del DBs[db]
        kvs.delete_data_base(db)
    except Exception as e:
        return str(e)
    return '"{}" was successfully deleted'.format(db)


def start_server(port):
    target = "localhost"
    target_ip = gethostbyname(target)
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((target_ip, port))
    s.close()

    if result != 0:
        app.run(port=port)
        return 'Server is turned off'

    return 'Port "{}" is unavailable'


if __name__ == '__main__':
    pass
