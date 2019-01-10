from typing import Callable, Any

from tube.base.Block import Block


class Function(Block):

    def __init__(self, function: Callable[[Any], Any]):
        self.function = function

    def execute(self, data):
        return self.function(data)
