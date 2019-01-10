from tube.base.Parallel import Parallel
from tube.base.Sequence import Sequence


class Block:

    name: str

    def invoke(self, data):
        return self.execute(data)

    def execute(self, data):
        return data

    def set_name(self, value: str) -> 'Block':
        self.name = value
        return self

    def __or__(self, next_block):
        return (
            Sequence([self, next_block])
        )

    def __and__(self, next_block):
        return Parallel([self, next_block])
