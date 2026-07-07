---
title: 从零开始的Python(2)
date: 2025-03-19
categories:
    - 算法
slug: 从零开始的python2
hidden: true
seriesOrder: 8
---
## 矩阵转置
### 描述
输入一个 $n$ 行 $m$ 列的矩阵A，输出它的转置 $A^T$ 。
### 输入
第一行包含两个整数 $n$ 和 $m$ ，表示矩阵A的行数和列数。$1 \leq n \leq 100,1 \leq m \leq 100$ 。  
接下来 $n$ 行，每行 $m$ 个整数，表示矩阵A的元素。相邻两个整数之间用单个空格隔开，每个元素均在1~1000之间。

```
3 3
1 2 3
4 5 6
7 8 9
```

### 输出
$m$ 行，每行 $n$ 个整数，为矩阵A的转置。相邻两个整数之间用单个空格隔开。

```
1 4 7
2 5 8
3 6 9
```
### Solution
思路是直接模拟就可以，注意这里二维数组使用列表嵌套实现。

同时需要注意，二维数组的初始化形式，像下面这么写会更方便，如果一个一个``append``会很麻烦，虽然笔者在初学的时候就是这么干的。
```py
lst = input().split()
n = int(lst[0])
m = int(lst[1])
kd = [[] for _ in range(n)]
for i in range(0, n):
    x = input().split()
    for j in range(0, m):
        tem = int(x[j])
        kd[i].append(tem)
for i in range(0, m):
    for j in range(0, n):
        print(kd[j][i], end=' ')
    print()

```
## 扑克牌排序
### 描述
一副扑克牌有 $52$ 张牌，分别是红桃，黑桃，方片，梅花各 $13$ 张，不包含大小王，现在Alex抽到了 $n$ 张牌，请将扑克牌按照牌面从大到小的顺序排序。  

红桃(heart)用字母h表示，黑桃(spade)用字母s表示，方片(dianmond)用字母d表示，梅花(club)用字母c表示。

2~10的牌面直接用``2,3,4,5,6,7,8,9,10``表示，其余的分别为``A,J,Q,K``。 

牌面大小：2>A>K>Q>J>10>9>……>4>3，相同牌面的按照花色（h>s>d>c）顺序排。  
### 输入
多组数据。每组数据一行，表示当前摸到的 $n$ 张牌 $(1 \leq n \leq 52)$。

```
h7 c10 h4 s7 c5 cA dA c4 sJ h9 hQ d8 h2 s2 d9 sA dQ c6 hA
h7 s8 s7 c5 c8 cK sQ d2 s3 hQ d8 s10 sA d5 h10 hA
```
### 输出
针对每组数据，输出一行，即排序后的结果。

```
h2 s2 hA sA dA cA hQ dQ sJ c10 h9 d9 d8 h7 s7 c6 c5 h4 c4 
d2 hA sA cK hQ sQ h10 s10 s8 d8 c8 h7 s7 d5 c5 s3 
```
### Solution
这道题有两种做法，一种是使用``key``函数作为``sorted``的排序依据，类似``C++中的cmp``，以及函数可以一次返回多个值，这个算是Python的特色了，然后按照返回值的顺序进行排列，而``reverse=True``则是表示降序排列。

不过，排序这句还可以使用``lambda``表达式书写，即``lst_1=sorted(lst,key=lambda x:(x[1],x[0]))``的形式，表达式内就是关键字比较的顺序，不过还需要对原来的字符进行以下处理。

无论哪种做法，都需要注意本题中不定项输出的书写格式，因为不常见到容易遗忘。
```py
def pd(x):
    f = first_order[x[1:]]
    g = second_order[x[0]]
    return f, g


while True:
    try:
        lst = input().split()
        first_order = {'2': 15, 'A': 14, 'K': 13, 'Q': 12, 'J': 11}
        second_order = {'h': 3, 's': 2, 'd': 1, 'c': 0}
        for i in range(10, 2, -1):
            first_order[str(i)] = i
        lst_1 = sorted(lst, key=pd, reverse=True)
        for i in lst_1:
            print(i, end=' ')
        print()
    except EOFError:
        break

```
## 实现deepcopy
### 描述
填空实现下面的深拷贝函数deepcopy。

