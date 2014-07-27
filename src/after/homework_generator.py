#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'kimura'

from fractions import gcd
from datetime import datetime
import random


# TeX 出力 ------------------------------------------------------
def mathmode(expression):
    return "$" + expression + "$"


def myfrac(numerator, denominator):
    return r"\myfrac{" + str(numerator) + "}{" + str(denominator) + "}"


def mitemxx(left, right):
    return r"\mitemxx{" + left + "}{" + right + "}"


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
        return myfrac(numerator, denominator)
    elif numerator > 1:
        return str(numerator)
    else:
        return ""


# (ax+b)
def bracket_print(sgn_a, a, symbol, sgn_b, b):
    output = sgn_print(sgn_a, avoid_plus=True) + coeff(a) + symbol
    output += sgn_print(sgn_b) + str(b)
    return "(" + output + ")"


def int_polyn(symbol, sgn, intdata):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(intdata[0])
    output += bracket_print(sgn[1], intdata[1], symbol, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(intdata[3])
    output += bracket_print(sgn[4], intdata[4], symbol, sgn[5], intdata[5])
    return output


def frac_polyn(symbol, sgn, intdata):
    output = sgn_print(sgn[0], avoid_plus=True) + coeff(1, intdata[0])
    output += bracket_print(sgn[1], intdata[1], symbol, sgn[2], intdata[2])
    output += sgn_print(sgn[3]) + coeff(1, intdata[3])
    output += bracket_print(sgn[4], intdata[4], symbol, sgn[5], intdata[5])
    return output


# ax+b+cx+d
def tenkaiA(symbol, sgn, intdata):
    sgn_a = (sgn[0] + sgn[1]) % 2
    a = intdata[0] * intdata[1]
    sgn_b = (sgn[0] + sgn[2]) % 2
    b = intdata[0] * intdata[2]
    sgn_c = (sgn[3] + sgn[4]) % 2
    c = intdata[3] * intdata[4]
    sgn_d = (sgn[3] + sgn[5]) % 2
    d = intdata[3] * intdata[5]

    output = sgn_print(sgn_a, avoid_plus=True) + coeff(a) + symbol
    output += sgn_print(sgn_b) + str(b)
    output += sgn_print(sgn_c) + coeff(c) + symbol
    output += sgn_print(sgn_d) + str(d)
    return output


# ax+b
def tenkaiB(symbol, sgn, intdata):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid_plus = False

    if a > 0:
        output += coeff(a) + symbol
    elif a < 0:
        output += "-" + coeff(a * (-1)) + symbol
    else:
        avoid_plus = True

    if b > 0:
        output += sgn_print(0, avoid_plus) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    return output


# 答えが約分可能かどうか。係数と分母の最大公約数
def common_factor(sgn, intdata, denominator):
    coeff = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    return gcd(gcd(abs(coeff), abs(constt)), denominator)


# ax+b
# 約分実行
def tenkaiB_reduct(symbol, sgn, intdata, g):
    output = ""
    a = intdata[0] * intdata[1] * (-1) ** (sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1) ** (sgn[3] + sgn[4])
    b = intdata[0] * intdata[2] * (-1) ** (sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1) ** (sgn[3] + sgn[5])
    avoid_plus = False
    a = a / g
    b = b / g

    if a > 0:
        output += coeff(a) + symbol
    elif a < 0:
        output += "-" + coeff(a * (-1)) + symbol
    else:
        avoid_plus = True

    if b > 0:
        output += sgn_print(0, avoid_plus) + str(b)
    elif b < 0:
        output += "-" + str(b * (-1))
    else:
        if a == 0:
            output += "0"

    return output


# 排除すべきデータならFalse. 同じ問題と、左右入れ替えただけのものと、カッコの前が+1なものだけ排除
def isAdmissible(data, data_list):
    lL = len(data[0])
    lR = len(data[1])
    exchange_data = [data[0][lL / 2:lL] + data[0][0:lL / 2], data[1][lR / 2:lR] + data[1][0:lR / 2]]

    a = data not in data_list
    b = exchange_data not in data_list
    c = not (data[0][0] == 0 and data[1][0] == 1)
    d = not (data[0][lL / 2] == 0 and data[1][lR / 2] == 1)
    e = not (data[1][0] == data[1][3])  # 分数の場合のみ排除したいが今回は排除。分母が同じものは排除。

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


def create_problems_tex(data_list, symbols):
    tex = r"\begin{multienumerate}\restmultienumparameters" + "\n"
    at_int_mode = True

    for i in xrange(0, len(data_list), 2):
        polyn = int_polyn if at_int_mode else frac_polyn

        left_problem  = mathmode(polyn(symbols[i],   sgn=data_list[i][0],   intdata=data_list[i][1]))
        right_problem = mathmode(polyn(symbols[i+1], sgn=data_list[i+1][0], intdata=data_list[i+1][1]))
        tex += mitemxx(left_problem, right_problem) + "\n"

        at_int_mode = not at_int_mode  # 2題ごとに整数モードと分数モードの切り替え

    tex += r"\end{multienumerate}"
    return tex


def create_answers_tex(data_list, symbols):
    tex = "%"
    at_frac_mode = True
    at_newpage = True
    col_height_max = 17
    vskip = 0.45

    for i in xrange(len(data_list)):
        symbol = symbols[i]
        sgn = data_list[i][0]
        intdata = data_list[i][1]

        if i % 2 == 0:
            at_frac_mode = not at_frac_mode  # 2題ごとに分数モードと整数モードの切り替え

        if at_newpage:
            tex += "\n" + r"\questionII{1cm}{%"
            at_first_column = True
            col_height = 0.0
            page_open = True
            col_open = True
            at_newpage = False

        tex += "\n" + r"\qIIans{"
        if at_frac_mode:
            tex += mathmode(frac_polyn(symbol, sgn, intdata)) + r"\\"
            g_int = gcd(intdata[0], intdata[3])
            denominator = intdata[0] * intdata[3] / g_int
            intdata[0], intdata[3] = intdata[3] / g_int, intdata[0] / g_int
            tex += "\n" + r"& $ \speq " + myfrac(int_polyn(symbol, sgn, intdata), denominator) + r" $ \fracv \\"
            tex += "\n" + r"& $ \speq " + myfrac(tenkaiA(symbol, sgn, intdata), denominator) + r" $ \fracv \\"
            tex += "\n" + r"& $ \speq " + myfrac(tenkaiB(symbol, sgn, intdata), denominator) + r" $ \fracv \\"
            g = common_factor(sgn, intdata, denominator)
            if g > 1:
                if denominator == g:
                    tex += "\n" + r"& $ \speq " + tenkaiB_reduct(symbol, sgn, intdata, g) + r" $ \fracv \\"
                else:
                    tex += "\n" + r"& $ \speq " + myfrac(tenkaiB_reduct(symbol, sgn, intdata, g), denominator / g) + r" $ \fracv \\"
                tex += "\n" + r"}{4cm}"
                col_height += 4 + vskip
            else:
                tex += "\n" + r"}{3.2cm}"
                col_height += 3.2 + vskip
        else:
            tex += mathmode(int_polyn(symbol, sgn, intdata)) + r"\\"
            tex += "\n" + r"& $ \speq " + tenkaiA(symbol, sgn, intdata) + r"$\\"
            tex += "\n" + r"& $ \speq " + tenkaiB(symbol, sgn, intdata) + r"$\\"
            tex += "\n" + r"}{1.2cm}"
            col_height += 1.2 + vskip

        if col_height >= col_height_max:
            if at_first_column:
                tex += "\n" + r"%--- end of first column -----------------------------------------"
                tex += "\n" + r"}{%"
                col_open = False
                at_first_column = False
            else:
                tex += "\n" + r"%--- end of second column -----------------------------------------"
                tex += "\n" + r"}" + "\n" + r"%\newpage"
                page_open = False
                at_newpage = True
            col_height = 0.0

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
    # 1～9が、等確率で、大体10～19より30倍くらい出やすいように設定。
    coeff_probs = [0] + ([30] * 9) + ([1] * 10)

    symbol_list = ["x", "y", "a"]
    symbol_probs = [50, 1, 10]

    # データの生成 -------------------------------------------------------------------
    num_of_problems = 300  # とりあえず300題（2の倍数）
    data_list = []
    seed = 20140627
    random.seed(seed)

    while len(data_list) < num_of_problems:
        data = [
            [random.randint(0, 1) for i in range(6)],    # 符号情報
            [rand_coeff(coeff_probs) for i in range(6)]  # 絶対値情報
        ]
        if isAdmissible(data, data_list):
            data_list.append(data)

    # 問題ごとの使用文字番号を格納。解答の文字を揃えるため。
    symbols = [symbol_list[rand_coeff(symbol_probs)] for i in xrange(num_of_problems)]

    # texの1行目に、seed情報をコメント
    header = "% seed: " + str(seed) + "\n"

    # 問題の生成 ---------------------------------------------------------------------
    problems_tex = header + create_problems_tex(data_list, symbols)
    create_tex_file(datetime.now().strftime("M1a_HW_polyn_%Y%m%d_%H%M_%S"), problems_tex)
    print "problems are generated..."

    # 回答の生成 ---------------------------------------------------------------------
    answers_tex = header + create_answers_tex(data_list, symbols)
    create_tex_file(datetime.now().strftime("M1a_HW_polynAns_%Y%m%d_%H%M_%S"), answers_tex)
    print "End."