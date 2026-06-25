---
title: 从零开始的Python(3)
date: 2025-03-24
categories:
    - 程序设计实习
slug: 从零开始的python3
hidden: true
seriesOrder: 10
---
这节课老师讲了Python的面向对象部分，速度比较快，但是结合前面cpp的大部分知识可以弄懂。
## 运算符的实现
### 描述
根据输出完善程序。

```py
class A:
	def __init__(self,x):
		self.x = x
// 在此处补充你的代码
a,b,c = map(int,input().split())
print(isinstance(A(2),A))
print(A(a) < A(b))
print(A(a) >= A(c))
print(A(a) < c)
```
### 输入
输入三个整数 $a,b,c$

```
2 8 5
```
### 输出
先输出一行``True``，然后依次输出 $a < b， a \geq c , a < c$ 三个表达式的值(``True``或``False``)。

```
True
True
False
True
```
### Solution
Python和cpp的特性差别在于，Python在Vscode中并没有直接告诉你要重载啥运算符的报错，因此需要观察相关的代码，这应该是与它是一行一行执行的语言有关。

观察代码，需要重载一个``小于号``和一个``大于等于号``，而这个小于号的左操作数和右操作数有多种类型，在Python中不需要多次写同个函数，只需要每次判断它们的类型就可以，即通过``isinstance``函数判断。

注意，Python中各个运算符的函数的名称是固定的，也许结合Markdown的语法比较好记。

```py
cclass A:

    def __init__(self, x):
        self.x = x

    def __lt__(self, other):
        if isinstance(other, A):
            return self.x < other.x
        else:
            return self.x < other

    def __ge__(self, other):
        return self.x >= other.x


# 在此处补充你的代码
a, b, c = map(int, input().split())
print(isinstance(A(2), A))
print(A(a) < A(b))
print(A(a) >= A(c))
print(A(a) < c)

```
## 组合函数
### 描述
Python支持高阶函数，即函数可以作为函数的参数和返回值。

下面程序的combine函数``combine(f,g)``能得到一个新函数k, ``k(x) = f(g(x))``，请填空。

```py
def combine(f, g):

    def k(x):
        return f(g(x))

    return k


# 在此处补充你的代码
def square(x):
    return x * x


def double(x):
    return x + x


n = int(input())
f = combine(square, double)
#提示： f(x) = square(double(x))
print(f(n))
g = combine(f, double)
#提示: g(x) = f(double(x))
print(g(n))

```
### 输入
整数 $n$

```
3
```
### 输出
第一行是 ``(2*n)*(2*n)``的值，第二行是 ``(2*(2*n)) * (2*(2*n))`` 的值。

```
36
144
```
### Solution
这道题不难，Python的返回值类型可以是函数，这是它高度自由的体现。

只需要新定义一个函数，然后这个函数的类型是f,g得出的就行。
```py
def combine(f,g):
	def k(x):
		return f(g(x))
	return k
# 在此处补充你的代码
def square(x):
	return x * x
def double(x):
	return x + x
n = int(input())
f = combine(square,double)
#提示： f(x) = square(double(x))
print(f(n))
g = combine(f,double)
#提示: g(x) = f(double(x))
print(g(n))
```
## 实现带标签的列表
### 描述
``TaggedList``表示元素带标签的列表。每个元素都有不同标签，标签是字符串。元素可以用整数做下标访问，也可以用标签做下标访问。请给出该类的实现。

```py
exit = None
class TaggedList:  #元素带标签的列表
// 在此处补充你的代码
a = TaggedList([70,80,90,100],["语文","数学","英语","物理"])
print(len(a),78 in a, 80 in a) #>>4 False True
print(str(a)) #>>语文:70,数学:80,英语:90,物理:100,
print(a[0],a['数学']) #>>70 80   标签也可以作为下标访问元素
a[1] = a['物理'] = 85
print(a) #>>语文:70,数学:85,英语:90,物理:85,
```
### 输入
```
None
```
### 输出
```
4 False True
语文:70,数学:80,英语:90,物理:100,
70 80
语文:70,数学:85,英语:90,物理:85,
```
### Solution
这题难度较大，需要你实现一个类，先明确题目的要求是什么。

