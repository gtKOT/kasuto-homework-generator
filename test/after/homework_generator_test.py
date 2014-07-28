#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../../src/after')

import unittest
import homework_generator as hw


class TestMathmode(unittest.TestCase):
    def test(self):
        self.assertEqual('$1$', hw.mathmode('1'))


class TestMyfrac(unittest.TestCase):
    def test(self):
        self.assertEqual(r'\myfrac{1}{2}',   hw.myfrac(1, 2))
        self.assertEqual(r'\myfrac{x+1}{2}', hw.myfrac('x+1', 2))
        self.assertEqual(r'\myfrac{1}{y-2}', hw.myfrac(1, 'y-2'))


class TestMitemxx(unittest.TestCase):
    def test(self):
        self.assertEqual(r'\mitemxx{(x+1)}{(y-2)}', hw.mitemxx('(x+1)', '(y-2)'))


class TestSgnPrint(unittest.TestCase):
    def test(self):
        self.assertEqual('+', hw.sgn_print(0))
        self.assertEqual('+', hw.sgn_print(0, False))
        self.assertEqual('',  hw.sgn_print(0, True))
        self.assertEqual('-', hw.sgn_print(1))
        self.assertEqual('-', hw.sgn_print(1, False))
        self.assertEqual('-', hw.sgn_print(1, True))


class TestCoeff(unittest.TestCase):
    def test(self):
        self.assertEqual('',  hw.coeff(1))
        self.assertEqual('',  hw.coeff(1, 1))
        self.assertEqual('2', hw.coeff(2))
        self.assertEqual('2', hw.coeff(2, 1))
        self.assertEqual(r'\myfrac{1}{2}', hw.coeff(1, 2))


class TestBracketPrint(unittest.TestCase):
    def test(self):
        self.assertEqual('(x+1)',   hw.bracket_print(0, 1, 'x', 0, 1))
        self.assertEqual('(-y-1)',  hw.bracket_print(1, 1, 'y', 1, 1))
        self.assertEqual('(2z+2)',  hw.bracket_print(0, 2, 'z', 0, 2))
        self.assertEqual('(-2w-2)', hw.bracket_print(1, 2, 'w', 1, 2))


