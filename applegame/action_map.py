class ActionMap:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.rects = []
        self._index = {}
        self._build()

    def _build(self):
        idx = 0
        for r1 in range(self.rows):
            for r2 in range(r1, self.rows):
                for c1 in range(self.cols):
                    for c2 in range(c1, self.cols):
                        rect = (r1, c1, r2, c2)
                        self.rects.append(rect)
                        self._index[rect] = idx
                        idx += 1

    @property
    def size(self):
        return len(self.rects)

    def decode(self, index):
        return self.rects[index]

    def encode(self, r1, c1, r2, c2):
        return self._index[(r1, c1, r2, c2)]
