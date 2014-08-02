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


class questionii(unittest.TestCase):
    def test_one_column(self):
        expected = '\n'.join([
            r'\questionII{1cm}{%',
            r'first',
            r'%--- end of first column -----------------------------------------',
            r'}{%',
            r'}'
        ])
        self.assertEqual(expected, hw.questionii('first', ''))

    def test_two_column(self):
        expected = '\n'.join([
            r'\questionII{1cm}{%',
            r'first',
            r'%--- end of first column -----------------------------------------',
            r'}{%',
            r'second',
            r'%--- end of second column -----------------------------------------',
            r'}',
        ])
        self.assertEqual(expected, hw.questionii('first', 'second'))


class TestQiians(unittest.TestCase):
    def test_int(self):
        expected = '\n'.join([
            r'\qIIans{$2(3x+4)+5(6x+7)$\\',
            r'& $ \speq 6x+8+30x+35$\\',
            r'& $ \speq 36x+43$\\',
            r'}{1.2cm}',
        ])
        self.assertEqual(expected, hw.qiians(['2(3x+4)+5(6x+7)', '6x+8+30x+35', '36x+43'], 1.2))
        self.assertEqual(expected, hw.qiians(['2(3x+4)+5(6x+7)', '6x+8+30x+35', '36x+43'], 1.2, False))

    def test_frac(self):
        expected = '\n'.join([
            r'\qIIans{$2(3x+4)+5(6x+7)$\\',
            r'& $ \speq 6x+8+30x+35$ \fracv \\',
            r'& $ \speq 36x+43$ \fracv \\',
            r'}{1.2cm}',
        ])
        self.assertEqual(expected, hw.qiians(['2(3x+4)+5(6x+7)', '6x+8+30x+35', '36x+43'], 1.2, True))


class TestSign(unittest.TestCase):
    def test(self):
        self.assertEqual('+', hw.sign(1))
        self.assertEqual('',  hw.sign(0))
        self.assertEqual('-', hw.sign(-1))


class TestCoefficient(unittest.TestCase):
    def test(self):
        self.assertEqual('+',  hw.coefficient(1))
        self.assertEqual('+',  hw.coefficient( 1,  1))
        self.assertEqual('+',  hw.coefficient(-1, -1))
        self.assertEqual('-',  hw.coefficient(-1))
        self.assertEqual('-',  hw.coefficient(-1,  1))
        self.assertEqual('-',  hw.coefficient( 1, -1))
        self.assertEqual('+2', hw.coefficient(2))
        self.assertEqual('+2', hw.coefficient( 2,  1))
        self.assertEqual('+2', hw.coefficient(-2, -1))
        self.assertEqual('-2', hw.coefficient(-2))
        self.assertEqual('-2', hw.coefficient( 2, -1))
        self.assertEqual('-2', hw.coefficient(-2,  1))
        self.assertEqual(r'+\myfrac{1}{2}', hw.coefficient( 1,  2))
        self.assertEqual(r'+\myfrac{1}{2}', hw.coefficient(-1, -2))
        self.assertEqual(r'-\myfrac{1}{2}', hw.coefficient(-1,  2))
        self.assertEqual(r'-\myfrac{1}{2}', hw.coefficient( 1, -2))


class TestConstant(unittest.TestCase):
    def test(self):
        self.assertEqual('', hw.constant(0))
        self.assertEqual('+1', hw.constant(1))
        self.assertEqual('+2', hw.constant(2))
        self.assertEqual('-1', hw.constant(-1))
        self.assertEqual('-2', hw.constant(-2))


class TestTrimFirstPlus(unittest.TestCase):
    def test(self):
        self.assertEqual('', hw.trim_first_plus(''))
        self.assertEqual('ax+b', hw.trim_first_plus('ax+b'))
        self.assertEqual('ax+b', hw.trim_first_plus('+ax+b'))
        self.assertEqual('-ax+b', hw.trim_first_plus('-ax+b'))


class TestBracketPrint(unittest.TestCase):
    def test(self):
        self.assertEqual('(x+1)',   hw.bracket_print( 1, 'x',  1))
        self.assertEqual('(-y-1)',  hw.bracket_print(-1, 'y', -1))
        self.assertEqual('(2z+2)',  hw.bracket_print( 2, 'z',  2))
        self.assertEqual('(-2w-2)', hw.bracket_print(-2, 'w', -2))


