---
title: 【程序设计实习】python速通作业四
date: 2025-03-26
categories:
    - 程序设计实习
---
# A:Python:怎么能够这么求和
## 描述
程序填空 程序先输出10(10=1+2+3+4),30， 然后读入若干整数，并输出它们的和
```
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
## 输入
多组数据，每组一行，包括不超过100个整数（至少一个），其中第一个整数一定大于0。
## 输出
对每组数据，输出所有整数的和
## 样例输入
```
1 2 3
4 5
```
## 样例输出
```
10
30
6
9
```
# Solution
有点类似C++STL里的accumulate?  
我们要返回一个函数，同时这个函数能存储一个值，用闭包也能实现（当时写的时候不知道为啥忘记用闭包了）
```
def mysum(x):
    def inner(y=None):
        if y is None:
            return x
        return mysum(x + y)
    return inner
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

# B:函数累加器
## 描述
编写一个函数累加器accfunc

```
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
## 输入
多组数据，每组2行  
第一行形如：   
p_1 p_2 p_3 ....p_n  
p_i 是个字符串，值是 "f1", "f2", "f3", "f4", "f5" 中间的任何一个，代表程序中相应函数  
这一行项数不定，至少有1项  
第二行是个整数x  
对每组数据，输出以下函数调用的结果:  
p_n(p_n-1(...(p2(p1(x)...)  
## 输出
对每组数据，输出以下函数调用的结果:

p_n(p_n-1(...(p2(p1(x)...)
## 样例输入
```
f1 f2 f3
4
f2
5
f2 f2 f5
3
```
## 样例输出
```
50
25
77
```
## 提示
第一个例子，输出结果是 f3(f2(f1(4)))
第二个例子，输出结果是 f2(5)
# Solution
跟上题有点像，也可以用闭包  
直接把我当时写的代码搬上来了() 
```
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

# C:生成器
## 描述
下面程序输入正整数n和m，输出从0开始的前m个n的倍数，请写出times函数的内部实现。不得使用列表、元组、集合、字典，times必须是个生成器函数。
```
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
## 输入
两个整数 n和m
## 输出
n的前m个倍数（从0开始)
## 样例输入
```
2 5
```
## 样例输出
```
0
2
4
6
8
```
# Solution
题目的要求写得很清楚了，就是生成器  
生成器的原理课件里也挺清楚的  
在yield的时候停止并抛出下一个值就可以~  
```
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