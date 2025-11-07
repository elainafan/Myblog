---
title: 【程序设计实习】python速通作业二
date: 2025-03-19
categories:
    - 程序设计实习
---
# A:矩阵转置
## 描述
输入一个n行m列的矩阵A，输出它的转置AT。
##  输入
第一行包含两个整数n和m，表示矩阵A的行数和列数。1 <= n <= 100，1 <= m <= 100。  
接下来n行，每行m个整数，表示矩阵A的元素。相邻两个整数之间用单个空格隔开，每个元素均在1~1000之间。
## 输出
m行，每行n个整数，为矩阵A的转置。相邻两个整数之间用单个空格隔开。
## 样例输入
```
3 3
1 2 3
4 5 6
7 8 9
```
## 样例输出
```
1 4 7
2 5 8
3 6 9
```
# Solution
没啥 就直接模拟  
注意 列表是可以嵌套的就行
```
lst=input().split()
n=int(lst[0])
m=int(lst[1])
kd=[]
for i in range(0,n):
    kd.append([])
for i in range(0,n):
    x=input().split()
    for j in range(0,m):
        tem=int(x[j])
        kd[i].append(tem)
for i in range(0,m):
    for j in range(0,n):
        print(kd[j][i],end=' ')
    print()
```
# B:扑克牌排序
## 描述
一副扑克牌有52张牌，分别是红桃，黑桃，方片，梅花各13张，不包含大小王，现在Alex抽到了n张牌，请将扑克牌按照牌面从大到小的顺序排序。  
牌的表示方法：  
红桃(heart)用字母h表示  
黑桃(spade)用字母s表示  
方片(dianmond)用字母d表示  
梅花(club)用字母c表示  
2~10的牌面直接用2,3,4,5,6,7,8,9,10 表示，其余的分别为A，J，Q，K  
比如方片J用dJ表示， 红桃A用hA表示  
牌面大小：  
2>A>K>Q>J>10>9>……>4>3  
相同牌面的按照花色（h>s>d>c）顺序排。  
## 输入
多组数据。每组数据一行，表示当前摸到的n张牌（1 < n <=52）。
## 输出
针对每组数据，输出一行，即排序后的结果。
## 样例输入
```
h7 c10 h4 s7 c5 cA dA c4 sJ h9 hQ d8 h2 s2 d9 sA dQ c6 hA
h7 s8 s7 c5 c8 cK sQ d2 s3 hQ d8 s10 sA d5 h10 hA
```
## 样例输出
```
h2 s2 hA sA dA cA hQ dQ sJ c10 h9 d9 d8 h7 s7 c6 c5 h4 c4 
d2 hA sA cK hQ sQ h10 s10 s8 d8 c8 h7 s7 d5 c5 s3 
```
# Solution
这道题主要就是讲key函数可以作为sorted的排序依据，类似cmp，以及一次返回多个值，起到一个另类结构体的效果  
- ### 笔者注：到期末考前只会写lambda表达式作为key了，判断函数是啥？
```
def pd(x):
    f=first_order[x[1:]]
    g=second_order[x[0]]
    return f,g
while True:
    try:
        lst=input().split()
        first_order={'2':15,'A':14,'K':13,'Q':12,'J':11}
        second_order={'h':3,'s':2,'d':1,'c':0}
        for i in range(10,2,-1):
            first_order[str(i)]=i
        lst_1=sorted(lst,key=pd,reverse=True)
        for i in lst_1:
            print(i,end=' ')
        print()
    except EOFError:
        break
```
# C:实现deepcopy
## 描述
填空实现下面的深拷贝函数deepcopy
```
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
## 输入
无
## 输出
[1, 2, [3, [4], 5], (6, [7, [8], 9])]
[1, 2, [3, [4, 400], 5], (6, [7, [8, 800], 9])]
[1, 2, [3, [4], 5], (6, [7, [8], 9])]
## 样例输入
无
## 样例输出
```
[1, 2, [3, [4], 5], (6, [7, [8], 9])]
[1, 2, [3, [4, 400], 5], (6, [7, [8, 800], 9])]
[1, 2, [3, [4], 5], (6, [7, [8], 9)]
```
# Solution
这道题主要考察深拷贝的实现形式  
那么 深拷贝要怎么实现呢？  
首先，我们要明确的是  
在函数中 像浮点、整型、字符串这样的是不可变变量  
而列表、元组这样的是可变变量  
这样导致列表和元组会变成浅拷贝  
那么 只要递归到不可变变量进行传值就可以实现深拷贝了  
```
def deepcopy(a):
    if isinstance(a,list):
        tem=[]
        for item in a:
            tem.append(deepcopy(item))
        return tem
    elif isinstance(a,tuple):
        tem=tuple(deepcopy(item) for item in a)
        return tem
    else:
        return a
a = [1,2,[3,[4],5],(6,[7,[8],9])]
b = deepcopy(a)
print(b)
a[2][1].append(400)
a[3][1][1].append(800)
print(a)
print(b)
```
# D:校园食宿预订系统
## 描述
某校园为方便学生订餐，推出食堂预定系统。食宿平台会在前一天提供菜单，学生在开饭时间前可订餐。  
食堂每天会推出m个菜，每个菜有固定的菜价和总份数，售卖份数不能超过总份数。   
假设共有n个学生点餐，每个学生固定点3个菜，当点的菜售罄时, 学生就买不到这个菜了。   
请根据学生预定记录，给出食堂总的预定收入   
数据满足1 <= n <= 6000，3 <= m <= 6000，单品菜价不大于1000元，每个菜的配额不超过3000  
## 输入
第一行两个整数n和m，代表有n个学生订餐，共有m个可选的菜  
下面m行，每行三个元素，分别是菜名、售价和可提供量，保证菜名不重合，菜价为整数  
下面n行，每行三个元素，表示这个学生点的三个菜的菜名  
## 输出
一个整数，表示食堂的收入
## 样例输入
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
## 样例输出
```
1157
```
## 提示
如果用python做，要用字典，  
如果用其它语言做，也要用类似的数据结构  
否则会超时  
名字长度范围没有给出，长度不会太离谱。请自己选用合适的办法确保这不是个问题
# Solution
字典这玩意吧，我感觉，就像C++中的map  
而且添加的时候直接加就可以了  
很方便  
这题用两个字典  
```
lst=input().split()
n=int(lst[0])
m=int(lst[1])
canteen={}
price={}
for i in range(0,m):
    k=input().split()
    course=k[0]
    p=int(k[1])
    num=int(k[2])
    canteen[course]=num
    price[course]=p
ans=0
for i in range(0,n):
    k=input().split()
    tem=k[0]
    temp=k[1]
    te=k[2]
    if canteen[tem]!=0:
        ans+=price[tem]
        canteen[tem]-=1
    if canteen[temp]!=0:
        ans+=price[temp]
        canteen[temp]-=1
    if canteen[te]!=0:
        ans+=price[te]
        canteen[te]-=1
print(ans)
```