class TestIntPolyn(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '(x+2)+(x+3)',
            hw.int_polyn([1, 1, 2, 1, 1, 3], 'x')
        )
        self.assertEqual(
            '2(3y+4)+5(6y+7)',
            hw.int_polyn([2, 3, 4, 5, 6, 7], 'y')
        )
        self.assertEqual(
            '-(-z-2)-(-z-3)',
            hw.int_polyn([-1, -1, -2, -1, -1, -3], 'z')
        )
        self.assertEqual(
            '-2(-3w-4)-5(-6w-7)',
            hw.int_polyn([-2, -3, -4, -5, -6, -7], 'w')
        )


class TestFracPolyn(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '(x+2)+(x+3)',
            hw.frac_polyn([1, 1, 2, 1, 1, 3], 'x')
        )
        self.assertEqual(
            '\myfrac{1}{2}(3y+4)+\myfrac{1}{5}(6y+7)',
            hw.frac_polyn([2, 3, 4, 5, 6, 7], 'y')
        )
        self.assertEqual(
            '-(-z-2)-(-z-3)',
            hw.frac_polyn([-1, -1, -2, -1, -1, -3], 'z')
        )
        self.assertEqual(
            '-\myfrac{1}{2}(-3w-4)-\myfrac{1}{5}(-6w-7)',
            hw.frac_polyn([-2, -3, -4, -5, -6, -7], 'w')
        )


class TestTenkaiA(unittest.TestCase):
    def test(self):
        self.assertEqual(
            'x+2+x+3',
            hw.tenkaiA([1, 1, 2, 1, 1, 3], 'x')
        )
        self.assertEqual(
            '6y+8+30y+35',
            hw.tenkaiA([2, 3, 4, 5, 6, 7], 'y')
        )
        self.assertEqual(
            '-z-2-z-3',
            hw.tenkaiA([-1, 1, 2, -1, 1, 3], 'z')
        )
        self.assertEqual(
            '-6w-8-30w-35',
            hw.tenkaiA([-2, 3, 4, -5, 6, 7], 'w')
        )


class TestTenkaiB(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '2x+5',  # (x+2)+(x+3)
            hw.tenkaiB([1, 1, 2, 1, 1, 3], 'x')
        )
        self.assertEqual(
            '36y+43',  # 2(3y+4)+5(6y+7)
            hw.tenkaiB([2, 3, 4, 5, 6, 7], 'y')
        )
        self.assertEqual(
            '-2z+5',  # -(z-2)-(z-3)
            hw.tenkaiB([-1, 1, -2, -1, 1, -3], 'z')
        )
        self.assertEqual(
            '-36w+43',  # -2(3w-4)-5(6w-7)
            hw.tenkaiB([-2, 3, -4, -5, 6, -7], 'w')
        )
        self.assertEqual(
            '-2a',  # -(a+2)-(a-2)
            hw.tenkaiB([-1, 1, 2, -1, 1, -2], 'a')
        )
        self.assertEqual(
            '-4',  # -(b+2)-(-b+2)
            hw.tenkaiB([-1, 1, 2, -1, -1, 2], 'b')
        )
        self.assertEqual(
            '0',  # -(c+2)-(-c-2)
            hw.tenkaiB([-1, 1, 2, -1, -1, -2], 'c')
        )


class TestCommonFactor(unittest.TestCase):
    def test(self):
        # ((x+2)+(x+3)) / 2
        self.assertEqual(1, hw.common_factor([1, 1, 2, 1, 1, 3], 2))
        # ((x+2)+(11x+28)) / 60
        self.assertEqual(6, hw.common_factor([1, 1, 2, 1, 11, 28], 60))
        # ((x+2)+(x-2)) / 2
        self.assertEqual(2, hw.common_factor([1, 1, 2, 1, 1, -2], 2))
        # ((x+2)-(x-2)) / 4
        self.assertEqual(4, hw.common_factor([1, 1, 2, 1, -1, 2], 4))


class TestTenkaiBreduct(unittest.TestCase):
    def test(self):
        self.assertEqual(
            '2x+5',  # ((x+2)+(x+3)) / 1
            hw.tenkaiB_reduct([1, 1, 2, 1, 1, 3], 'x', 1)
        )
        self.assertEqual(
            '2x+5',  # ((x+2)+(11x+28)) / 6
            hw.tenkaiB_reduct([1, 1, 2, 1, 11, 28], 'x', 6)
        )
        self.assertEqual(
            'x',  # ((x+2)+(x-2)) / 2
            hw.tenkaiB_reduct([1, 1, 2, 1, 1, -2], 'x', 2)
        )
        self.assertEqual(
            '1',  # ((x+2)-(x-2)) / 4
            hw.tenkaiB_reduct([1, 1, 2, 1, -1, 2], 'x', 4)
        )
        self.assertEqual(
            '0',  # ((x+2)-(x+2)) / 2
            hw.tenkaiB_reduct([1, 1, 2, -1, 1, 2], 'x', 2)
        )


