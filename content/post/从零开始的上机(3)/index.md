---
title: 从零开始的上机(3)
date: 2025-03-23
categories:
    - 程序设计实习
---
本次上机涉及内容：Python基础(I)(II)
## 求阶乘的和
### 描述
给定正整数n，求不大于n的正整数的阶乘的和（即求1!+2!+3!+...+n!）。

### 输入
输入有一行，包含一个正整数n（1 < n < 12）。

```
5
```
### 输出
输出有一行：阶乘的和。

```
153
```

### Solution
按照题意模拟即可，没什么难的。

```py
n = int(input())
ans = 0
res = 1
for i in range(1, n + 1):
    res *= i
    ans += res
print(ans)
```

## 画矩形
### 描述
根据参数，画出矩形。

### 输入
输入一行，包括四个参数：前两个参数为整数，依次代表矩形的高和宽（高不少于3行不多于10行，宽不少于5列不多于10列）；第三个参数是一个字符，表示用来画图的矩形符号；第四个参数为1或0，0代表空心，1代表实心。

```
7 7 @ 0
```
### 输出
输出画出的图形。

```
@@@@@@@
@     @
@     @
@     @
@     @
@     @
@@@@@@@
```
### Solution
也是按照题意模拟，注意需要判断是实心还是空心。
```py
lst = input().split()
x = int(lst[0])
y = int(lst[1])
d = lst[2]
z = int(lst[3])
if z == 1:
    for i in range(0, x):
        for j in range(0, y):
            print(d, end='')
        print()
elif z == 0:
    for i in range(0, x):
        if i == 0 or i == x - 1:
            for j in range(0, y):
                print(d, end='')
            print()
        else:
            for j in range(0, y):
                if j == 0 or j == y - 1:
                    print(d, end='')
                else:
                    print(' ', end='')
            print()
```

## 有趣的跳跃
### 描述
一个长度为 $n(n>0)$ 的序列中存在“有趣的跳跃”，当且仅当相邻元素的差的绝对值经过排序后正好是从 $1$ 到 $(n-1)$ 。例如，$1 4 2 3$ 存在“有趣的跳跃”，因为差的绝对值分别为 $3,2,1$ 。当然，任何只包含单个元素的序列一定存在“有趣的跳跃”。你需要写一个程序判定给定序列是否存在“有趣的跳跃”。

### 输入
一行，第一个数是 $n(0 < n < 3000),n$ 为序列长度，接下来有 $n$ 个整数，依次为序列中各元素，各元素的绝对值均不超过 $10^9$ 。

```
4 1 4 2 3
```
### 输出
一行，若该序列存在“有趣的跳跃”，输出"Jolly"，否则输出"Not jolly"。

```
Jolly
```
### Solution
这道题，首先需要特判 $n=1$ 的情况，否则无法使用差分。

接着，再用差分求出相邻差的绝对值，并一一判断即可。

```py
lst = input().split()
n = int(lst[0])
ans = [
    0,
]
if n == 1:
    print("Jolly")
    exit()
for i in range(1, n):
    ans.append(abs(int(lst[i]) - int(lst[i + 1])))
ans.sort()
for i in range(1, n):
    if ans[i] != i:
        print("Not jolly")
        exit()
print("Jolly")

```

## 石头剪刀布
### 描述
石头剪刀布是常见的猜拳游戏。石头胜剪刀，剪刀胜布，布胜石头。如果两个人出拳一样，则不分胜负。

一天，小A和小B正好在玩石头剪刀布。已知他们的出拳都是有周期性规律的，比如：“石头-布-石头-剪刀-石头-布-石头-剪刀……”，就是以“石头-布-石头-剪刀”为周期不断循环的。请问，小A和小B比了 $N$ 轮之后，谁赢的轮数多？

### 输入
输入包含三行。
第一行包含三个整数： $N，NA，NB$ ，分别表示比了 $N$ 轮，小A出拳的周期长度，小B出拳的周期长度。 $0 < N,NA,NB < 100$ 。
第二行包含 $NA$ 个整数，表示小A出拳的规律。
第三行包含 $NB$ 个整数，表示小B出拳的规律。
其中，0表示“石头”，2表示“剪刀”，5表示“布”。相邻两个整数之间用单个空格隔开。

