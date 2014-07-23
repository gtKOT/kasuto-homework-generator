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


# 現在、bracket_fracstyle_printは未使用
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


# 現在、frac_polynIIは未使用
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


class TestTenkaiB(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '2x+5',  # (x+2)+(x+3)
            hw.tenkaiB('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '36y+43',  # 2(3y+4)+5(6y+7)
            hw.tenkaiB('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '-2z+5',  # -(z-2)-(z-3)
            hw.tenkaiB('z', [1, 0, 1, 1, 0, 1], [1, 1, 2, 1, 1, 3], False)
        )
        self.assertEqual(
            '-36w+43',  # -2(3w-4)-5(6w-7)
            hw.tenkaiB('w', [1, 0, 1, 1, 0, 1], [2, 3, 4, 5, 6, 7], False)
        )
        self.assertEqual(
            '-2a',  # -(a+2)-(a-2)
            hw.tenkaiB('a', [1, 0, 0, 1, 0, 1], [1, 1, 2, 1, 1, 2], False)
        )
        self.assertEqual(
            '-4',  # -(b+2)-(-b+2)
            hw.tenkaiB('b', [1, 0, 0, 1, 1, 0], [1, 1, 2, 1, 1, 2], False)
        )
        self.assertEqual(
            '0',  # -(c+2)-(-c-2)
            hw.tenkaiB('c', [1, 0, 0, 1, 1, 1], [1, 1, 2, 1, 1, 2], False)
        )
        self.assertEqual(
            '$0$',
            hw.tenkaiB('c', [1, 0, 0, 1, 1, 1], [1, 1, 2, 1, 1, 2], True)
        )


class TestCommonFactor(unittest.TestCase):
    def test(self):
        # ((x+2)+(x+3)) / 2
        self.assertEqual(1, hw.common_factor([0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], 2))
        # ((x+2)+(11x+28)) / 60
        self.assertEqual(6, hw.common_factor([0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 11, 28], 60))
        # ((x+2)+(x-2)) / 2
        self.assertEqual(2, hw.common_factor([0, 0, 0, 0, 0, 1], [1, 1, 2, 1, 1, 2], 2))
        # ((x+2)-(x-2)) / 4
        self.assertEqual(4, hw.common_factor([0, 0, 0, 0, 1, 0], [1, 1, 2, 1, 1, 2], 4))


class TestTenkaiBreduct(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '2x+5',  # ((x+2)+(x+3)) / 1
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], False, 1)
        )
        self.assertEqual(
            '2x+5',  # ((x+2)+(11x+28)) / 6
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 11, 28], False, 6)
        )
        self.assertEqual(
            'x',  # ((x+2)+(x-2)) / 2
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 1], [1, 1, 2, 1, 1, 2], False, 2)
        )
        self.assertEqual(
            '1',  # ((x+2)-(x-2)) / 4
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 1, 0], [1, 1, 2, 1, 1, 2], False, 4)
        )
        self.assertEqual(
            '0',  # ((x+2)-(x+2)) / 2
            hw.tenkaiB_reduct('x', [0, 0, 0, 1, 0, 0], [1, 1, 2, 1, 1, 2], False, 2)
        )


class TestIsAdmissible(unittest.TestCase):
    def setUp(self):
        self.allPlus = [0, 0, 0, 0, 0, 0]

    def test(self):
        self.assertTrue(hw.isAdmissible([self.allPlus,  [2, 3, 4, 5, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([self.allPlus, [2, 3, 4, 5, 6, 7]], [[self.allPlus, [2, 3, 4, 5, 6, 7]]]))
        self.assertFalse(hw.isAdmissible([self.allPlus, [2, 3, 4, 5, 6, 7]], [[self.allPlus, [5, 6, 7, 2, 3, 4]]]))
        self.assertFalse(hw.isAdmissible([self.allPlus, [1, 3, 4, 5, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([self.allPlus, [2, 3, 4, 1, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([self.allPlus, [2, 3, 4, 2, 6, 7]], []))


if __name__ == '__main__':
    unittest.main()