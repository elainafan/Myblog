---
title: 从零开始的上机(4)
date: 2025-03-30
categories:
    - 程序设计实习
---
## 求分数序列和
### 描述
有一个分数序列 $\frac{q_1}{p_1},\frac{q_2}{p_2},\frac{q_3}{p_3},\frac{q_4}{p_4},\frac{q_5}{p_5} \ldots$ ，其中 $q_{i+1}=q_i+p_i,p_{i+1}=q_i,p_1,q_1=2$ 。求这个分数序列的前n项之和。
### 输入
输入有一行，包含一个正整数 $n \ (n \leq 30)$

```
2
```

### 输出
输出有一行，包含一个浮点数，表示分数序列前 $n$ 项的和，精确到小数点后4位。

```
3.5000
```

### Solution
不难发现分子跟分母都是斐波那契数列，因此直接模拟即可，注意不要忘记保留小数点的语句。

```py
n = int(input())
p = [0, 1]
q = [0, 2]
ans = 0
for i in range(2, n + 1):
    p.append(q[i - 1])
    q.append(p[i - 1] + q[i - 1])
for i in range(1, n + 1):
    ans += q[i] / p[i]
print(f"{ans:.4f}")

```

## 字符串中最长的连续出现的字符
### 描述
求一个字符串中最长的连续出现的字符，输出该字符及其出现次数。字符串中无空白字符（空格、回车和tab），如果这样的字符不止一个，则输出出现最早的字符。

### 输入
一行，一个不包含空白字符的字符串，字符串长度小于200。

```
aaaaadbbbbbcccccccdddddddddd
```

### 输出
一行，输出最长的连续出现的字符及其最长的连续出现次数，中间以一个空格分开。

```
d 10
```

### Solution
边遍历边统计最大的连续字符数量及其对应字符即可，时间复杂度为 $O(n)$ 。

```py
x = input()
mi = ""
ans = 0
temp = 0
for i in range(0, len(x)):
    if i == 0:
        ans = 1
        temp = 1
        mi = x[i]
        continue
    if x[i] == x[i - 1]:
        if i == len(x) - 1:
            temp += 1
            if temp > ans:
                mi = x[i]
                ans = temp
        else:
            temp += 1
    else:
        if temp > ans:
            ans = temp
            mi = x[i - 1]
        temp = 1
print(mi, end=' ')
print(ans)
```

## 病人排队
### 描述
病人登记看病，编写一个程序，将登记的病人按照以下原则排出看病的先后顺序：

1. 老年人（年龄 >= 60岁）比非老年人优先看病。

2. 老年人按年龄从大到小的顺序看病，年龄相同的按登记的先后顺序排序。

3. 非老年人按登记的先后顺序看病。

### 输入
第1行，输入一个小于100的正整数，表示病人的个数。

后面按照病人登记的先后顺序，每行输入一个病人的信息，包括：一个长度小于10的字符串表示病人的ID（每个病人的ID各不相同且只含数字和字母），一个整数表示病人的年龄，中间用单个空格隔开。

```
5
021075 40
004003 15
010158 67
021033 75
102012 30
```

### 输出
按排好的看病顺序输出病人的ID，每行一个。

```
021033
010158
021075
004003
102012
```

### Solution
这题考察``lambda``表达式排序的算法，即将老人与年轻人先分开存各自排序，最后再合并即可（事实上如果直接存在一起排序也可以，但是排序函数比较麻烦）。

如果忘记怎么排序可以见[elainafan-从零开始的Python(2)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84python2/)。

```py
n = int(input())
age = []
nonage = []
for i in range(0, n):
    lst = input().split()
    x = lst[0]
    y = int(lst[1])
    if y >= 60:
        age.append([x, y, i])
    else:
        nonage.append([x, i])
age.sort(key=lambda x: (-x[1], x[2]))
nonage.sort(key=lambda x: x[1])
for i in range(0, len(age)):
    print(age[i][0])
for i in range(0, len(nonage)):
    print(nonage[i][0])
```

