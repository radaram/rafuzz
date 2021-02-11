import random


class ProxiesHandler(object):

    def __init__(self, fpath: str):
        self.proxies = self.open_file(fpath)

    def open_file(self, fpath):
        with open(fpath, "r") as f:
           return [item.strip() for item in f.readlines() if item.strip()]

    def get_random_proxy(self):
        return random.choice(self.proxies).strip()

    def exclude_not_working_proxy(self, proxy: str):
        self.proxies.remove(proxy)
 
