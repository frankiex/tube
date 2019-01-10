from collections import Mapping
from toolz import valmap
from tube.base.Block import Block
from tube.types import Invokable


class Map(Block):

    def __init__(self, block: Invokable):
        self.block = block

    def execute(self, data):
        return (
            (valmap if isinstance(data, Mapping) else map)(
                lambda value: self.block.invoke(value),
                data,
            )
        )