## 合影效果
### 描述
小云和朋友们去爬香山，为美丽的景色所陶醉，想合影留念。如果他们站成一排，男生全部在左（从拍照者的角度），并按照从矮到高的顺序从左到右排，女生全部在右，并按照从高到矮的顺序从左到右排，请问他们合影的效果是什么样的（所有人的身高都不同）？

### 输入
第一行是人数 $n(2 \leq n \leq 40)$ ，且至少有一个男生和一个女生。

后面紧跟 $n$ 行，每行输入一个人的性别（男male或女female）和身高（浮点数，单位米），两个数据之间以空格分隔。

```
6
male 1.72
male 1.78
female 1.61
male 1.65
female 1.70
female 1.56
```

### 输出
$n$ 个浮点数，模拟站好队后，拍照者眼中从左到右每个人的身高。每个浮点数需保留到小数点后2位，相邻两个数之间用单个空格隔开。

```
1.65 1.72 1.78 1.70 1.61 1.56
```

### Solution
还是读懂题目逻辑，将男生和女生分别排序，然后再合并即可。

```py
n = int(input())
man = []
woman = []
for i in range(0, n):
    lst = input().split()
    x = lst[0]
    y = float(lst[1])
    if x == "male":
        man.append(y)
    else:
        woman.append(y)
man.sort()
woman.sort(reverse=True)
for i in man:
    print(f"{i:.2f}", end=' ')
for i in woman:
    print(f"{i:.2f}", end=' ')

```

## 正整数的任意进制转换
将 $p$ 进制数 $n$ 转换为 q 进制。p 和 q 的取值范围为 $[2，36]$ ，其中，用到的数码按从小到大依次为：0，1，2，3，4，5，6，7，8，9，A，B，...，Z，不考虑小写字母。
### 输入
一共 $m+1$ 行。

第一行为 $m$ ，表示后面有 $m$ 行 $1 \leq m \leq 60$ 。

其后的 $m$行中，每行3个数: 进制 $p$ ， $p$ 进制数 $n$ ，以及进制 $q$ ，三个数之间用逗号间隔， $n$ 的长度不超过50位。  

```
6
18,2345678A123,18
15,23456,18
12,2345678,20
16,12345678,23
25,3456AB,21
18,AB1234567,22
```
### 输出
转换后的 $q$ 进制数。

```
2345678A123
114E0
22B7A4
21A976L
7C2136
22JF0G367
```
### Solution
这道题在计概中肯定都学过，所以这里不多讲具体的实现了，而且Python还不需要自己实现高精度。

一个Corner Case是 $n=0$ 时需要特判。

```py
n = int(input())
di = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'
]
dict = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    'M': 22,
    'N': 23,
    'O': 24,
    'P': 25,
    'Q': 26,
    'R': 27,
    'S': 28,
    'T': 29,
    'U': 30,
    'V': 31,
    'W': 32,
    'X': 33,
    'Y': 34,
    'Z': 35
}
for i in range(0, n):
    lst = input().split(',')
    p = int(lst[0])
    x = lst[1]
    q = int(lst[2])
    num = 0
    k = 1
    l = []
    t = x[::-1]
    for j in range(0, len(t)):
        num += k * dict[t[j]]
        k *= p
    if num == 0:
        print('0')
        continue
    while num > 0:
        temp = num % q
        l.append(di[temp])
        num //= q
    res = l[::-1]
    for j in res:
        print(j, end='')
    print()
```
## 古代密码
### 描述
古罗马帝国有一个拥有各种部门的强大政府组织。其中一个部门就是保密服务部门。为了保险起见，在省与省之间传递的重要文件中的大写字母是加密的。当时最流行的加密方法是替换和重新排列。

替换方法是将所有出现的字符替换成其它的字符。有些字符会替换成它自己。例如：替换规则可以是将'A' 到 'Y'替换成它的下一个字符，将'Z'替换成 'A'，如果原词是 "VICTORIOUS" 则它变成 "WJDUPSJPVT"。  

排列方法改变原来单词中字母的顺序。例如：将顺序例如将顺序 < 2 1 5 4 3 7 6 10 9 8 > 应用到 "VICTORIOUS" 上，则得到"IVOTCIRSUO"。  

