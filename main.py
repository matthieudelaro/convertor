# This file describes the convertor classes and provides some tests.
# It has been designed for Python 3.5.1 Please upgrade if you
# are using Python 2.X version.

import sys
from Convertor import Convertor


def convert():
    if len(sys.argv) != 2:
        print("Please provide as unique argument the path of the" +
              "file which is to be parsed.")
    else:
        c = Convertor()
        res = c.parseFile(sys.argv[1])
        if res:
            print("Conversion failed for the following reason:", res)
        else:
            res = c.convert()
            res = c.formatOutput(res)
            print(res)
            return 0
    return -1


if __name__ == '__main__':
    convert()
