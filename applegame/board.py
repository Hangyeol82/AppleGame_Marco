import numpy as np


def _prefix_sum(values):
    rows, cols = values.shape
    prefix = np.zeros((rows + 1, cols + 1), dtype=np.int32)
    prefix[1:, 1:] = values.cumsum(axis=0).cumsum(axis=1)
    return prefix


def _rect_sum(prefix, r1, c1, r2, c2):
    r1 += 1
    c1 += 1
    r2 += 1
    c2 += 1
    return (
        prefix[r2, c2]
        - prefix[r1 - 1, c2]
        - prefix[r2, c1 - 1]
        + prefix[r1 - 1, c1 - 1]
    )


class Board:
    def __init__(self, rows, cols, values=None):
        self.rows = rows
        self.cols = cols
        if values is None:
            self.values = np.zeros((rows, cols), dtype=np.int8)
        else:
            self.values = values.astype(np.int8, copy=True)

    def randomize(self, rng):
        self.values = rng.integers(1, 10, size=(self.rows, self.cols), dtype=np.int8)

    def rect_sum(self, r1, c1, r2, c2):
        return int(self.values[r1 : r2 + 1, c1 : c2 + 1].sum())

    def rect_nonzero(self, r1, c1, r2, c2):
        return int(np.count_nonzero(self.values[r1 : r2 + 1, c1 : c2 + 1]))

    def apply_rect(self, r1, c1, r2, c2):
        rect = self.values[r1 : r2 + 1, c1 : c2 + 1]
        rect_sum = int(rect.sum())
        if rect_sum != 10:
            return False, 0
        removed = int(np.count_nonzero(rect))
        rect[...] = 0
        return True, removed

    def valid_action_mask(self, action_map):
        prefix = _prefix_sum(self.values)
        nonzero = (self.values > 0).astype(np.int32)
        nonzero_prefix = _prefix_sum(nonzero)
        mask = np.zeros(action_map.size, dtype=bool)
        for idx, (r1, c1, r2, c2) in enumerate(action_map.rects):
            rect_sum = _rect_sum(prefix, r1, c1, r2, c2)
            if rect_sum != 10:
                continue
            rect_count = _rect_sum(nonzero_prefix, r1, c1, r2, c2)
            if rect_count > 0:
                mask[idx] = True
        return mask
