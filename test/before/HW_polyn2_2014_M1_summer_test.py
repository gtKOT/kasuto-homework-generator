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


class TestBracketFracstylePrint(unittest.TestCase):
    def test(self):
        self.assertEqual(r'\myfrac{(x+1)}{2}',   hw.bracket_fracstyle_print(2, 0, 1, 'x', 0, 1))
        self.assertEqual(r'\myfrac{(-y-1)}{3}',  hw.bracket_fracstyle_print(3, 1, 1, 'y', 1, 1))
        self.assertEqual(r'\myfrac{(2z+2)}{4}',  hw.bracket_fracstyle_print(4, 0, 2, 'z', 0, 2))
        self.assertEqual(r'\myfrac{(-2w-2)}{5}', hw.bracket_fracstyle_print(5, 1, 2, 'w', 1, 2))


class TestIntPolyn(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '(x+2)+(x+3)',
            hw.int_polyn('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '2(3y+4)+5(6y+7)',
            hw.int_polyn('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '-(-z-2)-(-z-3)',
            hw.int_polyn('z', [1, 1, 1, 1, 1, 1], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '-2(-3w-4)-5(-6w-7)',
            hw.int_polyn('w', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '$-2(-3w-4)-5(-6w-7)$',
            hw.int_polyn('w', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7], True)
        )


class TestFracPolynI(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '$(x+2)+(x+3)$',
            hw.frac_polynI('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '$\myfrac{1}{2}(3y+4)+\myfrac{1}{5}(6y+7)$',
            hw.frac_polynI('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '$-(-z-2)-(-z-3)$',
            hw.frac_polynI('z', [1, 1, 1, 1, 1, 1], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '$-\myfrac{1}{2}(-3w-4)-\myfrac{1}{5}(-6w-7)$',
            hw.frac_polynI('w', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7])
        )


class TestFracPolynII(unittest.TestCase):
    def test(self):
        self.assertEqual(
            r'\myfrac{(3x+4)}{2}+\myfrac{(6x+7)}{5}',
            hw.frac_polynII('x', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            r'-\myfrac{(-3y-4)}{2}-\myfrac{(-6y-7)}{5}',
            hw.frac_polynII('y', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            r'$-\myfrac{(-3y-4)}{2}-\myfrac{(-6y-7)}{5}$',
            hw.frac_polynII('y', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7], True)
        )


class TestTenkaiA(unittest.TestCase):
    def test(self):
        self.assertEqual(
            'x+2+x+3',
            hw.tenkaiA('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '6y+8+30y+35',
            hw.tenkaiA('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '-z-2-z-3',
            hw.tenkaiA('z', [1, 0, 0, 1, 0, 0], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '-6w-8-30w-35',
            hw.tenkaiA('w', [1, 0, 0, 1, 0, 0], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '$-6w-8-30w-35$',
            hw.tenkaiA('w', [1, 0, 0, 1, 0, 0], [2, 3, 4, 5, 6, 7], True)
        )


if __name__ == '__main__':
    unittest.main()