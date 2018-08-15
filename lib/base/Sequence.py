from functools import reduce


class Sequence:

    def __init__(self, initialize=None):
        self.sequence = initialize if initialize else []

    def append(self, block):
        self.sequence.append(block)
        return self

    def get_sequence(self):
        return self.sequence

    def execute(self, data = None):
        result = reduce(
            lambda current_data, block:
                block.execute(current_data),
            self.sequence,
            data
        )
        return result

    def __rshift__(self, next_block):
        self.append(next_block)
        return self

    def __and__(self, next_block):
        from lib.base.Parallel import Parallel
        return Parallel([self, next_block])

    def __iter__(self):
        return iter(self.sequence)
