#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'kimura'

from fractions import gcd
from datetime import datetime
import random


# TeX 出力 ------------------------------------------------------
def mathmode(expression):
    return "$"+expression+"$"


def myfrac(numerator, denominator):
    return r"\myfrac{"+str(numerator)+"}{"+str(denominator)+"}"


def mitemxx(left, right):
    return r"\mitemxx{"+left+"}{"+right+"}"


def questionii(first_column_tex, second_column_tex):
    tex = r"\questionII{1cm}"

    tex += "\n".join([
        "{%",
        first_column_tex,
        "%--- end of first column -----------------------------------------",
        "}"
    ])

    if second_column_tex:
        tex += "\n".join([
            "{%",
            second_column_tex,
            "%--- end of second column -----------------------------------------",
            "}"
        ])
    else:
        tex += "\n".join([
            "{%",
            "}"
        ])

    return tex


def qiians(expressions, height_cm, frac=False):
    speq  = r" \speq "
    fracv = r" \fracv "

    lines = [mathmode(expressions[0])+r"\\"]
    lines += map(
        (lambda expr:
            "& "+mathmode(speq + expr)+(fracv if frac else "")+r"\\"),
        expressions[1:]
    )
    return r"\qIIans{" + "\n".join(lines) + "\n}{"+str(height_cm)+"cm}"


def sign(num):
    if num > 0:
        return "+"
    elif num < 0:
        return "-"
    else:  # num == 0
        return ""


# 約分は行わない。
def coefficient(numerator, denominator=1):
    sgn = sign(numerator * denominator)
    abs_numerator   = abs(numerator)
    abs_denominator = abs(denominator)

    if abs_denominator > 1:
        return sgn + myfrac(abs_numerator, abs_denominator)
    elif abs_numerator > 1:
        return sgn + str(abs_numerator)
    else:
        return sgn


def constant(num):
    if num == 0:
        return ""
    else:
        return sign(num) + str(abs(num))


def trim_first_plus(str):
    if len(str) == 0:
        return ""

    if str[0] == "+":
        return str[1:]
    else:
        return str


# +ax+b
def expr(a, symbol, b):
    expression = ""

    if a != 0:
        expression += coefficient(a) + symbol
    if b != 0:
        expression += constant(b)

    return expression or "0"


# (ax+b)
def bracket_expr(a, symbol, b):
    return "("+trim_first_plus(expr(a, symbol, b))+")"


# a(bx+c)+d(ex+f)
def int_polyn(nums, symbol):
    expression  = coefficient(nums[0]) + bracket_expr(nums[1], symbol, nums[2])
    expression += coefficient(nums[3]) + bracket_expr(nums[4], symbol, nums[5])
    return trim_first_plus(expression)


# \myfrac{1}{a}(bx+c)+\myfrac{1}{d}(ex+f)
def frac_polyn(nums, symbol):
    expression  = coefficient(1, nums[0]) + bracket_expr(nums[1], symbol, nums[2])
    expression += coefficient(1, nums[3]) + bracket_expr(nums[4], symbol, nums[5])
    return trim_first_plus(expression)


# ax+b+cx+d
def tenkaiA(nums, symbol):
    a = nums[0] * nums[1]
    b = nums[0] * nums[2]
    c = nums[3] * nums[4]
    d = nums[3] * nums[5]

    expression  = expr(a, symbol, b)
    expression += expr(c, symbol, d)
    return trim_first_plus(expression)


# ax+b
def tenkaiB(nums, symbol):
    a = nums[0] * nums[1] + nums[3] * nums[4]
    b = nums[0] * nums[2] + nums[3] * nums[5]
    return trim_first_plus(expr(a, symbol, b))


# ax+b
# 約分実行
def tenkaiB_reduct(nums, symbol, g):
    a = (nums[0] * nums[1] + nums[3] * nums[4]) / g
    b = (nums[0] * nums[2] + nums[3] * nums[5]) / g
    return trim_first_plus(expr(a, symbol, b))


# 答えが約分可能かどうか。係数と分母の最大公約数
def common_factor(nums, denominator):
    coeff = nums[0] * nums[1] + nums[3] * nums[4]
    const = nums[0] * nums[2] + nums[3] * nums[5]
    return gcd(gcd(coeff, const), denominator)


# 排除すべきデータならFalse. 同じ問題と、左右入れ替えただけのものと、カッコの前が+1なものだけ排除
def isAdmissible(nums, nums_list):
    length = len(nums)
    exchange_nums = nums[length/2:length] + nums[0:length/2]

    a = nums not in nums_list
    b = exchange_nums not in nums_list
    c = not (nums[0] == 1)
    d = not (nums[3] == 1)
    e = not (abs(nums[0]) == abs(nums[3]))  # 分数の場合のみ排除したいが今回は排除。分母が同じものは排除。

    return a and b and c and d and e


# 乱数の割合調節
def rand_coeff(probs):
    s = sum(probs)
    int = random.randint(1, s)
    interval = 0
    for i in xrange(len(probs)):
        if interval <= int and int <= interval + probs[i]:
            return i
        interval += probs[i]


