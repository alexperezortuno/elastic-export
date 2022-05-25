class ElasticParams:
    def __init__(self, gte=None,
                 lte=None,
                 size=10,
                 query='',
                 query_string='',
                 scroll='1m',
                 scroll_id=None,
                 file=None,
                 headers=False,
                 sort=None,
                 showquery=False,
                 rawquery='',
                 max_size: int = None,
                 max_content: int = None,
                 output_path=None,
                 count=0):
        self.gte = gte
        self.lte = lte
        self.size = size
        self.query = query
        self.query_string = query_string
        self.scroll = scroll
        self.scroll_id = scroll_id
        self.file = file
        self.headers = headers
        self.sort = sort
        self.showquery = showquery
        self.rawquery = rawquery
        self.max_size = max_size
        self.max_content = max_content
        self.output_path = output_path
        self.count = count

    def __hash__(self):
        return hash((self.gte,
                     self.lte,
                     self.size,
                     self.query,
                     self.query_string,
                     self.scroll,
                     self.scroll_id,
                     self.file,
                     self.headers,
                     self.sort,
                     self.showquery,
                     self.rawquery,
                     self.max_size,
                     self.max_content,
                     self.output_path,
                     self.count))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)