```
10 3 4
0 2 5
0 5 0 2
```
### 输出
输出一行，如果小A赢的轮数多，输出A；如果小B赢的轮数多，输出B；如果两人打平，输出draw。

```
A
```
### Solution
由于比赛次数过少，因此直接使用循环遍历，同时同余判断即可。

```py
lst = input().split()
n = int(lst[0])
a = int(lst[1])
b = int(lst[2])
lst_1 = input().split()
lst_2 = input().split()
tem_a = [0]
tem_b = [0]
for i in range(0, a):
    tem_a.append(int(lst_1[i]))
for i in range(0, b):
    tem_b.append(int(lst_2[i]))
ans_1 = 0
ans_2 = 0
for i in range(1, n + 1):
    x = (i - 1) % a + 1
    y = (i - 1) % b + 1
    if tem_a[x] == tem_b[y]:
        continue
    elif tem_a[x] == 0 and tem_b[y] == 2:
        ans_1 += 1
        continue
    elif tem_a[x] == 0 and tem_b[y] == 5:
        ans_2 += 1
        continue
    elif tem_a[x] == 2 and tem_b[y] == 0:
        ans_2 += 1
        continue
    elif tem_a[x] == 2 and tem_b[y] == 5:
        ans_1 += 1
        continue
    elif tem_a[x] == 5 and tem_b[y] == 0:
        ans_1 += 1
        continue
    elif tem_a[x] == 5 and tem_b[y] == 2:
        ans_2 += 1
        continue
if ans_1 == ans_2:
    print("draw")
elif ans_1 > ans_2:
    print("A")
elif ans_2 > ans_1:
    print("B")

```

## 加密的病历单
小英是药学专业大三的学生，暑假期间获得了去医院药房实习的机会。

在药房实习期间，小英扎实的专业基础获得了医生的一致好评，得知小英在计算概论中取得过好成绩后，主任又额外交给她一项任务，解密抗战时期被加密过的一些伤员的名单。  

经过研究，小英发现了如下加密规律（括号中是一个“原文 -> 密文”的例子）  
1.原文中所有的字符都在字母表中被循环左移了三个位置（dec  -> abz）  

2.逆序存储（abcd -> dcba ）  

3.大小写反转（abXY -> ABxy）  
### 输入
一个加密的字符串。（长度小于50且只包含大小写字母）

```
GSOOWFASOq
```
### 输出
输出解密后的字符串。

```
Trvdizrrvj
```
### Solution
这道题要注意的有两个点，一个是大小写转换用``swapcase()``，另一个是ASCII码与字符间的转换，给定ASCII码用``chr``，反之使用``ord``。

```py
x = input()
l = len(x)
res_1 = x.swapcase()
res_2 = res_1[::-1]
res_3 = []
for i in range(0, l):
    if res_2[i] == 'X':
        res_3.append('A')
    elif res_2[i] == 'Y':
        res_3.append('B')
    elif res_2[i] == 'Z':
        res_3.append('C')
    elif res_2[i] == 'x':
        res_3.append('a')
    elif res_2[i] == 'y':
        res_3.append('b')
    elif res_2[i] == 'z':
        res_3.append('c')
    else:
        t = ord(res_2[i])
        t += 3
        res_3.append(chr(t))
for i in range(0, l):
    print(res_3[i], end='')
```

## 字符串最大跨距
### 描述
有三个字符串 $S,S_1,S_2$ ，其中，S长度不超过 $300$ ， $S_1$ 和 $S_2$ 的长度不超过 $10$ 。想检测 $S_1$ 和 $S_2$ 是否同时在 $S$ 中出现，且 $S_1$ 位于 $S_2$ 的左边，并在 $S$ 中互不交叉（即， $S_1$ 的右边界点在 $S_2$ 的左边界点的左侧）。计算满足上述条件的最大跨距（即，最大间隔距离：最右边的 $S_2$ 的起始点与最左边的 $S_1$ 的终止点之间的字符数目）。如果没有满足条件的 $S_1,S_2$ 存在，则输出-1。  
例如，S = "abcd123ab888efghij45ef67kl", S1="ab", S2="ef"，其中，S1在S中出现了2次，S2也在S中出现了2次，最大跨距为：18。
### 输入
三个串： $S,S_1,S_2$ ，其间以逗号间隔（注意， $S, S_1, S_2$ 中均不含逗号和空格）。

