class Paginator:
    def __init__(self, query, max, page):
        self.query = query
        self.max = max
        self.page = page

    def get_page(self):
        return self.query.limit(self.max).offset(self.page * self.max)

    def has_next_page(self):
        return self.page < (self.query.count() / self.max) - 1

    def next_page(self):
        return self.page + 1

    def prev_page(self):
        return self.page - 1
