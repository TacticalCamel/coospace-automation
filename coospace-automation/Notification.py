class Notification:
    def __init__(self, title, date, scene, tool, url):
        self._title = title
        self._date = date
        self._scene = scene
        self._tool = tool
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self._date

    @property
    def scene(self):
        return self._scene

    @property
    def tool(self):
        return self._tool

    @property
    def url(self):
        return self._url
