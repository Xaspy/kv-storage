

class InformationOfItem:
    def __init__(self, is_data_in_mem):
        self.is_data_in_mem = is_data_in_mem
        self.usage_freq = 1

    def __str__(self):
        string = str(self.usage_freq) + ' ' + str(self.is_data_in_mem)
        return string

    def __repr__(self):
        string = str(self.usage_freq) + ' ' + str(self.is_data_in_mem)
        return string

    def use(self):
        self.usage_freq += 1

    def load_to_mem(self):
        self.is_data_in_mem = True

    def unload_to_disc(self):
        self.is_data_in_mem = False


def main():
    pass


if __name__ == '__main__':
    main()
