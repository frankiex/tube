from copy import copy
from functools import reduce
from pydash import assign


class Parallel:

    def __init__(self, initialize=None):
        self.parallel = initialize if initialize else []

    def append(self, block):
        self.parallel.append(block)
        return self

    def get_parallel(self):
        return self.parallel

    def execute(self, data=None):
        return reduce(
            lambda current_data, block:
                assign(
                    current_data,
                    block.execute(data)
                ),
            self.parallel,
            copy(data) if data else {}
        )

    def __and__(self, next_block):
        self.append(next_block)
        return self

    def __rshift__(self, next_block):
        from lib.base.Sequence import Sequence
        return Sequence([self, next_block])

    def __iter__(self):
        return iter(self.parallel)
