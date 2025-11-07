---
title: 【程序设计实习】python速通作业三
date: 2025-03-24
categories:
    - 程序设计实习
---
这节课老师讲了Python的面向对象部分，速度比较快   
但是结合前面cpp的大部分知识可以弄懂  
# 01:运算符的实现
## 描述
程序填空
```
 

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
## 输入
输入三个整数a,b,c
## 输出
先输出一行True  
然后依次输出 a < b， a >= c , a < c 三个表达式的值(True或False)
## 样例输入
```
2 8 5
```
## 样例输出
```
True
True
False
True
```
# Solution
py和cpp的特性差别在于  
py并没有报错 直接告诉你要重载啥运算符  
我们看题目 需要重载一个小于号和一个大于等于号  
小于号要判断类型（相比cpp的重载函数里直接给定类型 这里只要重载一次再判断）  
下面看代码:  
```
class A:
	def __init__(self,x):
		self.x = x
	def __lt__(self,other):
		if isinstance(other,A):
			return self.x<other.x
		else:
			return self.x<other
	def __ge__(self,other):
		return self.x>=other.x
# 在此处补充你的代码
a,b,c = map(int,input().split())
print(isinstance(A(2),A))
print(A(a) < A(b))
print(A(a) >= A(c))
print(A(a) < c)
```
# 02:组合函数
## 描述
Python支持高阶函数，即函数可以作为函数的参数和返回值  
下面程序的combine函数 combine(f,g)能得到一个新函数k, k(x) = f(g(x))，请填空
```
def combine(f,g):
// 在此处补充你的代码
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
## 输入
整数n
## 输出
第一行是 (2*n)*(2*n)的值  
第二行是 (2*(2*n)) * (2*(2*n)) 的值
## 样例输入
```
3
```
## 样例输出
```
36
144
```
# Solution
简单题 因为py的返回值类型可以是函数 高度自由  
新定义一个函数 然后这个函数的类型是f,g得出的就行
```
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
# 03:实现带标签的列表
## 描述
TaggedList 表示元素带标签的列表。每个元素都有不同标签，标签是字符串。元素可以用整数做下标访问，也可以用标签做下标访问。请给出该类的实现
```
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
## 输入
无
## 输出
如样例
## 样例输入
无
## 样例输出
```
4 False True
语文:70,数学:80,英语:90,物理:100,
70 80
语文:70,数学:85,英语:90,物理:85,
```
# Solution
这题有点烧脑  
需要你实现一个类 我们先明确题目的要求是什么  
填入的是两个列表，我们需要建构一个映射关系  
因为题目相当于两个字典合并成一个 前面的数是值 而后面数字的编号和字符串都是键  
好了 怎么建立映射关系？  
当然是用后面的一个拼接函数来了 然后相当于是一个迭代的字典  
然后，我们通过查资料明确 contains getitem 和 setitem都是python用魔术方法定义的函数  
最后用str拼接  
下面看代码  
```
exit = None
class TaggedList:  #元素带标签的列表
    def __init__(self,value,tags):
        self.values=value
        self.tag_index={tag:idx for idx,tag in enumerate(tags)}
    def __len__(self):
        return len(self.values)
    def __contains__(self,item):
        return item in self.values
    def __getitem__(self,key):
        if isinstance(key,int):
            return self.values[key]
        return self.values[self.tag_index[key]]
    def __setitem__(self,key,value):
        if isinstance(key,int):
            self.values[key]=value
        else:
            self.values[self.tag_index[key]]=value
    def __str__(self):
        return ','.join(f"{tag}:{val}" for tag,val in zip(self.tag_index.keys(),self.values))+','
# 在此处补充你的代码
a = TaggedList([70,80,90,100],["语文","数学","英语","物理"])
print(len(a),78 in a, 80 in a) #>>4 False True
print(str(a)) #>>语文:70,数学:80,英语:90,物理:100,
print(a[0],a['数学']) #>>70 80   标签也可以作为下标访问元素
a[1] = a['物理'] = 85
print(a) #>>语文:70,数学:85,英语:90,物理:85,
```
# 04:闭包
## 描述
程序填空，完成函数cons  
按要求输出结果
```
def cons(x,y):
	s = a = b = None #防止作弊用
// 在此处补充你的代码
s = input().split()
a,b = s[0],s[1]
pair = cons(a,b)
print(pair(int(input())))
```
## 输入
第一行是两个字符串,用空格隔开  
第二行是一个整数n
## 输出
如果n 为0，则输出第一个字符串  
如果n 为1，则输出第二个字符串  
如果n 为其它数，则输出error  
## 样例输入
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
## 样例输出
```
#样例1：
13
#样例2：
aa
#样例3：
error
```
# Solution
这道题感觉比上道题简单   
因为我们观察到最后的pair还是接收了一个n的  
所以推测经过前面pair的处理返回的是一个关于n的函数  
然后重写一个函数返回就可以了  
```
def cons(x,y):
	s = a = b = None 
	def f(n):
		if n==0:
			return x
		elif n==1:
			return y
		else:
			return "error"
	return f
# 在此处补充你的代码
s = input().split()
a,b = s[0],s[1]
pair = cons(a,b)
print(pair(int(input())))
```