人们很快意识到单独应用替换方法或排列方法加密，都是很不保险的。但是如果结合这两种方法，在当时就可以得到非常可靠的加密方法。所以，很多重要信息先使用替换方法加密，再将加密的结果用排列的方法加密。用两种方法结合就可以将"VICTORIOUS" 加密成"JWPUDJSTVP"。  

考古学家最近在一个石台上发现了一些信息。初看起来它们毫无意义，所以有人设想它们可能是用替换和排列的方法被加密了。人们试着解读了石台上的密码，现在他们想检查解读的是否正确。他们需要一个计算机程序来验证，你的任务就是写这个验证程序。  
### 输入
输入有两行。第一行是石台上的文字。文字中没有空格，并且只有大写英文字母。第二行是被解读出来的加密前的文字。第二行也是由大写英文字母构成的。

两行字符数目的长度都不超过100。

```
JWPUDJSTVP
VICTORIOUS
```
### 输出
如果第二行经过某种加密方法后可以产生第一行的信息，输出 "YES"，否则输出"NO"。

```
YES
```
### Solution
这题很有CF d2B的味道？直接贪心判断，如果第二个数组中不同字符及其每项的数量跟第一个数组中不同字符及其每项的数量相同，那么就能变，否则不能变。

```py
x = input()
y = input()
dict_1 = {}
dict_2 = {}
for i in range(0, len(x)):
    if x[i] not in dict_1:
        dict_1[x[i]] = 1
    else:
        dict_1[x[i]] += 1
for i in range(0, len(y)):
    if y[i] not in dict_2:
        dict_2[y[i]] = 1
    else:
        dict_2[y[i]] += 1
list_1 = []
list_2 = []
for i in dict_1.values():
    list_1.append(i)
for i in dict_2.values():
    list_2.append(i)
list_1.sort()
list_2.sort()
flag = 1
for i in range(0, max(len(list_1), len(list_2))):
    if list_1[i] == list_2[i]:
        continue
    else:
        flag = 0
        break
if flag == 0:
    print("NO")
else:
    print("YES")
```
## 啤酒厂选址
### 描述
海上有一个岛，在环海边上建有一条环岛高速公路，沿着公路有 $n(5 < n < 10000)$ 个居民点，假设每个居民点有一个编号，从0开始，按顺时针依次从小到大（即 $0,1,\ldots ,n-1$ ）编号。在岛上啤酒很受青睐。某啤酒企业计划在岛上投资建一个啤酒厂，并根据啤酒需求每天向居住点送啤酒。已知两个相邻的居民点的距离以及每个居住点每天的啤酒需求量（假设每个居住点每天不超过 $2000$ 桶）。假定每单位长度的路程送一桶啤酒需要的费用恒定（为单位费用）。请问，选择哪一个居民点建啤酒厂，才能使每天送啤酒的费用最小（空车不计费用）。
### 输入
第一行为居民点数目 $n$ 。 
后面为 $n$ 行，每行为一个居民点的啤酒需求量以及按顺时针离下一个居民点的距离（均为整数,空格间隔），从编号为0的开始，按单增顺次给出。  
注意：后面第 $n$ 行对应于居民点 $n-1$ 的啤酒需求量以及到编号为0的居民点距离。

```
6
500 10
300 30
350 25
400 60
700 28
200 35
```
## 输出
啤酒厂所在的居民点编号以及每天的运输费用，其间以逗号间隔

```
0,94100
```
### Solution
这道题在计概中出过一模一样的题目，时间复杂度为 $O(n^3)$ 肯定是过不去的，因此需要使用前缀和优化算法，使其为 $O(n^2)$ 。

也就是，通过前缀和存储距离，这样查询两点间的前缀和复杂度为 $O(1)$ ，再加上遍历点的时间复杂度 $O(n^2)$ ，就是 $O(n^2)$ 了。

至于剩下的做法想必不用多说，直接看代码吧~

