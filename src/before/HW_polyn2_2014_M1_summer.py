﻿#coding:utf-8
'''
Created on 2014/06/24
2014年度 M1 夏休みの宿題生成装置
@author: NSatoh
'''

import random
import copy
import datetime

# global ------------------------------------------------------
avoid_plus = True
no_avoid = False
math_mode = True

# 数学関数 ------------------------------------------------------
def gcd(a,b):
    if b == 0:
        return a
    r = a % b
    return gcd(b,r)

def abs(x):
    if x >= 0:
        return x
    else:
        return x*(-1)

# TeX 出力 ------------------------------------------------------
def sgn_print(boolnum,avoid_plus):
    output = "+"
    if boolnum == 1:
        output = "-"
    elif avoid_plus:
        output = ""
    return output


def int_coeff(num):
    output = ""
    if num > 1:
        output += str(num)
    return output

def frac_coeff(num):
    output = ""
    if num > 1:
        output += r"\myfrac{1}{" + str(num) + r"}"
    return output

def bracket_print(sgnL,coeff,moji,sgnR,int):
    output = r"(" + sgn_print(sgnL,avoid_plus) + int_coeff(coeff) + moji 
    output += sgn_print(sgnR,no_avoid) + str(int) + r")"
    return output

def bracket_fracstyle_print(bunbo,sgnL,coeff,moji,sgnR,int):
    output = r"\myfrac{(" + sgn_print(sgnL,avoid_plus) + int_coeff(coeff) + moji 
    output +=  sgn_print(sgnR,no_avoid) + str(int) + r")}{" + str(bunbo) + r"}"
    return output

def int_polyn(moji,sgn,intdata,atMathMode):
    output = r""
    if atMathMode:
        output += r"$"
    output += sgn_print(sgn[0],avoid_plus) + int_coeff(intdata[0])
    output += bracket_print(sgn[1],intdata[1],moji,sgn[2],intdata[2])
    output += sgn_print(sgn[3],no_avoid) + int_coeff(intdata[3])
    output += bracket_print(sgn[4],intdata[4],moji,sgn[5],intdata[5])
    if atMathMode:
        output += r"$"
    return output
 
def frac_polynI(moji,sgn,intdata):
    output = r"$" 
    output += sgn_print(sgn[0],avoid_plus) + frac_coeff(intdata[0])
    output += bracket_print(sgn[1],intdata[1],moji,sgn[2],intdata[2])
    output += sgn_print(sgn[3],no_avoid) + frac_coeff(intdata[3])
    output += bracket_print(sgn[4],intdata[4],moji,sgn[5],intdata[5])
    output += r"$"
    return output

def frac_polynII(moji,sgn,intdata,atMathMode):
    output = r""
    if atMathMode:
        output += r"$"
    output += sgn_print(sgn[0],avoid_plus)
    output += bracket_fracstyle_print(intdata[0],sgn[1],intdata[1],moji,sgn[2],intdata[2])
    output += sgn_print(sgn[3],no_avoid)
    output += bracket_fracstyle_print(intdata[3],sgn[4],intdata[4],moji,sgn[5],intdata[5])
    if atMathMode:
        output += r"$"
    return output

def tenkaiA(moji,sgn,intdata,atMathMode):
    output = r""
    if atMathMode:
        output += r"$"
    sgnA = (sgn[0] + sgn[1]) % 2
    coeffA = intdata[0] * intdata[1]
    sgnB = (sgn[0] + sgn[2]) % 2
    coeffB = intdata[0] * intdata[2]
    sgnC = (sgn[3] + sgn[4]) % 2
    coeffC = intdata[3] * intdata[4]
    sgnD = (sgn[3] + sgn[5]) % 2
    coeffD = intdata[3] * intdata[5]
    output += sgn_print(sgnA,avoid_plus) + int_coeff(coeffA) + moji
    output += sgn_print(sgnB,no_avoid) + str(coeffB)
    output += sgn_print(sgnC,no_avoid) + int_coeff(coeffC) + moji
    output += sgn_print(sgnD,no_avoid) + str(coeffD)
    if atMathMode:
        output += r"$"
    return output