```py
def deepcopy(a):
// 在此处补充你的代码
a = [1,2,[3,[4],5],(6,[7,[8],9])]
b = deepcopy(a)
print(b)
a[2][1].append(400)
a[3][1][1].append(800)
print(a)
print(b)
```
### 输入
```
None
```
### 输出
```
[1, 2, [3, [4], 5], (6, [7, [8], 9])]
[1, 2, [3, [4, 400], 5], (6, [7, [8, 800], 9])]
[1, 2, [3, [4], 5], (6, [7, [8], 9)]
```
### Solution
这道题主要考察深拷贝的实现形式，首先要明确的是深拷贝是``复制全部的值``，而浅拷贝只是``复制一个引用``。

那么，深拷贝要怎么实现呢？  

回忆到之前讲过的，函数中像浮点、整型、字符串这样的是``不可变变量``，而列表、元组这样的是可变变量，如果直接用``等号复制``，会导致列表和元组会变成浅拷贝，即只返回了``引用``。

那么 只要递归到不可变变量进行``传值``就可以实现深拷贝了。

同时，需要注意Python中判断变量类型的语法。
```py
def deepcopy(a):
    if isinstance(a, list):
        tem = []
        for item in a:
            tem.append(deepcopy(item))
        return tem
    elif isinstance(a, tuple):
        tem = tuple(deepcopy(item) for item in a)
        return tem
    else:
        return a


a = [1, 2, [3, [4], 5], (6, [7, [8], 9])]
b = deepcopy(a)
print(b)
a[2][1].append(400)
a[3][1][1].append(800)
print(a)
print(b)

```
## 校园食宿预订系统
### 描述
某校园为方便学生订餐，推出食堂预定系统。食宿平台会在前一天提供菜单，学生在开饭时间前可订餐。  

食堂每天会推出 $m$ 个菜，每个菜有固定的菜价和总份数，售卖份数不能超过总份数。   

假设共有 $n$ 个学生点餐，每个学生固定点 $3$ 个菜，当点的菜售罄时, 学生就买不到这个菜了。   

请根据学生预定记录，给出食堂总的预定收入。   
数据满足 $1 \leq n \leq 6000，3 \leq m \leq 6000$ ，单品菜价不大于 $1000$ 元，每个菜的配额不超过 $3000$ 。  
### 输入
第一行两个整数 $n$ 和 $m$ ，代表有 $n$ 个学生订餐，共有 $m$ 个可选的菜。

下面 $m$ 行，每行三个元素，分别是菜名、售价和可提供量，保证菜名不重合，菜价为整数。

下面n行，每行三个元素，表示这个学生点的三个菜的菜名。

```
5 5
yangroupaomo 13 10
jituifan 7 5
luosifen 16 3
xinlamian 12 20
juruo_milktea 999 1
yangroupaomo luosifen juruo_milktea
luosifen xinlamian jituifan
yangroupaomo jituifan juruo_milktea
jituifan xinlamian luosifen
yangroupaomo yangroupaomo yangroupaomo
```
### 输出
一个整数，表示食堂的收入。

```
1157
```
### 提示
如果用python做，要用字典，如果用其它语言做，也要用类似的数据结构，否则会超时。

名字长度范围没有给出，长度不会太离谱。请自己选用合适的办法确保这不是个问题
### Solution
这道题的意义在于向大家介绍字典这个数据结构，笔者个人感觉它和C++的``map``非常类似，都是建立键值意义映射的关系，至于管理它的数据结构就不了解了，虽然此时按照道理程设并没有教到C++的STL，但是在计概中应该有见到过。

首先读取所有菜的名字，价格跟份数，随后再按照一个一个学生一次读入，分别判断他要吃的三道菜是否有存货，如果有则拿掉一份菜并加上收入，最后输出总收入即可。

```py
lst = input().split()
n = int(lst[0])
m = int(lst[1])
canteen = {}
price = {}
for i in range(0, m):
    k = input().split()
    course = k[0]
    p = int(k[1])
    num = int(k[2])
    canteen[course] = num
    price[course] = p
ans = 0
for i in range(0, n):
    k = input().split()
    tem = k[0]
    temp = k[1]
    te = k[2]
    if canteen[tem] != 0:
        ans += price[tem]
        canteen[tem] -= 1
    if canteen[temp] != 0:
        ans += price[temp]
        canteen[temp] -= 1
    if canteen[te] != 0:
        ans += price[te]
        canteen[te] -= 1
print(ans)
```