import unittest
import os
if __name__ == "__main__":
    loader = unittest.TestLoader()
    currentDir = os.path.dirname(os.path.realpath(__file__))
    testSuite = loader.discover(currentDir)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testSuite)
