
from collections import defaultdict
import itertools

class SparseMap(object):
    """Basic container object for later optimization"""

    def __init__(self):
        self.__objects = defaultdict(list)

    def area(self, x, y, width, height):
        for xy in itertools.product(range(x, x + width), range(y, y + height)):
            if xy in self.__objects:
                yield from self.__objects[xy]

    def square(self, x, y, radius):
        width = radius * 2 + 1
        yield from self.area(x - radius, y - radius, width, width)

    def __iter__(self):
        yield from itertools.chain.from_iterable(self.__objects.values())

    def __getitem__(self, xy):
        return self.__objects[xy]
