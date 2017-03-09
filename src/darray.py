
import itertools

import numpy as np

class DynamicArray(object):

    def __init__(self, chunk_shape, dtype, default=None):
        self.dimensions = len(chunk_shape)
        self.chunk_shape = np.asarray(chunk_shape)
        self.dtype = dtype
        self.default = self.default_chunk if default is None else default
        self.chunk_map = {}

    def generate_chunk(self, chunk_index):
        assert tuple(chunk_index) not in self.chunk_map
        chunk_index = np.asarray(chunk_index)
        mgrid = np.mgrid[[slice(pos * size, pos * size + size)
                          for pos, size in zip(chunk_index, self.chunk_shape)]]
        array = self.default(mgrid)
        self.chunk_map[tuple(chunk_index)] = array
        return array

    def default_chunk(self, mgrid):
        return np.zeros(self.chunk_shape, self.dtype)

    def get_chunk(self, index):
        try:
            return self.chunk_map[index]
        except KeyError:
            return self.generate_chunk(index)

    def _shape_from_index(self, index):
        for item in index:
            if not isinstance(item, slice):
                yield 1
            else:
                yield item.stop - (item.start or 0)

    def _parse_axis(self, slice_, chunk_size):
        if not isinstance(slice_, slice):
            slice_ %= chunk_size
            yield 0, slice_ % chunk_size, slice_ // chunk_size
            return
        slice_ = slice(
            slice_.start if slice_.start is not None else 0,
            slice_.stop,
            slice_.step if slice_.step is not None else 1,
            )
        start = slice_.start
        stop = slice_.stop
        step = slice_.step
        assert stop is not None
        assert step == 1

        while start < stop:
            chunk_slice = slice(
                start % chunk_size,
                min(chunk_size,
                    start % chunk_size + stop - start),
                step,
                )
            array_slice = slice(
                start - slice_.start,
                start - slice_.start + (chunk_slice.stop - chunk_slice.start),
                step,
                )
            yield(array_slice, chunk_slice, start // chunk_size)
            start = (start // chunk_size + 1) * chunk_size

    def _parse_index(self, index):
        return itertools.product(*(self._parse_axis(i, s)
                                   for i,s in zip(index, self.chunk_shape)))

    def __getitem__(self, index):
        assert len(index) == self.dimensions
        array = np.empty(tuple(self._shape_from_index(index)), self.dtype)
        for chunk in self._parse_index(index):
            arr_slice, chunk_slice, chunk_index = zip(*chunk)
            array[arr_slice] = self.get_chunk(chunk_index)[chunk_slice]
        return array

    def __setitem__(self, index, value):
        if isinstance(value, np.ndarray):
            assert tuple(self._shape_from_index(index)) == value.shape, \
                'Expected a shape of %s, got %s' % (
                    tuple(self._shape_from_index(index)), value.shape)
        for chunk in self._parse_index(index):
            arr_slice, chunk_slice, chunk_index = zip(*chunk)
            if isinstance(value, np.ndarray):
                self.get_chunk(chunk_index)[chunk_slice] = value[arr_slice]
            else:
                self.get_chunk(chunk_index)[chunk_slice] = value


if __name__ == '__main__':
    iarr = DynamicArray((2, 2), np.int)
    iarr[:100,:100] = np.mgrid[0:100,0:100][0]
    iarr[32:35,0] = 0
    iarr[33:36,1] = 1
    print(iarr[32:39,:3])
