# -*- coding: utf-8 -*-


from captchasniper.multipart import post_multipart


class CaptchaSniperApi(object):
    _url = None

    def __init__(self, url: str):
        """
        url is the url string of the captcha sniper server.
        You may specify a port inside the url string (like http://SOMESERVER:PORT)
        """
        self.url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def solve(self, file_name: (object, str)) -> str:
        """
        Solve the captcha file passed as arg.
        file_name can be a str path or a fileobject (read() method)

        return a str representing the solved captcha or none if the captcha can't be solved
        """
        if hasattr(file_name, 'read'):
            return self.solve_raw(file_name.read())
        with open(file_name, 'rb') as f:
            return self.solve_raw(f.read())

    def solve_raw(self, data: bytes) -> str:
        """
        data: value of the captcha to solve

        return a str representing the solved captcha or none if the captcha can't be solved
        """
        resolved = post_multipart(self.url, {}, {'pict': {'filename': "captcha", 'content': data}})
        resolved = resolved if isinstance(resolved, str) else str(resolved, 'utf-8')
        results = resolved.split("|")
        result_code = results[0]
        if result_code == "0":
            return results[-1]
        return None