def tenkaiB(moji,sgn,intdata,atMathMode):
    output = r""
    if atMathMode:
        output += r"$"
    coeff = intdata[0] * intdata[1] * (-1)**(sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1)**(sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1)**(sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1)**(sgn[3] + sgn[5])
    avoid = False
    if coeff > 0:
        output += int_coeff(coeff) + moji
    elif coeff < 0:
        output += "-" + int_coeff(coeff*(-1)) + moji
    else:
        avoid = True
    if constt > 0:
        output += sgn_print(0,avoid) + str(constt)
    elif constt < 0:
        output += "-" + str(constt*(-1))
    else:
        if coeff == 0:
            output += "0"
    if atMathMode:
        output += r"$"
    return output

# 答えが約分可能かどうか。係数と分母の最大公約数
def common_factor(sgn,intdata,bunbo):
    coeff = intdata[0] * intdata[1] * (-1)**(sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1)**(sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1)**(sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1)**(sgn[3] + sgn[5])
    gi = gcd(abs(coeff),abs(constt))
    gii = gcd(gi,bunbo)
    return gii

# 約分実行
def tenkaiB_reduct(moji,sgn,intdata,atMathMode,g):
    output = r""
    if atMathMode:
        output += r"$"
    coeff = intdata[0] * intdata[1] * (-1)**(sgn[0] + sgn[1]) + intdata[3] * intdata[4] * (-1)**(sgn[3] + sgn[4])
    constt = intdata[0] * intdata[2] * (-1)**(sgn[0] + sgn[2]) + intdata[3] * intdata[5] * (-1)**(sgn[3] + sgn[5])
    avoid = False
    coeff = coeff / g
    constt = constt / g
    if coeff > 0:
        output += int_coeff(coeff) + moji
    elif coeff < 0:
        output += "-" + int_coeff(coeff*(-1)) + moji
    else:
        avoid = True
    if constt > 0:
        output += sgn_print(0,avoid) + str(constt)
    elif constt < 0:
        output += "-" + str(constt*(-1))
    else:
        if coeff == 0:
            output += "0"
    if atMathMode:
        output += r"$"
    return output


# 排除すべきデータならFalse. 同じ問題と、左右入れ替えただけのものと、カッコの前が+1なものだけ排除

def isAdmissible(tmpdata,data_list):
    lL = len(tmpdata[0])
    lR = len(tmpdata[1])
    exchange_tmpdata = [tmpdata[0][lL/2:lL]+tmpdata[0][0:lL/2],tmpdata[1][lR/2:lR]+tmpdata[1][0:lR/2]]
    a = tmpdata not in data_list 
    b = exchange_tmpdata not in data_list
    c = not (tmpdata[0][0] == 0 and tmpdata[1][0] == 1)
    d = not (tmpdata[0][lL/2] == 0 and tmpdata[1][lR/2] == 1)
    e = not (tmpdata[1][0] == tmpdata[1][3]) # 分数の場合のみ。分母が同じものは排除。
    return a and b and c and d and e


# 乱数の割合調節
def rand_coeff(prob):
    s = sum(prob)
    int = random.randint(1,s)
    interval = 0
    for i in xrange(len(prob)):
        if interval <= int and int <= interval + prob[i]:
            return i
        interval += prob[i]

