# This file describes the convertor classes and provides some tests.
# It has been designed for Python 3.5.1 Please upgrade if you
# are using Python 2.X version.

import unittest
import csv
from decimal import Decimal


class Edge:
    def __init__(self, source, value, destination):
        self.source = source
        self.destination = destination
        self.value = value

    def __str__(self):
        return self.source + "=>" + str(self.value) + "=>" + self.destination


class Convertor:
    def parseFile(self, filepath):
        """Parses file given by filepath argument.
        Returns a non empty string in case of error.
        Builds the graph of currency conversions, and stores it.
        Computes and stores the best path of converstion as well."""
        self._graph = {}
        self._path = None
        self._rules = []

        csvFile = open(filepath)
        reader = csv.reader(csvFile, delimiter=';')
        firstLine = True
        try:
            for row in reader:
                if len(row) != 3:
                    return "invalid_format"
                for cell in row:
                    if not cell:
                        return "invalid_format"

                if firstLine:
                    self._DS = row[0]
                    self._MS = Decimal(row[1])
                    self._DD = row[2]
                    self._graph[self._DS] = []
                    firstLine = False
                else:
                    TDS = row[0]
                    TDD = row[1]
                    TC = Decimal(row[2])
                    self._graph[TDS] = self._graph.get(TDS, []) + [TDD]
                    self._graph[TDD] = self._graph.get(TDD, []) + [TDS]
                    self._rules.append(Edge(TDS, TC, TDD))
                    self._rules.append(Edge(TDD, Decimal(1.0)/TC, TDS))
        except Exception as e:
            return "invalid_format"
        finally:
            csvFile.close()

        if firstLine:
            return "invalid_format"
        if self._DS == self._DD:
            self._path = None  # nothing to be done
        else:
            self._path = findShortestPath(self._graph, self._DS, self._DD)
            if not self._path:
                return "missing_path"
        return ""

    def convert(self):
        """Applies the conversion. Returns the result."""
        if self._path is None:  # nothing to be done
            return self._MS
        else:
            res = Decimal(self._MS)
            for source,destination in zip(self._path[0::1], self._path[1::1]):
                coef = ([edge.value
                        for edge in self._rules
                        if edge.source == source and edge.destination == destination])[0]
                res = res * coef
            return res

    def formatOutput(self, number):
        """Returns the provided number as a string, properly formated."""
        return "%0.2f" % (number,)


def findShortestPath(graph, start, end, path=[]):
    """Reference: https://www.python.org/doc/essays/graphs/"""
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.c = Convertor()

    def test_valid(self):
        res = self.c.parseFile("examples/validExample.txt")
        self.assertEqual(res, "")

        res = self.c.convert()

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
        self.assertEqual(res, "invalid_format")

    def test_missing_root(self):
        res = self.c.parseFile("examples/missingRootExample.txt")
        self.assertEqual(res, "missing_path")

    def test_missing_path(self):
        res = self.c.parseFile("examples/missingPathExample.txt")
        self.assertEqual(res, "missing_path")

    def test_empty_example(self):
        res = self.c.parseFile("examples/emptyExample.txt")
        self.assertEqual(res, "invalid_format")

    def test_invalid_format1(self):
        res = self.c.parseFile("examples/invalidFormat1.txt")
        self.assertEqual(res, "invalid_format")

    def test_invalid_format2(self):
        res = self.c.parseFile("examples/invalidFormat2.txt")
        self.assertEqual(res, "invalid_format")

    def test_invalid_format3(self):
        res = self.c.parseFile("examples/invalidFormat3.txt")
        self.assertEqual(res, "invalid_format")

    def test_invalid_format4(self):
        res = self.c.parseFile("examples/invalidFormat4.txt")
        self.assertEqual(res, "invalid_format")


if __name__ == '__main__':
    unittest.main()
