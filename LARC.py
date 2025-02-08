from collections import OrderedDict

class LARC:
    def __init__(self, cache_size):
        self.Q = OrderedDict()
        self.Qr = OrderedDict()

        self.cache_size = cache_size
        self.cr = 0.1 * cache_size
        self.cache_hits = 0
        self.cache_misses = 0

    def access(self, page):
        if page in self.Q:
            self.cache_hits += 1
            self.Q.move_to_end(page, last=True)
            self.cr = max(0.1 * self.cache_size, self.cr - self.cache_size / (self.cache_size - self.cr))
        else:
            self.cache_misses += 1
            self.cr = min(0.9 * self.cache_size, self.cr + self.cache_size / self.cr)
            if page in self.Qr:
                self.Qr[page] = False
                self.Q[page] = True
                if len(self.Q) > self.cache_size:
                    old, _ = self.Q.popitem(last=False)
            else:
                self.Qr[page] = True
                if len(self.Qr) > self.cr:
                    self.Qr.popitem(last=False)

    def get_stats(self):
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses
        }
