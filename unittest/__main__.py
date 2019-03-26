import unittest
import os
def main():
    loader = unittest.TestLoader()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_suite = loader.discover(current_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == "__main__":
    main()