```
abcd123ab888efghij45ef67kl,ab,ef
```
### 输出
$S_1$ 和 $S_2$ 在 $S$ 中最大跨距；若在 $S$ 中没有满足条件的 $S_1$ 和 $S_2$ ，则输出-1。

```
18
```

### Solution
这题需要注意的是，``rfind``函数，可以找到某个字符串出现的最后一个位置，然后就做完了。

注意需要判断 $S_2$ 在 $S_1$ 左边的情况。
```py
lst = input().split(',')
s = lst[0]
a = lst[1]
b = lst[2]
l = s.find(a)
r = s.rfind(b)
if l == -1 or r == -1:
    print(-1)
    exit()
if r - l >= len(a):
    print(r - l - len(a))
else:
    print(-1)
```

## 矩阵加法
### 描述
输入两个 $n$ 行 $m$ 列的矩阵 $A$ 和 $B$ ，输出它们的和 $A+B$ 。

### 输入
第一行包含两个整数 $n$ 和 $m$ ，表示矩阵的行数和列数。 $1 \leq n \leq 100,1 \leq m \leq 100$ 。

接下来 $n$ 行，每行 $m$ 个整数，表示矩阵A的元素。
接下来 $n$ 行，每行 $m$ 个整数，表示矩阵B的元素。
相邻两个整数之间用单个空格隔开，每个元素均在 $1 \sim 1000$之间。

```
3 3
1 2 3
1 2 3
1 2 3
1 2 3
4 5 6
7 8 9
```
### 输出
$n$ 行，每行 $m$ 个整数，表示矩阵加法的结果。相邻两个整数之间用单个空格隔开。

```
2 4 6
5 7 9
8 10 12
```
### Solution
这道题还是模拟，不过要注意前面讲过的矩阵初始化方法，这样写起来比较简单。

```py
lst = input().split()
n = int(lst[0])
m = int(lst[1])
a = [[] for _ in range(n)]
b = [[] for _ in range(n)]
for i in range(0, n):
    k = input().split()
    for j in range(0, m):
        a[i].append(int(k[j]))
for i in range(0, n):
    k = input().split()
    for j in range(0, m):
        b[i].append(int(k[j]))
for i in range(0, n):
    for j in range(0, m):
        a[i][j] = a[i][j] + b[i][j]
for i in range(0, n):
    for j in range(0, m):
        print(a[i][j], end=' ')
    print()

```

## 肿瘤面积
### 描述
在一个正方形的灰度图片上，肿瘤是一块矩形的区域，肿瘤的边缘所在的像素点在图片中用0表示。其它肿瘤内和肿瘤外的点都用255表示。现在要求你编写一个程序，计算肿瘤内部的像素点的个数（不包括肿瘤边缘上的点）。已知肿瘤的边缘平行于图像的边缘。

### 输入
只有一个测试样例。第一行有一个整数 $n(n \leq 1000)$ ，表示正方形图像的边长。其后 $n$ 行每行有 $n$ 个整数，取值为 $0$ 或 $255$ 。整数之间用一个空格隔开。

```
5
255 255 255 255 255
255 0 0 0 255
255 0 255 0 255
255 0 0 0 255
255 255 255 255 255
```
### 输出
输出一行，该行包含一个整数，为要求的肿瘤内的像素点的个数。

```
1
```
### Solution
这道题按照数据类型还是模拟，因为 $O(n^2)$ 显然是可以接受的。

先找到肿瘤区域的左上和右下，再将内部像素点一个个遍历即可。

