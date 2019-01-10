from tube.types.Mergable import Mergable
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Union
from pandas import DataFrame


@dataclass
class Dataset(Mergable):
    frame: DataFrame
    label: str = None
    payload: dict = field(default_factory=lambda: {})

    def merge(self, what: Union['Dataset', DataFrame]) -> 'Dataset':
        frame_to_merge = what.frame if isinstance(what, Dataset) else what
        return Dataset(
            frame=self.frame.join(frame_to_merge),
            label=self.label,
            payload=deepcopy(self.payload)
        )