首先，传入类构造的是两个列表，需要建构一个映射关系，题目相当于一个像字典一样，能根据键值关系访问，同时像列表一样能根据下标访问的数据结构。

那么，要怎么设计呢？如果在C++中，多半会用``两个map``，或者``一个map加一个vector``来写，这里就参照后者结果，将原来的分数作为vector的元素，此时只需建立科目到下标的映射，而后者是显然的字典结构。

注意``__init__``函数的构建方式，这样的``for``循环写起来挺快的。

随后，从后文代码中，还需要显式地实现``len``函数（获取列表长度）和``str``函数（转字符串），这里用到的``enumerate``和``zip``函数，算是遍历字典/列表结构的小窍门。

像C++一样，这里既然支持下标访问，那么就需要重载``[]``运算符，``Python``中有对应的``__getitem__``函数（支持访问），``__setitem__``函数（支持修改），同时还需要重载``in``关键字，即使用``__contains__``函数。
```py
exit = None


class TaggedList:  #元素带标签的列表

    def __init__(self, value, tags):
        self.values = value
        self.tag_index = {tag: idx for idx, tag in enumerate(tags)}

    def __len__(self):
        return len(self.values)

    def __contains__(self, item):
        return item in self.values

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.values[key]
        return self.values[self.tag_index[key]]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.values[key] = value
        else:
            self.values[self.tag_index[key]] = value

    def __str__(self):
        return ','.join(
            f"{tag}:{val}"
            for tag, val in zip(self.tag_index.keys(), self.values)) + ','


# 在此处补充你的代码
a = TaggedList([70, 80, 90, 100], ["语文", "数学", "英语", "物理"])
print(len(a), 78 in a, 80 in a)  #>>4 False True
print(str(a))  #>>语文:70,数学:80,英语:90,物理:100,
print(a[0], a['数学'])  #>>70 80   标签也可以作为下标访问元素
a[1] = a['物理'] = 85
print(a)  #>>语文:70,数学:85,英语:90,物理:85,
```
## 闭包
### 描述
程序填空，完成函数cons  
按要求输出结果
```py
def cons(x,y):
	s = a = b = None #防止作弊用
// 在此处补充你的代码
s = input().split()
a,b = s[0],s[1]
pair = cons(a,b)
print(pair(int(input())))
```
### 输入
第一行是两个字符串,用空格隔开，第二行是一个整数 $n$ 。

```
#样例1：
13 5
0
#样例2：
4 aa
1
#样例3：
bd c
7
```
### 输出
如果 $n=0$ ，则输出第一个字符串，如果 $n=1$ ，则输出第二个字符串，如果 $n$ 为其它数，则输出``error``。 

```
#样例1：
13
#样例2：
aa
#样例3：
error
```
### Solution
首先回顾闭包的定义，闭包指的是一个函数，加上它所捕获的、来自其定义时外层作用域的自由变量的绑定。

听起来有点不大好理解，转换为闭包的三个条件就是，它要在``另一个函数``内定义，且``内层函数``使用了``不是自己局部变量、也不是全局变量``的变量，同时外层函数结束的时候，临时变量能被保留。

从做题的角度来说，因为观察到最后的pair还是接收了一个n的，所以推测经过前面pair的处理返回的是一个关于``n``的函数，再根据给定的代码，然后重写一个函数返回就可以了。

但是，从闭包理解的角度，如果要弄懂这段代码，就要知道它如何形成闭包的，也就是在返回``pair``时，正常来说，临时变量``x、y``都被销毁了，不过此时返回给``pair``的``f``是记得这两个变量的，那么就可以处理了。
```py
def cons(x, y):
    s = a = b = None

    def f(n):
        if n == 0:
            return x
        elif n == 1:
            return y
        else:
            return "error"

    return f


# 在此处补充你的代码
s = input().split()
a, b = s[0], s[1]
pair = cons(a, b)
print(pair(int(input())))
```