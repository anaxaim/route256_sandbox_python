from bisect import bisect_left, bisect_right, insort
from functools import reduce
from itertools import chain
from operator import iadd


class SortedList:
    DEFAULT_LOAD_FACTOR = 1000

    def __init__(self, iterable=None):

        self._len = 0
        self._load = self.DEFAULT_LOAD_FACTOR
        self._lists = []
        self._maxes = []
        self._index = []
        self._offset = 0

        if iterable is not None:
            self.update(iterable)

    def __iter__(self):
        return chain.from_iterable(self._lists)

    def add(self, value):
        _lists = self._lists
        _maxes = self._maxes

        if _maxes:
            pos = bisect_right(_maxes, value)

            if pos == len(_maxes):
                pos -= 1
                _lists[pos].append(value)
                _maxes[pos] = value
            else:
                insort(_lists[pos], value)

            self._expand(pos)
        else:
            _lists.append([value])
            _maxes.append(value)

        self._len += 1

    def update(self, iterable):
        _lists = self._lists
        _maxes = self._maxes
        values = sorted(iterable)

        if _maxes:
            if len(values) * 4 >= self._len:
                _lists.append(values)
                values = reduce(iadd, _lists, [])
                values.sort()
                self.clear()
            else:
                _add = self.add
                for val in values:
                    _add(val)
                return

        _load = self._load
        _lists.extend(values[pos:(pos + _load)] for pos in range(0, len(values), _load))
        _maxes.extend(sublist[-1] for sublist in _lists)
        self._len = len(values)
        del self._index[:]

    def clear(self):
        self._len = 0
        del self._lists[:]
        del self._maxes[:]
        del self._index[:]
        self._offset = 0

    def _expand(self, pos):
        _load = self._load
        _lists = self._lists
        _index = self._index

        if len(_lists[pos]) > (_load << 1):
            _maxes = self._maxes

            _lists_pos = _lists[pos]
            half = _lists_pos[_load:]
            del _lists_pos[_load:]
            _maxes[pos] = _lists_pos[-1]

            _lists.insert(pos + 1, half)
            _maxes.insert(pos + 1, half[-1])

            del _index[:]
        else:
            if _index:
                child = self._offset + pos
                while child:
                    _index[child] += 1
                    child = (child - 1) >> 1
                _index[0] += 1

    def _delete(self, pos, idx):
        _lists = self._lists
        _maxes = self._maxes
        _index = self._index

        _lists_pos = _lists[pos]

        del _lists_pos[idx]
        self._len -= 1

        len_lists_pos = len(_lists_pos)

        if len_lists_pos > (self._load >> 1):
            _maxes[pos] = _lists_pos[-1]

            if _index:
                child = self._offset + pos
                while child > 0:
                    _index[child] -= 1
                    child = (child - 1) >> 1
                _index[0] -= 1
        elif len(_lists) > 1:
            if not pos:
                pos += 1

            prev = pos - 1
            _lists[prev].extend(_lists[pos])
            _maxes[prev] = _lists[prev][-1]

            del _lists[pos]
            del _maxes[pos]
            del _index[:]

            self._expand(prev)
        elif len_lists_pos:
            _maxes[pos] = _lists_pos[-1]
        else:
            del _lists[pos]
            del _maxes[pos]
            del _index[:]

    def remove(self, value):
        _maxes = self._maxes

        pos = bisect_left(_maxes, value)

        _lists = self._lists
        idx = bisect_left(_lists[pos], value)

        if _lists[pos][idx] == value:
            self._delete(pos, idx)


class SortedSet:
    def __init__(self, iterable=None):
        self._set = set()
        self._list = SortedList(self._set)

        if iterable is not None:
            self.update(iterable)

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._set)

    def add(self, value):
        _set = self._set
        if value not in _set:
            _set.add(value)
            self._list.add(value)

    def remove(self, value):
        self._set.remove(value)
        self._list.remove(value)

    def update(self, *iterables):
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self.add
            for value in values:
                _add(value)
        return self


if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        input()
        n, q = input().split()

        coupes_dt = {j: [i-1, i] for j, i in enumerate(range(2, 2*int(n) + 1, 2))}
        coupes_keys = SortedSet(coupes_dt.keys())

        it = iter(range(int(q)))
        while True:
            try:
                next(it)

                query = input().split()
                if len(query) == 2:
                    p = int(query[1])
                    coupe_idx = p - (p // 2) - 1
                    coupe = coupes_dt[coupe_idx]
                    if query[0] == '1':
                        if p in coupe:
                            coupe.remove(p)
                            try:
                                coupes_keys.remove(coupe_idx)
                            except:
                                pass
                            print('SUCCESS')
                        else:
                            print('FAIL')
                    else:
                        if p not in coupe:
                            len_v = len(coupe)
                            if len_v == 0:
                                coupe.append(p)
                            elif len_v == 1:
                                if p > coupe[0]:
                                    coupe.append(p)
                                else:
                                    coupe.insert(0, p)
                                coupes_keys.add(coupe_idx)
                            print('SUCCESS')
                        else:
                            print('FAIL')
                else:
                    if coupes_keys:
                        empty_coupe = next(iter(coupes_keys))
                        coupes_keys.remove(empty_coupe)
                        print('SUCCESS {0}-{1}'.format(*coupes_dt[empty_coupe]))
                        coupes_dt[empty_coupe] = []
                    else:
                        print('FAIL')
            except:
                break
