class UrlBuilder:
    def __init__(self, apiURL):
        self.__apiURL = apiURL

    def build_url(self, *parts):
        part = '/'.join(str(x) for x in parts)
        return '{}/{}'.format(self.__apiURL, part)
