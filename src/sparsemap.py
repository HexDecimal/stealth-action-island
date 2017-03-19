
from collections import defaultdict
import itertools

class SparseMap(object):
    """Basic container object for later optimization"""

    def __init__(self):
        super().__init__()
        self._objects = defaultdict(list)

    def area(self, x, y, width, height):
        for xyz in itertools.product(range(x, x + width),
                                     range(y, y + height), (0,)):
            if xyz in self._objects:
                yield from self._objects[xyz]

    def square(self, x, y, radius):
        width = radius * 2 + 1
        yield from self.area(x - radius, y - radius, width, width)

    def __iter__(self):
        yield from itertools.chain.from_iterable(self._objects.values())

    def __getitem__(self, xy):
        return self._objects[xy]