```py
n = int(input())
ma = [[] for _ in range(n)]
ans = 0
for i in range(0, n):
    k = input().split()
    for j in range(0, n):
        ma[i].append(int(k[j]))
lx = 0
ly = 0
for i in range(0, n):
    flag = 0
    for j in range(0, n):
        if ma[i][j] == 0:
            lx = i
            ly = j
            flag = 1
            break
    if flag == 1:
        break
rx = 0
ry = 0
for i in range(n - 1, -1, -1):
    flag = 0
    for j in range(n - 1, -1, -1):
        if ma[i][j] == 0:
            rx = i
            ry = j
            flag = 1
            break
    if flag == 1:
        break
ans = (rx - lx - 1) * (ry - ly - 1)
print(ans)

```

## 话题焦点人物
### 描述
微博提供了一种便捷的交流平台。一条微博中，可以提及其它用户。例如Lee发出一条微博为：“期末考试顺利 @Kim @Neo”，则Lee提及了Kim和Neo两位用户。 

我们收集了 $N(1 < N < 10000)$ 条微博，并已将其中的用户名提取出来，用小于等于100的正整数表示。  

通过分析这些数据，我们希望发现大家的话题焦点人物，即被提及最多的人（题目保证这样的人有且只有一个），并找出那些提及它的人。  
### 输入
输入共两部分：  
第一部分是微博数量 $N,1 < N < 10000$ 。  
第二部分是 $N$ 条微博，每条微博占一行，表示为：  
发送者序号 $a$ ，提及人数 $k(0 \leq k \leq 20)$ ，然后是 $k$个被提及者序号 $b_1,b_2 \ldots,b_k$ ，其中 $a$ 和 $b_1,b_2,\ldots,b_k$ 均为大于0小于等于100的整数。相邻两个整数之间用单个空格分隔。  

```
5
1 2 3 4
1 0
90 3 1 2 4
4 2 3 2
2 1 3
```
### 输出
输出分两行：  
第一行是被提及最多的人的序号；  
第二行是提及它的人的序号，从小到大输出，相邻两个数之间用单个空格分隔。同一个序号只输出一次。  

```
3
1 2 4
```
### Solution
这道题比较搞笑的是，最后输出结果的时候，注意可能一个发送人提及了多次某个人，即 $b_1,b_2,\ldots,b_n$ 不一定全部不同。

另一种做法是，可以用字典嵌套字典/列表来做，类似C++中的``map<int,vector<int>>ma;``。

```py
n = int(input())
ans = [0]
res = [0]
for i in range(1, 101):
    ans.append(0)
    res.append([])
for i in range(0, n):
    k = input().split()
    t = int(k[0])
    z = int(k[1])
    for j in range(2, z + 2):
        x = int(k[j])
        ans[x] += 1
        if t in res[x]:
            pass
        else:
            res[x].append(t)
mi = max(ans)
mixx = ans.index(mi)
print(mixx)
res[mixx].sort()
for i in res[mixx]:
    print(i, end=' ')
```
## 判断元素是否存在
### 描述
有一个集合M是这样生成的： (1) 已知 $k$ 是集合 M 的元素； (2) 如果 $y$ 是 M 的元素，那么， $2y+1$ 和 $3y+1$ 都是 M 的元素； (3) 除了上述二种情况外，没有别的数能够成为 M 的一个元素。  

问题：任意给定 $k(0 \leq k \leq 2^31)$ 和 $x(0 \leq x \leq 10^5)$ ，请判断 $x$ 是否是 M 的元素。如果是，则输出YES，否则，输出 NO  
### 输入
输入整数 $k$ 和 $x$ , 逗号间隔。

```
0,22
```
### 输出
如果是，则输出 YES，否则，输出NO。

```
YES
```
### Solution
联想到计概中学过的类似题目，直接搜索即可，这题的复杂度完全是够的，也不需要用记忆化。

至于Python的递归，逻辑跟C++的差不多，注意这里使用``global``关键字表示可以对全局变量 $n$ 进行修改和调用，而一般是将其作为不可变变量处理的。\

同时为了节省时间，可以直接特判 $k>n$ 的情况。

```py
def check(x):
    global n
    if x > n:
        return False
    if x == n:
        return True
    return check(2 * x + 1) or check(3 * x + 1)


lst = input().split(',')
k = int(lst[0])
n = int(lst[1])
if k > n:
    print("NO")
    exit()
t = check(k)
if t == True:
    print("YES")
else:
    print("NO")

```