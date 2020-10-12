

class ExistenceError(Exception):
    def __init__(self, msg):
        self.message = msg


class NotExistenceError(Exception):
    def __init__(self, msg):
        self.message = msg


if __name__ == '__main__':
    pass