class TestIntPolyn(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '(x+2)+(x+3)',
            hw.int_polyn('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '2(3y+4)+5(6y+7)',
            hw.int_polyn('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '-(-z-2)-(-z-3)',
            hw.int_polyn('z', [1, 1, 1, 1, 1, 1], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '-2(-3w-4)-5(-6w-7)',
            hw.int_polyn('w', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7])
        )


class TestFracPolyn(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '(x+2)+(x+3)',
            hw.frac_polyn('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '\myfrac{1}{2}(3y+4)+\myfrac{1}{5}(6y+7)',
            hw.frac_polyn('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '-(-z-2)-(-z-3)',
            hw.frac_polyn('z', [1, 1, 1, 1, 1, 1], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '-\myfrac{1}{2}(-3w-4)-\myfrac{1}{5}(-6w-7)',
            hw.frac_polyn('w', [1, 1, 1, 1, 1, 1], [2, 3, 4, 5, 6, 7])
        )


class TestTenkaiA(unittest.TestCase):
    def test(self):
        self.assertEqual(
            'x+2+x+3',
            hw.tenkaiA('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '6y+8+30y+35',
            hw.tenkaiA('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '-z-2-z-3',
            hw.tenkaiA('z', [1, 0, 0, 1, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '-6w-8-30w-35',
            hw.tenkaiA('w', [1, 0, 0, 1, 0, 0], [2, 3, 4, 5, 6, 7])
        )


class TestTenkaiB(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '2x+5',  # (x+2)+(x+3)
            hw.tenkaiB('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '36y+43',  # 2(3y+4)+5(6y+7)
            hw.tenkaiB('y', [0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '-2z+5',  # -(z-2)-(z-3)
            hw.tenkaiB('z', [1, 0, 1, 1, 0, 1], [1, 1, 2, 1, 1, 3])
        )
        self.assertEqual(
            '-36w+43',  # -2(3w-4)-5(6w-7)
            hw.tenkaiB('w', [1, 0, 1, 1, 0, 1], [2, 3, 4, 5, 6, 7])
        )
        self.assertEqual(
            '-2a',  # -(a+2)-(a-2)
            hw.tenkaiB('a', [1, 0, 0, 1, 0, 1], [1, 1, 2, 1, 1, 2])
        )
        self.assertEqual(
            '-4',  # -(b+2)-(-b+2)
            hw.tenkaiB('b', [1, 0, 0, 1, 1, 0], [1, 1, 2, 1, 1, 2])
        )
        self.assertEqual(
            '0',  # -(c+2)-(-c-2)
            hw.tenkaiB('c', [1, 0, 0, 1, 1, 1], [1, 1, 2, 1, 1, 2])
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
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 3], 1)
        )
        self.assertEqual(
            '2x+5',  # ((x+2)+(11x+28)) / 6
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 11, 28], 6)
        )
        self.assertEqual(
            'x',  # ((x+2)+(x-2)) / 2
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 0, 1], [1, 1, 2, 1, 1, 2], 2)
        )
        self.assertEqual(
            '1',  # ((x+2)-(x-2)) / 4
            hw.tenkaiB_reduct('x', [0, 0, 0, 0, 1, 0], [1, 1, 2, 1, 1, 2], 4)
        )
        self.assertEqual(
            '0',  # ((x+2)-(x+2)) / 2
            hw.tenkaiB_reduct('x', [0, 0, 0, 1, 0, 0], [1, 1, 2, 1, 1, 2], 2)
        )


class TestIsAdmissible(unittest.TestCase):
    def test(self):
        all_plus = [0, 0, 0, 0, 0, 0]
        self.assertTrue(hw.isAdmissible([all_plus,  [2, 3, 4, 5, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([all_plus, [2, 3, 4, 5, 6, 7]], [[all_plus, [2, 3, 4, 5, 6, 7]]]))
        self.assertFalse(hw.isAdmissible([all_plus, [2, 3, 4, 5, 6, 7]], [[all_plus, [5, 6, 7, 2, 3, 4]]]))
        self.assertFalse(hw.isAdmissible([all_plus, [1, 3, 4, 5, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([all_plus, [2, 3, 4, 1, 6, 7]], []))
        self.assertFalse(hw.isAdmissible([all_plus, [2, 3, 4, 2, 6, 7]], []))


class TestCreateProblemsTex(unittest.TestCase):
    def test(self):
        data_list = [
            [[0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7]],
            [[1, 1, 1, 1, 1, 1], [1, 2, 3, 1, 4, 5]],
            [[0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7]],
            [[1, 1, 1, 1, 1, 1], [1, 2, 3, 1, 4, 5]]
        ]
        symbols = ['x', 'y', 'x', 'y']
        tex = '\n'.join([
            r'\begin{multienumerate}\restmultienumparameters',
            r'\mitemxx{$2(3x+4)+5(6x+7)$}{$-(-2y-3)-(-4y-5)$}',
            r'\mitemxx{$\myfrac{1}{2}(3x+4)+\myfrac{1}{5}(6x+7)$}{$-(-2y-3)-(-4y-5)$}',
            r'\end{multienumerate}'
        ])
        self.assertEqual(tex, hw.create_problems_tex(data_list, symbols))


class TestCreateAnswersTex(unittest.TestCase):
    def test(self):
        data_list = [
            [[0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7]],
            [[1, 1, 1, 1, 1, 1], [1, 2, 3, 1, 4, 5]],
            [[0, 0, 0, 0, 0, 0], [2, 3, 4, 5, 6, 7]],
            [[1, 1, 1, 1, 1, 1], [1, 2, 3, 1, 4, 5]]
        ]
        symbols = ['x', 'y', 'x', 'y']
        tex = '\n'.join([
            r'%',
            r'\questionII{1cm}{%',
            r'\qIIans{',
            r'$2(3x+4)+5(6x+7)$\\',
            r'& $ \speq 6x+8+30x+35$\\',
            r'& $ \speq 36x+43$\\',
            r'}{1.2cm}',
            r'\qIIans{',
            r'$-(-2y-3)-(-4y-5)$\\',
            r'& $ \speq 2y+3+4y+5$\\',
            r'& $ \speq 6y+8$\\',
            r'}{1.2cm}',
            r'\qIIans{',
            r'$\myfrac{1}{2}(3x+4)+\myfrac{1}{5}(6x+7)$\\',
            r'& $ \speq \myfrac{5(3x+4)+2(6x+7)}{10} $ \fracv \\',
            r'& $ \speq \myfrac{15x+20+12x+14}{10} $ \fracv \\',
            r'& $ \speq \myfrac{27x+34}{10} $ \fracv \\',
            r'}{3.2cm}',
            r'\qIIans{',
            r'$-(-2y-3)-(-4y-5)$\\',
            r'& $ \speq \myfrac{-(-2y-3)-(-4y-5)}{1} $ \fracv \\',
            r'& $ \speq \myfrac{2y+3+4y+5}{1} $ \fracv \\',
            r'& $ \speq \myfrac{6y+8}{1} $ \fracv \\',
            r'}{3.2cm}',
            r'}{%',
            r'}'
        ])
        self.assertEqual(tex, hw.create_answers_tex(data_list, symbols))


if __name__ == '__main__':
    unittest.main()