﻿#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'kimura'

from fractions import gcd
import random
import copy
import datetime


# TeX 出力 ------------------------------------------------------
def to_mathmode(expression):
    return "$" + expression + "$"


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
        return r"\myfrac{" + str(numerator) + "}{" + str(denominator) + "}"
    elif numerator > 1:
        return str(numerator)
    else:
        return ""


# (ax+b)
def bracket_print(sgnL, a, moji, sgnR, b):
    output = sgn_print(sgnL, avoid_plus=True) + coeff(a) + moji
    output += sgn_print(sgnR) + str(b)
    return "(" + output + ")"


def int_polyn(moji, sgn, intdata, atMathMode=False):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(intdata[0])
    output += bracket_print(sgn[1], intdata[1], moji, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(intdata[3])
    output += bracket_print(sgn[4], intdata[4], moji, sgn[5], intdata[5])

    if atMathMode:
        output = to_mathmode(output)
    return output


def frac_polyn(moji, sgn, intdata):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(1, intdata[0])
    output += bracket_print(sgn[1], intdata[1], moji, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(1, intdata[3])
    output += bracket_print(sgn[4], intdata[4], moji, sgn[5], intdata[5])
    return to_mathmode(output)


def tenkaiA(moji, sgn, intdata, atMathMode=False):
    sgnA = (sgn[0] + sgn[1]) % 2
    coeffA = intdata[0] * intdata[1]
    sgnB = (sgn[0] + sgn[2]) % 2
    coeffB = intdata[0] * intdata[2]
    sgnC = (sgn[3] + sgn[4]) % 2
    coeffC = intdata[3] * intdata[4]
    sgnD = (sgn[3] + sgn[5]) % 2
    coeffD = intdata[3] * intdata[5]

    output = sgn_print(sgnA, avoid_plus=True) + coeff(coeffA) + moji
    output += sgn_print(sgnB) + str(coeffB)
    output += sgn_print(sgnC) + coeff(coeffC) + moji
    output += sgn_print(sgnD) + str(coeffD)

    if atMathMode:
        output = to_mathmode(output)
    return output


# ax+b
def tenkaiB(moji, sgn, intdata, atMathMode=False):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid = False

    if a > 0:
        output += coeff(a) + moji
    elif a < 0:
        output += "-" + coeff(a * (-1)) + moji
    else:
        avoid = True
    if b > 0:
        output += sgn_print(0, avoid) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    if atMathMode:
        output = to_mathmode(output)
    return output


# 答えが約分可能かどうか。係数と分母の最大公約数
def common_factor(sgn, intdata, bunbo):
    coeff = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    return gcd(gcd(abs(coeff), abs(constt)), bunbo)


# ax+b
# 約分実行
def tenkaiB_reduct(moji, sgn, intdata, g, atMathMode=False):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid = False
    a = a / g
    b = b / g

    if a > 0:
        output += coeff(a) + moji
    elif a < 0:
        output += "-" + coeff(a * (-1)) + moji
    else:
        avoid = True
    if b > 0:
        output += sgn_print(0, avoid) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    if atMathMode:
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
def rand_coeff(prob):
    s = sum(prob)
    int = random.randint(1, s)
    interval = 0
    for i in xrange(len(prob)):
        if interval <= int and int <= interval + prob[i]:
            return i
        interval += prob[i]


if __name__ == "__main__":
    # 係数の出やすさ設定
    prob = [0] * 20
    # 1～9が、等確率で、大体10～19より30倍くらい出やすいように設定。
    for i in xrange(1, 10):
        prob[i] = 30
    for i in xrange(10, 20):
        prob[i] = 1

    moji_list = ["x", "y", "a"]
    moji_prob = [50, 1, 10]

    # データの生成 -------------------------------------------------------------------
    sgn = [0] * 6
    intdata = [0] * 6
    data_list = []
    seed = 20140627
    random.seed(seed)

    Nmax = 200  # とりあえず200題（2の倍数）
    N = 0  # = len(data_list)
    while N < Nmax:
        for j in xrange(6):
            sgn[j] = random.randint(0, 1)
            intdata[j] = rand_coeff(prob)
        tmpdata = [copy.copy(sgn), copy.copy(intdata)]
        if isAdmissible(tmpdata, data_list):
            data_list += [copy.deepcopy(tmpdata)]
            N += 1

    # 問題の生成 ---------------------------------------------------------------------
    problems_tex = r"% seed: " + str(seed) + "\n"
    problems_tex += r"\begin{multienumerate}\restmultienumparameters"

    # 問題ごとの使用文字の確定
    mojinum = []
    for i in xrange(Nmax):
        n = rand_coeff(moji_prob)
        mojinum += [n]
        moji = moji_list[n]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % 2 == 0:
            problems_tex += "\n" + r"\mitemxx"
        problems_tex += r"{" + frac_polyn(moji, sgn, intdata) + r"}"

    problems_tex += "\n" + r"\end{multienumerate}"

    dt = datetime.datetime.now()
    file_name = dt.strftime("M1a_HW_frac_%Y%m%d_%H%M_%S")
    file = open(file_name + ".tex", "w")
    file.write(problems_tex)
    file.close()

    print "problems are generated..."

    colQ = 5
    answers_tex = r"% seed: " + str(seed) + "\n"
    answers_tex += r"%"

    for i in xrange(Nmax):
        n = mojinum[i]
        moji = moji_list[n]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % (2 * colQ) == 0:
            answers_tex += "\n" + r"\questionII{1cm}{%"
            page_open = True
            col_open = True
        answers_tex += "\n" + r"\qIIans{"
        answers_tex += frac_polyn(moji, sgn, intdata) + r"\\"
        #TeX += "\n" + r"& $ \speq " + frac_polynII(moji,sgn,intdata,not math_mode) + r" $ \fracv \\"
        g_int = gcd(intdata[0], intdata[3])
        bunbo = intdata[0] * intdata[3] / g_int
        intdata[0], intdata[3] = intdata[3] / g_int, intdata[0] / g_int
        answers_tex += "\n" + r"& $ \speq \myfrac{" + int_polyn(moji, sgn, intdata) + r"}{" + str(
            bunbo) + r"} $ \fracv \\"
        answers_tex += "\n" + r"& $ \speq \myfrac{" + tenkaiA(moji, sgn, intdata) + r"}{" + str(
            bunbo) + r"} $ \fracv \\"
        answers_tex += "\n" + r"& $ \speq \myfrac{" + tenkaiB(moji, sgn, intdata) + r"}{" + str(
            bunbo) + r"} $ \fracv \\"
        g = common_factor(sgn, intdata, bunbo)
        if g > 1:
            if bunbo == g:
                answers_tex += "\n" + r"& $ \speq " + tenkaiB_reduct(moji, sgn, intdata, g) + r" $ \fracv \\"
            else:
                answers_tex += "\n" + r"& $ \speq \myfrac{" + tenkaiB_reduct(moji, sgn, intdata, g) + r"}{" + str(bunbo / g) + r"} $ \fracv \\"
            answers_tex += "\n" + r"}{4cm}"
        else:
            answers_tex += "\n" + r"}{3.2cm}"
        if (i + 1) % colQ == 0:
            answers_tex += "\n" + r"}{%"
            col_open = False
        if (i + 1) % (2 * colQ) == 0:
            answers_tex += "\n" + r"}" + "\n" + r"%\newpage"
            page_open = False

    if col_open:
        answers_tex += "\n" + r"}{%"
    if page_open:
        answers_tex += "\n" + r"}"

    dt = datetime.datetime.now()
    file_name = dt.strftime("M1a_HW_fracAns_%Y%m%d_%H%M_%S")
    file = open(file_name + ".tex", "w")
    file.write(answers_tex)
    file.close()

    print "End."