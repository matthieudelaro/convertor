# This file describs the convertor classes and provides some tests.
# It has been designed for Python 3.5.1 Please upgrade if you
# are using Python 2.X version.

import unittest
import csv

class Convertor:
    def parseFile(self, path):
        """Parses file given by path argument.
        Returns a non empty string in case of error.
        Builds the graph of currency conversions, and stores it.
        Computes and stores the best path of converstion as well."""
        self.fileContent = ""
        self.graph = None
        self.path = None
        pass

    def convert(self):
        """Applies the conversion. Returns the result."""
        raise NotImplementedError("convert is not implemented yet")
        pass

    def formatOutput(self, number):
        """Returns the provided number as a string, properly formated."""
        pass


class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.c = Convertor()

    def test_valid(self):
        res = self.c.parseFile("examples/validExample.txt")
        self.assertEqual(res, "")

        res = self.c.convert()
        self.assertEqual(res, 23.70)

        res = self.c.formatOutput(res)
        self.assertEqual(res, "23.70")

    def test_nothing_to_be_done(self):
        res = self.c.parseFile("examples/nothingToBeDone.txt")
        self.assertEqual(res, "")

        res = self.c.convert()
        self.assertEqual(res, 20.00)

        res = self.c.formatOutput(res)
        self.assertEqual(res, "20.00")

    def test_missing_first_line(self):
        res = self.c.parseFile("examples/missingFirstLineExample.txt")
        self.assertEqual(res, "missing_first_line")

    def test_missing_root(self):
        res = self.c.parseFile("examples/missingRootExample.txt")
        self.assertEqual(res, "missing_root")

    def test_missing_path(self):
        res = self.c.parseFile("examples/missingPathExample.txt")
        self.assertEqual(res, "missing_path")

    def test_empty_example(self):
        res = self.c.parseFile("examples/emptyExample.txt")
        self.assertEqual(res, "missing_first_line")


if __name__ == '__main__':
    unittest.main()
