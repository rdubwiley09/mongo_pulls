#!projectenv/bin/python3
import json, pdb
from requests import put, get
import unittest
import pdb

class TestScript(unittest.TestCase):

    def test_hello_world(self):
        self.assertEqual("hello", "hello")

if __name__ == '__main__':
    unittest.main()
