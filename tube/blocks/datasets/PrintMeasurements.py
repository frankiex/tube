from tube.base.Block import Block
from tube.functions.utils import title, table
from tube.types.Dataset import Dataset


class PrintMeasurements(Block):
    def execute(self, dataset: Dataset) -> Dataset:
        print()
        if dataset.label:
            print(title("Measurements for %s" % dataset.label))
        try:
            measurements = dataset.payload["measurements"]
        except KeyError:
            print("No measurements\n")
            return dataset

        print(table(measurements.items()))
        return dataset
