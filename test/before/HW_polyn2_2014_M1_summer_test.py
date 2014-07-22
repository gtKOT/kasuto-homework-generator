#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../../src/before')

import unittest
import HW_polyn2_2014_M1_summer as hw


class TestSgnPrint(unittest.TestCase):
    def test(self):
        self.assertEqual(hw.sgn_print(0, False), '+')
        self.assertEqual(hw.sgn_print(0, True),  '')
        self.assertEqual(hw.sgn_print(1, False), '-')
        self.assertEqual(hw.sgn_print(1, True),  '-')


class TestIntCoeff(unittest.TestCase):
    def test(self):
        self.assertEqual(hw.int_coeff(1), '')
        self.assertEqual(hw.int_coeff(2), '2')


if __name__ == '__main__':
    unittest.main()