class TestIsAdmissible(unittest.TestCase):
    def test(self):
        self.assertTrue(hw.isAdmissible([2, 3, 4, 5, 6, 7], []))
        self.assertFalse(hw.isAdmissible([2, 3, 4, 5, 6, 7], [[2, 3, 4, 5, 6, 7]]))
        self.assertFalse(hw.isAdmissible([2, 3, 4, 5, 6, 7], [[5, 6, 7, 2, 3, 4]]))
        self.assertFalse(hw.isAdmissible([1, 3, 4, 5, 6, 7], []))
        self.assertFalse(hw.isAdmissible([2, 3, 4, 1, 6, 7], []))
        self.assertFalse(hw.isAdmissible([2, 3, 4, 2, 6, 7], []))
        self.assertFalse(hw.isAdmissible([-2, 3, 4,  2, 6, 7], []))
        self.assertFalse(hw.isAdmissible([ 2, 3, 4, -2, 6, 7], []))


class TestCreateProblemsTex(unittest.TestCase):
    def test(self):
        data_list = [
            [2, 3, 4, 5, 6, 7],
            [-1, -2, -3, -1, -4, -5],
            [2, 3, 4, 5, 6, 7],
            [-1, -2, -3, -1, -4, -5]
        ]
        symbols = ['x', 'y', 'x', 'y']
        expected = '\n'.join([
            r'\begin{multienumerate}\restmultienumparameters',
            r'\mitemxx{$2(3x+4)+5(6x+7)$}{$-(-2y-3)-(-4y-5)$}',
            r'\mitemxx{$\myfrac{1}{2}(3x+4)+\myfrac{1}{5}(6x+7)$}{$-(-2y-3)-(-4y-5)$}',
            r'\end{multienumerate}'
        ])
        self.assertEqual(expected, hw.create_problems_tex(data_list, symbols))


class TestCreateAnswersTex(unittest.TestCase):
    def test(self):
        data_list = [
            [2, 3, 4, 5, 6, 7],
            [-1, 2, -3, 1, -4, 5],
            [-2, 3, -4, 5, -6, 7],
            [7, -6, 7, 2, 2, -4]
        ]
        symbols = ['x', 'y', 'x', 'y']
        expected = '\n'.join([
            r'%',
            r'\questionII{1cm}{%',
            r'\qIIans{$2(3x+4)+5(6x+7)$\\',
            r'& $ \speq 6x+8+30x+35$\\',
            r'& $ \speq 36x+43$\\',
            r'}{1.2cm}',
            r'\qIIans{$-(2y-3)+(-4y+5)$\\',
            r'& $ \speq -2y+3-4y+5$\\',
            r'& $ \speq -6y+8$\\',
            r'}{1.2cm}',
            r'\qIIans{$-\myfrac{1}{2}(3x-4)+\myfrac{1}{5}(-6x+7)$\\',
            r'& $ \speq \myfrac{-5(3x-4)+2(-6x+7)}{10}$ \fracv \\',
            r'& $ \speq \myfrac{-15x+20-12x+14}{10}$ \fracv \\',
            r'& $ \speq \myfrac{-27x+34}{10}$ \fracv \\',
            r'}{3.2cm}',
            r'\qIIans{$\myfrac{1}{7}(-6y+7)+\myfrac{1}{2}(2y-4)$\\',
            r'& $ \speq \myfrac{2(-6y+7)+7(2y-4)}{14}$ \fracv \\',
            r'& $ \speq \myfrac{-12y+14+14y-28}{14}$ \fracv \\',
            r'& $ \speq \myfrac{2y-14}{14}$ \fracv \\',
            r'& $ \speq \myfrac{y-7}{7}$ \fracv \\',
            r'}{4cm}',
            r'%--- end of first column -----------------------------------------',
            r'}{%',
            r'}'
        ])
        self.assertEqual(expected, hw.create_answers_tex(data_list, symbols))


if __name__ == '__main__':
    unittest.main()