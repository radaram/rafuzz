
class RequestParser():
    def __init__(self, fpath, backend):
        self.fpath = fpath
        self.backend = backend

    def open_file(self):
        with open(self.fpath, "r") as f:
            return f.read()

    def parse_text(self):
        text = self.open_file()
        return self.backend(text).parse_text()

