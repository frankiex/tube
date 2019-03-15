import unittest
from pandas import DataFrame
from tube.blocks.datasets.CompareMeasurementAndPrint import CompareMeasurementAndPrint
from tube.types.Dataset import Dataset


class CompareAndPrintTest(unittest.TestCase):

    def test_compute(self):
        block = CompareMeasurementAndPrint("a")
        result = block.compute({
            "0": Dataset(DataFrame({}), label="dataset1", payload={
                "measurements": {
                    "a": 4,
                }
            }),
            "1": Dataset(DataFrame({}), label="dataset2",  payload={
                "measurements": {
                    "a": 6,
                }
            }),
            "2": Dataset(DataFrame({}), label="dataset3",  payload={
                "measurements": {
                    "a": 2,
                }
            })
        })

        self.assertEqual(
            result,
            [['dataset3', -3.0, 0, -2, -4], ['dataset1', 0.0, 2, 0, -2], ['dataset2', 3.0, 4, 2, 0]]
        )


if __name__ == '__main__':
    unittest.main()
