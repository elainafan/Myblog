---
title: 从零开始的Python(4)
date: 2025-03-26
categories:
    - 算法
slug: 从零开始的python4
hidden: true
seriesOrder: 11
---
## 怎么能够这么求和
### 描述
程序填空，程序先输出 $10(10=1+2+3+4),30$ ，然后读入若干整数，并输出它们的和。

```py
def mysum(x):
// 在此处补充你的代码
def exec(g,i) : #call g for i times
    if i == 1 :
        g()
    else:
        g()
        exec(g,i-1)

k = mysum(1)(2)(3)(4)
k2 = mysum(10)(20)

print(k())
print(k2())

while True:
    try:
        s = input()
        s = s.split()
        k = mysum
        for x in s:
            k = k(int(x))
        exec(k,int(s[0]))
        print(k())
    except:  #读到 eof产生异常
        break
```
### 输入
多组数据，每组一行，包括不超过 $100$ 个整数（至少一个），其中第一个整数一定大于0。

```
1 2 3
4 5
```
### 输出
对每组数据，输出所有整数的和。

```
10
30
6
9
```
### Solution
有点类似C++STL里的accumulate? 不过不知道也没有关系，毕竟这时候应该程设还没上到这。

观察上面的代码，不难发现需要返回一个函数，这个函数能存储一个临时变量的值，于是联想到使用``闭包``，即写一个内层函数，它能返回一个值。

注意，这里第一次加的时候内层需要使用``缺省参数``来初始化。
```py
def mysum(x):

    def inner(y=None):
        if y is None:
            return x
        return mysum(x + y)

    return inner


# 在此处补充你的代码
def exec(g, i):  #call g for i times
    if i == 1:
        g()
    else:
        g()
        exec(g, i - 1)


k = mysum(1)(2)(3)(4)
k2 = mysum(10)(20)

print(k())
print(k2())

while True:
    try:
        s = input()
        s = s.split()
        k = mysum
        for x in s:
            k = k(int(x))
        exec(k, int(s[0]))
        print(k())
    except:  #读到 eof产生异常
        break
```

## 函数累加器
### 描述
编写一个函数累加器accfunc。

```py
#pylint: disable = no-value-for-parameter
def accfunc(f):
// 在此处补充你的代码
def f1(x):
    return x + 1
def f2(x):
    return x * x
def f3(x):
    return x + x
def f4(x):
    return x*3
def f5(x):
    return x-4

while True:
    try:
        s = input()
        n = int(input())
        s = s.split()
        k = accfunc
        for x in s:
            k = k(eval(x))
        print(k()(n))
    except:  #读到 eof产生异常
        break
```
### 输入
多组数据，每组2行  
第一行形如： $p_1 p_2 p_3 ....p_n,p_i$ 是个字符串，值是 "f1", "f2", "f3", "f4", "f5" 中间的任何一个，代表程序中相应函数，这一行项数不定，至少有1项。
第二行是个整数 $x$ 。

```
f1 f2 f3
4
f2
5
f2 f2 f5
3
```
### 输出
对每组数据，输出以下函数调用的结果:  $p_n(p_n-1( \ldots (p2(p1(x)) \ldots )))$  

```
50
25
77
```
### 提示
第一个例子，输出结果是 f3(f2(f1(4)))
第二个例子，输出结果是 f2(5)
### Solution
思路跟上题是一样的，都是使用闭包进行类似记忆化的操作，当然这里传入的参数应该是一个函数，然后依次叠加。

```py
#pylint: disable = no-value-for-parameter
def accfunc(f):

    def inner(g=None):
        if g is None:
            return f
        else:
            return accfunc(lambda x: g(f(x)))

    return inner


def f1(x):
    return x + 1


def f2(x):
    return x * x


def f3(x):
    return x + x


def f4(x):
    return x * 3


def f5(x):
    return x - 4


while True:
    try:
        s = input().strip()
        n = int(input())
        funcs = s.split()
        k = accfunc  # 初始化为accfunc函数
        for func_name in funcs:
            func = eval(func_name)  # 获取对应的函数对象
            k = k(func)  # 将当前函数添加到组合链
        # 获取最终的组合函数并调用
        composed_func = k()
        print(composed_func(n))
    except:
        break
```

## 生成器
### 描述
下面程序输入正整数 $n$ 和 $m$ ，输出从0开始的前 $m$ 个 $n$ 的倍数，请写出times函数的内部实现。不得使用列表、元组、集合、字典，times必须是个生成器函数。
```py
exit = None
def times(n):
// 在此处补充你的代码
n,m = map(int,input().split())
seq = times(n)
if str(type(seq) == "<class 'generator'>"):
	i = 0
	for x in seq:
		print(x)
		i += 1
		if i == m:
			break
```
### 输入
两个整数 $n$ 和 $m$ 。

```
2 5
```
### 输出
$n$ 的前 $m$ 个倍数（从0开始）。

```
0
2
4
6
8
```
### Solution
题目的要求写得很清楚了，就是生成器，生成器的原理课件里也挺清楚的，这里回顾一下。

所谓生成器，就是含有``yield``关键字的函数，它不会一次性执行完，而是在``yield``的地方暂停，把当前值抛出，并保存全部的运行环境，而下一次使用，通常是通过``next(gen)``或者``for``循环开始。

顺便说一句，第一行``exit=None``没啥用，而``seq=times(n)``只是创建了一个生成器对象，而``for``循环才是真正在执行它。

于是就可以写出来了~
```py
exit = None
def times(n):
    num = 0
    while True:
        yield num
        num += n
n,m = map(int,input().split())
seq = times(n)
if str(type(seq) == "<class 'generator'>"):
	i = 0
	for x in seq:
		print(x)
		i += 1
		if i == m:
			break
```