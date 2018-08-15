import unittest
from lib.base.Block import Block
from lib.base.Pipeline import Pipeline
from lib.blocks.Data import Data


class MultiplyBy(Block):

    def __init__(self, what, by):
        self.by = by
        self.what = what

    def process(self, input_data):
        return {
            self.what: input_data[self.what] * self.by
        }


class DefinedCompositionTest(unittest.TestCase):

    def test_basic_execution(self):

        result = Pipeline(
            Data({
                "number": 5,
            }) >>
            MultiplyBy("number", 2)
        ).execute()

        self.assertEqual(
            result,
            {"number": 10}
        )

    def test_composed_execution(self):

        result = Pipeline(
            (
                Data({
                    "number": 5,
                }) >>
                MultiplyBy("number", 2) >>
                MultiplyBy("number", 2)
            ) & (
                Data({
                    "number2": 1,
                }) >>
                MultiplyBy("number2", 2) >>
                MultiplyBy("number2", 2)
            )

        ).execute()

        self.assertEqual(
            result,
            {"number": 20, "number2": 4}
        )


if __name__ == '__main__':
    unittest.main()