```py
n = int(input())
d = [0]
l = 0
beer = []
ans = 1e8
mi = 0
for i in range(1, n + 1):
    lst = input().split()
    x = int(lst[0])
    y = int(lst[1])
    if (i != n):
        d.append(d[i - 1] + y)
    beer.append(x)
    l += y
for i in range(0, n):
    temp = 0
    for j in range(0, n):
        if i == j:
            continue
        else:
            temp += beer[j] * min(abs(d[j] - d[i]), l - abs(d[j] - d[i]))
    if temp < ans:
        mi = i
        ans = temp
print(mi, end=',')
print(ans)
```
## 玛雅历
### 描述
上周末，M.A. Ya教授对古老的玛雅有了一个重大发现。从一个古老的节绳（玛雅人用于记事的工具）中，教授发现玛雅人使用了一个一年有365天的叫做``Haab``的历法。这个Haab历法拥有 $19$ 个月，在开始的 $18$ 个月，一个月有 $20$ 天，月份的名字分别是pop, no, zip, zotz, tzec, xul, yoxkin, mol, chen, yax, zac, ceh, mac, kankin, muan, pax, koyab, cumhu。这些月份中的日期用0到19表示。Haab历的最后一个月叫做``uayet``，它只有 $5$ 天，用 $0$ 到 $4$ 表示。玛雅人认为这个日期最少的月份是不吉利的，在这个月法庭不开庭，人们不从事交易，甚至没有人打扫屋中的地板。

因为宗教的原因，玛雅人还使用了另一个历法，在这个历法中年被称为Tzolkin(holly年)，一年被分成``13``个不同的时期，每个时期有 $20$ 天，每一天用一个数字和一个单词相组合的形式来表示。使用的数字是 $1 \sim 13$ ，使用的单词共有 $20$ 个，它们分别是：imix, ik, akbal, kan, chicchan, cimi, manik, lamat, muluk, ok, chuen, eb, ben, ix, mem, cib, caban, eznab, canac, ahau。注意：年中的每一天都有着明确唯一的描述，比如，在一年的开始，日期如下描述： 1 imix, 2 ik, 3 akbal, 4 kan, 5 chicchan, 6 cimi, 7 manik, 8 lamat, 9 muluk, 10 ok, 11 chuen, 12 eb, 13 ben, 1 ix, 2 mem, 3 cib, 4 caban, 5 eznab, 6 canac, 7 ahau, ，8 imix, 9 ik, 10 akbal ……也就是说数字和单词各自独立循环使用。

Haab历和Tzolkin历中的年都用数字 $0,1,\ldots$ 表示，数字0表示世界的开始。所以第一天被表示成：

Haab: 0. pop 0

Tzolkin: 1 imix 0

请帮助M.A. Ya教授写一个程序可以把Haab历转化成Tzolkin历。

### 输入
Haab历中的数据由如下的方式表示：``日期. 月份 年数``

输入中的第一行表示要转化的Haab历日期的数据量。下面的每一行表示一个日期，年数小于5000。

```
3
10. zac 0
0. pop 0
10. zac 1995
```
### 输出
Tzolkin历中的数据由如下的方式表示：天数字 天名称 年数

第一行表示输出的日期数量。下面的每一行表示一个输入数据中对应的Tzolkin历中的日期。

```
3
3 chuen 0
1 imix 0
9 cimi 2801
```

### Solution
这里笔者要告诉同学们的是，日历型题目在Python(i)(II)部分的考察中，是最阴的一类题，赛时过题人数也非常少。因为它的本质就是大模拟，本题还算简单的，你将在[elainafan-从零开始的上机(10)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E4%B8%8A%E6%9C%BA10/)中见到更复杂的版本。

因为就是大模拟，笔者也没有什么好讲的，唯一要关注的就是最好赛时可以写注释提示自己各个变量的含义，以及注意取模，必要的时候自己构造Corner case。

