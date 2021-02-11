
class Request(object):
    def __init__(self, data: dict):
        self.data = data
    
    def __getattr__(self, name: str):
        try:
            return self.data[name]
        except KeyError:
            return None

    def __setitem__(self, key, item):
        self.data[key] = item

    def __getitem__(self, key):
        return self.data[key]
    
    def __str__(self):
        request_text = f"{self.method} {self.path} {self.http_version}\n"
        headers = "\n".join(["{}: {}".format(h, v) for h, v in self.headers.items()])
        request_text += headers
        if self.post_data:
            request_text += "\n\n" + self.post_data

        return request_text

    def items(self):
        return self.data.items()

    def set_data(self, data: dict):
        self.data = data
    
    def get_data(self):
        return self.data


