from lib.base.Parallel import Parallel
from lib.base.Sequence import Sequence


class Block:
    def __rshift__(self, next_block):
        return (
            Sequence([self, next_block])
        )

    def execute(self, data):
        return self.process(data)

    def process(self, data):
        return data

    def __and__(self, next_block):
        return Parallel([self, next_block])