def create_problems_tex(nums_list, symbols):
    tex_lines = [r"\begin{multienumerate}\restmultienumparameters"]
    at_int_mode = True

    for i in xrange(0, len(nums_list), 2):
        polyn = int_polyn if at_int_mode else frac_polyn

        left_problem  = mathmode(polyn(nums_list[i], symbols[i]))
        right_problem = mathmode(polyn(nums_list[i+1], symbols[i+1]))
        tex_lines.append( mitemxx(left_problem, right_problem) )

        at_int_mode = not at_int_mode  # 2題ごとに整数モードと分数モードの切り替え

    tex_lines.append(r"\end{multienumerate}")
    return "\n".join(tex_lines)


# TODO: max_col
def create_answers_tex(nums_list, symbols):
    at_frac_mode = True
    at_first_column = True
    col_height = 0.0
    col_height_max = 17.0
    vskip = 0.45

    tex_lines = ["%"]
    first_column_tex_lines = []
    second_column_tex_lines = []
    current_column_tex_lines = first_column_tex_lines

    for i in xrange(len(nums_list)):
        symbol = symbols[i]
        nums = nums_list[i]

        if i % 2 == 0:
            at_frac_mode = not at_frac_mode  # 2題ごとに分数モードと整数モードの切り替え

        if at_frac_mode:
            expressions = [frac_polyn(nums, symbol)]

            g_int = gcd(nums[0], nums[3])
            denominator = abs(nums[0] * nums[3] / g_int)
            nums[0] = denominator / nums[0]
            nums[3] = denominator / nums[3]

            expressions += [
                myfrac(int_polyn(nums, symbol), denominator),
                myfrac(tenkaiA(nums, symbol), denominator),
                myfrac(tenkaiB(nums, symbol), denominator)
            ]

            g = common_factor(nums, denominator)
            if g > 1:  # 約分
                if denominator == g:
                    expressions.append( tenkaiB_reduct(nums, symbol, g) )
                else:
                    expressions.append( myfrac(tenkaiB_reduct(nums, symbol, g), denominator / g) )
                problem_height = 4
            else:
                problem_height = 3.2
        else:
            expressions = [
                int_polyn(nums, symbol),
                tenkaiA(nums, symbol),
                tenkaiB(nums, symbol),
            ]
            problem_height = 1.2

        current_column_tex_lines.append(qiians(expressions, problem_height, at_frac_mode))
        col_height += problem_height + vskip

        # 列の終わり
        if col_height >= col_height_max:
            if at_first_column:
                current_column_tex_lines = second_column_tex_lines
                at_first_column = False
            else:
                tex_lines.append(questionii(
                    "\n".join(first_column_tex_lines),
                    "\n".join(second_column_tex_lines)
                ))
                tex_lines.append(r"%\newpage")

                first_column_tex_lines = []
                second_column_tex_lines = []
                current_column_tex_lines = first_column_tex_lines
                at_first_column = True

            col_height = 0.0

    if len(first_column_tex_lines) >= 1:
        tex_lines.append(questionii(
            "\n".join(first_column_tex_lines),
            "\n".join(second_column_tex_lines)
        ))

    return "\n".join(tex_lines)


def create_tex_file(name, tex):
    f = open(name + ".tex", "w")
    f.write(tex)
    f.close()


if __name__ == "__main__":
    # 係数の出やすさ設定
    # 1～9が、等確率で、大体10～19より30倍くらい出やすいように設定。
    coeff_probs = [0] + ([30] * 9) + ([1] * 10)

    symbol_list = ["x", "y", "a"]
    symbol_probs = [50, 1, 10]

    # データの生成 -------------------------------------------------------------------
    num_of_problems = 300  # とりあえず300題（2の倍数）
    nums_list = []
    seed = 20140627
    random.seed(seed)

    while len(nums_list) < num_of_problems:
        nums = [
            random.choice([-1, 1]) * rand_coeff(coeff_probs) for i in range(6)
        ]
        if isAdmissible(nums, nums_list):
            nums_list.append(nums)

    # 問題ごとの使用文字番号を格納。解答の文字を揃えるため。
    symbols = [symbol_list[rand_coeff(symbol_probs)] for i in xrange(num_of_problems)]

    # texの1行目に、seed情報をコメント
    header = "% seed: " + str(seed) + "\n"

    # 問題の生成 ---------------------------------------------------------------------
    problems_tex = header + create_problems_tex(nums_list, symbols)
    create_tex_file(datetime.now().strftime("M1a_HW_polyn_%Y%m%d_%H%M_%S"), problems_tex)
    print "problems are generated..."

    # 回答の生成 ---------------------------------------------------------------------
    answers_tex = header + create_answers_tex(nums_list, symbols)
    create_tex_file(datetime.now().strftime("M1a_HW_polynAns_%Y%m%d_%H%M_%S"), answers_tex)
    print "End."