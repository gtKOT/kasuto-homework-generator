﻿#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'kimura'

from fractions import gcd
from datetime import datetime
import random
import copy


# TeX 出力 ------------------------------------------------------
def to_mathmode(expression):
    return "$" + expression + "$"


def to_myfrac(numerator, denominator):
    return r"\myfrac{" + str(numerator) + "}{" + str(denominator) + "}"


def sgn_print(boolnum, avoid_plus=False):
    if boolnum == 1:
        return "-"
    elif (boolnum == 0) and (not avoid_plus):
        return "+"
    else:
        return ""


# 約分は行わない
def coeff(numerator, denominator=1):
    if denominator > 1:
        return to_myfrac(numerator, denominator)
    elif numerator > 1:
        return str(numerator)
    else:
        return ""


# (ax+b)
def bracket_print(sgn_a, a, moji, sgn_b, b):
    output = sgn_print(sgn_a, avoid_plus=True) + coeff(a) + moji
    output += sgn_print(sgn_b) + str(b)
    return "(" + output + ")"


def int_polyn(moji, sgn, intdata, at_math_mode=False):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(intdata[0])
    output += bracket_print(sgn[1], intdata[1], moji, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(intdata[3])
    output += bracket_print(sgn[4], intdata[4], moji, sgn[5], intdata[5])

    if at_math_mode:
        output = to_mathmode(output)
    return output


def frac_polyn(moji, sgn, intdata):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(1, intdata[0])
    output += bracket_print(sgn[1], intdata[1], moji, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(1, intdata[3])
    output += bracket_print(sgn[4], intdata[4], moji, sgn[5], intdata[5])
    return to_mathmode(output)


# ax+b+cx+d
def tenkaiA(moji, sgn, intdata, at_math_mode=False):
    sgn_a = (sgn[0] + sgn[1]) % 2
    a = intdata[0] * intdata[1]
    sgn_b = (sgn[0] + sgn[2]) % 2
    b = intdata[0] * intdata[2]
    sgn_c = (sgn[3] + sgn[4]) % 2
    c = intdata[3] * intdata[4]
    sgn_d = (sgn[3] + sgn[5]) % 2
    d = intdata[3] * intdata[5]

    output = sgn_print(sgn_a, avoid_plus=True) + coeff(a) + moji
    output += sgn_print(sgn_b) + str(b)
    output += sgn_print(sgn_c) + coeff(c) + moji
    output += sgn_print(sgn_d) + str(d)

    if at_math_mode:
        output = to_mathmode(output)
    return output


# ax+b
def tenkaiB(moji, sgn, intdata, at_math_mode=False):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid_plus = False

    if a > 0:
        output += coeff(a) + moji
    elif a < 0:
        output += "-" + coeff(a * (-1)) + moji
    else:
        avoid_plus = True

    if b > 0:
        output += sgn_print(0, avoid_plus) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    if at_math_mode:
        output = to_mathmode(output)
    return output


# 答えが約分可能かどうか。係数と分母の最大公約数
def common_factor(sgn, intdata, denominator):
    coeff = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    return gcd(gcd(abs(coeff), abs(constt)), denominator)


# ax+b
# 約分実行
def tenkaiB_reduct(moji, sgn, intdata, g, at_math_mode=False):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid_plus = False
    a = a / g
    b = b / g

    if a > 0:
        output += coeff(a) + moji
    elif a < 0:
        output += "-" + coeff(a * (-1)) + moji
    else:
        avoid_plus = True

    if b > 0:
        output += sgn_print(0, avoid_plus) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    if at_math_mode:
        output = to_mathmode(output)
    return output


# 排除すべきデータならFalse. 同じ問題と、左右入れ替えただけのものと、カッコの前が+1なものだけ排除
def isAdmissible(tmpdata, data_list):
    lL = len(tmpdata[0])
    lR = len(tmpdata[1])
    exchange_tmpdata = [tmpdata[0][lL / 2:lL] + tmpdata[0][0:lL / 2], tmpdata[1][lR / 2:lR] + tmpdata[1][0:lR / 2]]

    a = tmpdata not in data_list
    b = exchange_tmpdata not in data_list
    c = not (tmpdata[0][0] == 0 and tmpdata[1][0] == 1)
    d = not (tmpdata[0][lL / 2] == 0 and tmpdata[1][lR / 2] == 1)
    e = not (tmpdata[1][0] == tmpdata[1][3])  # 分数の場合のみ。分母が同じものは排除。

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


def create_problems_tex(data_list, mojis):
    tex = r"\begin{multienumerate}\restmultienumparameters"

    for i in xrange(len(data_list)):
        moji = mojis[i]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % 2 == 0:
            tex += "\n" + r"\mitemxx"
        tex += r"{" + frac_polyn(moji, sgn, intdata) + r"}"

    tex += "\n" + r"\end{multienumerate}"
    return tex


def create_answers_tex(data_list, mojis):
    colQ = 5
    tex = r"%"

    for i in xrange(len(data_list)):
        moji = mojis[i]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % (2 * colQ) == 0:
            tex += "\n" + r"\questionII{1cm}{%"
            page_open = True
            col_open = True
        tex += "\n" + r"\qIIans{"
        tex += frac_polyn(moji, sgn, intdata) + r"\\"

        g_int = gcd(intdata[0], intdata[3])
        denominator = intdata[0] * intdata[3] / g_int
        intdata[0], intdata[3] = intdata[3] / g_int, intdata[0] / g_int
        tex += "\n" + r"& $ \speq " + to_myfrac(int_polyn(moji, sgn, intdata), denominator) + r" $ \fracv \\"
        tex += "\n" + r"& $ \speq " + to_myfrac(tenkaiA(moji, sgn, intdata), denominator) + r" $ \fracv \\"
        tex += "\n" + r"& $ \speq " + to_myfrac(tenkaiB(moji, sgn, intdata), denominator) + r" $ \fracv \\"
        g = common_factor(sgn, intdata, denominator)
        if g > 1:
            if denominator == g:
                tex += "\n" + r"& $ \speq " + tenkaiB_reduct(moji, sgn, intdata, g) + r" $ \fracv \\"
            else:
                tex += "\n" + r"& $ \speq " + to_myfrac(tenkaiB_reduct(moji, sgn, intdata, g), denominator / g) + r" $ \fracv \\"
            tex += "\n" + r"}{4cm}"
        else:
            tex += "\n" + r"}{3.2cm}"
        if (i + 1) % colQ == 0:
            tex += "\n" + r"}{%"
            col_open = False
        if (i + 1) % (2 * colQ) == 0:
            tex += "\n" + r"}" + "\n" + r"%\newpage"
            page_open = False

    if col_open:
        tex += "\n" + r"}{%"
    if page_open:
        tex += "\n" + r"}"

    return tex


def create_tex_file(name, tex):
    f = open(name + ".tex", "w")
    f.write(tex)
    f.close()


if __name__ == "__main__":
    # 係数の出やすさ設定
    probs = [0] * 20
    # 1～9が、等確率で、大体10～19より30倍くらい出やすいように設定。
    for i in xrange(1, 10):
        probs[i] = 30
    for i in xrange(10, 20):
        probs[i] = 1

    moji_list = ["x", "y", "a"]
    moji_prob_list = [50, 1, 10]

    # データの生成 -------------------------------------------------------------------
    sgn = [0] * 6
    intdata = [0] * 6
    data_list = []
    seed = 20140627
    random.seed(seed)

    num_of_problems = 200  # とりあえず200題（2の倍数）
    n = 0  # = len(data_list)
    while n < num_of_problems:
        for m in xrange(6):
            sgn[m] = random.randint(0, 1)
            intdata[m] = rand_coeff(probs)
        tmpdata = [copy.copy(sgn), copy.copy(intdata)]
        if isAdmissible(tmpdata, data_list):
            data_list += [copy.deepcopy(tmpdata)]
            n += 1

    # 問題ごとの使用文字の確定
    mojis = [moji_list[rand_coeff(moji_prob_list)] for i in xrange(num_of_problems)]

    # texの1行目に、seed情報をコメント
    header = "% seed: " + str(seed) + "\n"

    # 問題の生成 ---------------------------------------------------------------------
    problems_tex = header + create_problems_tex(data_list, mojis)
    create_tex_file(datetime.now().strftime("M1a_HW_frac_%Y%m%d_%H%M_%S"), problems_tex)
    print "problems are generated..."

    # 回答の生成 ---------------------------------------------------------------------
    answers_tex = header + create_answers_tex(data_list, mojis)
    create_tex_file(datetime.now().strftime("M1a_HW_fracAns_%Y%m%d_%H%M_%S"), answers_tex)
    print "End."