```py
dict = {
    "pop": 1,
    "no": 2,
    "zip": 3,
    "zotz": 4,
    "tzec": 5,
    "xul": 6,
    "yoxkin": 7,
    "mol": 8,
    "chen": 9,
    "yax": 10,
    "zac": 11,
    "ceh": 12,
    "mac": 13,
    "kankin": 14,
    "muan": 15,
    "pax": 16,
    "koyab": 17,
    "cumhu": 18,
    "uayet": 19
}
day = [
    0, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    5
]
reday = [
    0, "imix", "ik", "akbal", "kan", "chicchan", "cimi", "manik", "lamat",
    "muluk", "ok", "chuen", "eb", "ben", "ix", "mem", "cib", "caban", "eznab",
    "canac", "ahau"
]
n = int(input())
print(n)
for i in range(0, n):
    tem = 0
    lst = input().split()
    x = lst[0]
    l = len(x)
    d = int(x[:(l - 1)])
    k = lst[1]
    z = lst[2]
    y = int(z)
    m = dict[k]
    tem += y * 365
    for j in range(1, m):
        tem += day[j]
    tem += d + 1
    if tem % 260 == 0:
        ry = tem // 260 - 1
        tem = 260
    else:
        ry = tem // 260
        tem %= 260
    temp = tem % 13
    if temp == 0:
        temp = 13
    rd = temp
    tt = tem % 20
    if tt == 0:
        tt = 20
    rm = reday[tt]
    print(rd, rm, ry)

```

## Minecraft
### 描述
Minecraft是一个几乎无所不能的沙盒游戏，玩家可以利用游戏内的各种资源进行创造，搭建自己的世界。  
在Minecraft中，基本的建筑元素是边长为1个单位的立方体，Tony想用 $N$ 个这种小立方体搭建一个长方体，并用他珍藏已久的贴纸对其进行装饰。如果一张贴纸可以贴满小立方体的一个面。那么，他需要用掉多少张贴纸呢？  
### 输入
一个整数 $N$ ，表示小明所拥有的小立方体的个数。N不会超过1000。

```
9
```
### 输出
一个整数，即小明最少用掉的贴纸有多少张。

```
30
```
### Solution
下面的代码是 $O(n^3)$ 的解法，也就是枚举 $n$ 的因数，但是经笔者试验如果没有三个维度的大小剪枝会被卡常而TLE。

需要注意的是，按理来说Python跑1e9，即本题中 $O(n^3)$ 的数据通常会超时，因此可能是时限标错了或者数据不够强。

另外，此题有 $O(1)$ 的做法，读者可以自己思考。

```py
n = int(input())
ans = 1e8
for i in range(1, n + 1):
    if i * i * i > n:
        break
    for j in range(i, n + 1):
        for k in range(j, n + 1):
            if n == i * j * k:
                ans = min(ans, 2 * (i * j + j * k + k * i))
print(ans)
```
## 猴子吃桃
### 描述
海滩上有一堆桃子， $N$ 只猴子来分。第一只猴子把这堆桃子平均分为 $N$ 份，多了一个，这只猴子把多的一个扔入海中，拿走了一份。第二只猴子接着把剩下的桃子平均分成N份，又多了一个，它同样把多的一个扔入海中，拿走了一份。第三、第四、……，第N只猴子仍是最终剩下的桃子分成N份，扔掉多了的一个，并拿走一份。

编写程序，输入猴子的数量 $N$ ，输出海滩上最少的桃子数，使得每只猴子都可吃到桃子。
### 输入
一个整数 $N$ 。

```
2
```
### 输出
输出当猴子数量为 $N$ 时海滩上最少的桃子数。结果保证在int型范围内。

```
7
```
### Solution
这道题是个经典的小学奥数题，但是不用担心，没学过也没关系。  

考虑朴素做法，直接枚举最后剩下的桃子数，然后根据指数级估算的时间复杂度，模拟猴子捡回桃子的过程，若中间出现捡到的桃子数量不是整数，就退出。

但是，显然地，这道题有 $O(1)$ 的做法，答案为 $n^n-(n-1)$ ，读者可以用递推自行证明，这也解释了枚举做法的正确性。

```py
n = int(input())
for i in range(1, 2147483647):
    ans = i * n + 1
    flag = 0
    for j in range(0, n - 1):
        if ans % (n - 1) == 0:
            ans = ans * n // (n - 1) + 1
            if j == n - 2:
                flag = 1
                break
            else:
                continue
        else:
            break
    if flag == 1:
        print(ans)
        break
```