#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../../src/before')

import unittest
import HW_polyn2_2014_M1_summer as hw


class TestSgnPrint(unittest.TestCase):
    def test(self):
        self.assertEqual('+', hw.sgn_print(0, False))
        self.assertEqual('',  hw.sgn_print(0, True))
        self.assertEqual('-', hw.sgn_print(1, False))
        self.assertEqual('-', hw.sgn_print(1, True))


class TestIntCoeff(unittest.TestCase):
    def test(self):
        self.assertEqual('',  hw.int_coeff(1))
        self.assertEqual('2', hw.int_coeff(2))


class TestFracCoeff(unittest.TestCase):
    def test(self):
        self.assertEqual('', hw.frac_coeff(1))
        self.assertEqual(r'\myfrac{1}{2}', hw.frac_coeff(2))


class TestBracketPrint(unittest.TestCase):
    def test(self):
        self.assertEqual('(x+1)',   hw.bracket_print(0, 1, 'x', 0, 1))
        self.assertEqual('(-y-1)',  hw.bracket_print(1, 1, 'y', 1, 1))
        self.assertEqual('(2z+2)',  hw.bracket_print(0, 2, 'z', 0, 2))
        self.assertEqual('(-2w-2)', hw.bracket_print(1, 2, 'w', 1, 2))


if __name__ == '__main__':
    unittest.main()