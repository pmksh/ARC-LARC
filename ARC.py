from collections import OrderedDict

class ARC:
    def __init__(self, cache_size):
        self.T1 = OrderedDict()
        self.T2 = OrderedDict()
        self.B1 = OrderedDict()
        self.B2 = OrderedDict()

        self.cache_size = cache_size
        self.p = 1
        self.cache_hits = 0
        self.cache_misses = 0

    def access(self, page):
        if page in self.T1 or page in self.T2:
            self.cache_hits += 1
            if page in self.T1:
                self.T1.pop(page)
                self.T2[page] = True
            else:
                self.T2.move_to_end(page)
        else:
            self.cache_misses += 1
            if page in self.B1:
                self.p = min(self.cache_size-1, self.p + max(1, len(self.B2) // max(1, len(self.B1))))
                self.B1.pop(page)
                self.T2[page] = True
            elif page in self.B2:
                self.p = max(1, self.p - max(1, len(self.B1) // max(1, len(self.B2))))
                self.B2.pop(page)
                self.T2[page] = True
            else:
                self.T1[page] = True

            if len(self.T1) + len(self.T2) > self.cache_size:
                if len(self.T1) < self.p:
                    old, _ = self.T2.popitem(last=False)
                    self.B2[old] = True
                else:
                    old, _ = self.T1.popitem(last=False)
                    self.B1[old] = True

            if len(self.T1) + len(self.T2) + len(self.B1) + len(self.B2) > 2 * self.cache_size:
                if len(self.B1) < self.p:
                    self.B2.popitem(last=False)
                else:
                    self.B1.popitem(last=False)

    def get_stats(self):
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses
        }
