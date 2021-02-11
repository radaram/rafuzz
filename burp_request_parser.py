from request import Request


class BurpRequestParser(object):
    def __init__(self, text: str):
        self.text = text

    def parse_text(self):
        result = {
            "headers": {}
        }
        lines = self._split_into_list(self.text)
        request_method, path, http_version = lines[0].split(" ")
        result["method"] = request_method
        result["path"] = path
        result["http_version"] = http_version

        start_post_data = False
        i = 1
        for line in lines[1:]:
            if line in ("\n", ""):
                start_post_data = True
                break
            
            values = line.split(":")

            header = values[0].strip()
            value = ":".join(values[1:]).strip()
            result["headers"][header] = value
            i += 1
       
        post_data = ""
        if start_post_data and len(lines) > i:
            for line in lines[i+1:]:
                post_data += line

        if post_data:
            result["post_data"] = post_data

        url = result["headers"]["Host"] + path

        result["url"] = url

        return Request(result)

    def _split_into_list(self, text):
        return text.split("\n")