if __name__ == "__main__":
    #prob = [0]*5
    #prob[1] = 30
    #prob[2] = 10
    #prob[3] = 10
    #prob[4] = 50

    # 係数の出やすさ設定
    prob = [0]*20
    # 1～9が、等確率で、大体10～19より30倍くらい出やすいように設定。
    for i in xrange(1,10):
        prob[i] = 30
    for i in xrange(10,20):
        prob[i] = 1

    moji_list = ["x","y","a"]
    moji_prob = [50,1,10]

    #cnt = [0]*20
    #for j in xrange(1000):
    #    a = rand_coeff(prob)
    #    cnt[a] += 1
    #
    #print cnt

    # データの生成 -------------------------------------------------------------------
    sgn = [0]*6
    intdata = [0]*6
    data_list = []
    seed = 20140627
    random.seed(seed)

    Nmax = 200 # とりあえず200題（2の倍数）
    N = 0 # = len(data_list)
    while N < Nmax:
        for j in xrange(6):
            sgn[j] = random.randint(0,1)
            intdata[j] = rand_coeff(prob)
        tmpdata = [copy.copy(sgn),copy.copy(intdata)]
        if isAdmissible(tmpdata,data_list):
            data_list +=[copy.deepcopy(tmpdata)]
            N += 1

    # 問題の生成 ---------------------------------------------------------------------
    TeX = r"% seed: " + str(seed) + "\n"
    TeX += r"\begin{multienumerate}\restmultienumparameters"

    # 問題ごとの使用文字の確定
    mojinum = []
    for i in xrange(Nmax):
        n = rand_coeff(moji_prob)
        mojinum += [n]
        moji = moji_list[n]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % 2 == 0:
            TeX += "\n" + r"\mitemxx"
        TeX +=r"{" + frac_polynI(moji,sgn,intdata) + r"}"

    TeX += "\n" + r"\end{multienumerate}"

    dt = datetime.datetime.now()
    file_name = dt.strftime("M1a_HW_frac_%Y%m%d_%H%M_%S")
    file = open(file_name+".tex" ,"w")
    file.write(TeX)
    file.close()

    print "plobrems are generated..."

    colQ = 5
    TeX = r"% seed: " + str(seed) + "\n"
    TeX += r"%"

    for i in xrange(Nmax):
        n = mojinum[i]
        moji = moji_list[n]
        sgn = data_list[i][0]
        intdata = data_list[i][1]
        if i % (2*colQ) == 0:
            TeX += "\n" + r"\questionII{1cm}{%"
            page_open = True
            col_open = True
        TeX += "\n" + r"\qIIans{"
        TeX += frac_polynI(moji,sgn,intdata) + r"\\"
        #TeX += "\n" + r"& $ \speq " + frac_polynII(moji,sgn,intdata,not math_mode) + r" $ \fracv \\"
        g_int = gcd(intdata[0], intdata[3])
        bunbo = intdata[0] * intdata[3] / g_int
        intdata[0], intdata[3] = intdata[3]/g_int, intdata[0]/g_int
        TeX += "\n" + r"& $ \speq \myfrac{" + int_polyn(moji,sgn,intdata,not math_mode) + r"}{" + str(bunbo) + r"} $ \fracv \\"
        TeX += "\n" + r"& $ \speq \myfrac{" + tenkaiA(moji,sgn,intdata,not math_mode) + r"}{" + str(bunbo) + r"} $ \fracv \\"
        TeX += "\n" + r"& $ \speq \myfrac{" + tenkaiB(moji,sgn,intdata,not math_mode) + r"}{" + str(bunbo) + r"} $ \fracv \\"
        g = common_factor(sgn,intdata,bunbo)
        if g > 1:
            if bunbo == g:
                TeX += "\n" + r"& $ \speq " + tenkaiB_reduct(moji,sgn,intdata,not math_mode,g) + r" $ \fracv \\"
            else:
                TeX += "\n" + r"& $ \speq \myfrac{" + tenkaiB_reduct(moji,sgn,intdata,not math_mode,g) + r"}{" + str(bunbo/g) + r"} $ \fracv \\"
            TeX += "\n" + r"}{4cm}"
        else:
            TeX += "\n" + r"}{3.2cm}"
        if (i+1) % colQ == 0:
            TeX += "\n" + r"}{%"
            col_open = False
        if (i+1) % (2*colQ) == 0:
            TeX += "\n" + r"}" + "\n" + r"%\newpage"
            page_open = False


    if col_open:
        TeX += "\n" + r"}{%"
    if page_open:
        TeX += "\n" + r"}"

    dt = datetime.datetime.now()
    file_name = dt.strftime("M1a_HW_fracAns_%Y%m%d_%H%M_%S")
    file = open(file_name+".tex" ,"w")
    file.write(TeX)
    file.close()

    print "End."

