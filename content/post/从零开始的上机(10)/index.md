---
title: 从零开始的上机(10)
date: 2025-06-08
categories:
    - 程序设计实习
---
## 质数的和与积
### 描述
两个质数的和是 $S$ ，它们的积最大是多少？

### 输入
一个不大于10000的正整数 $S$ ，为两个质数的和。

```
50
```

### Solution
一个整数，为两个质数的最大乘积。数据保证有解。

```
589
```

### Solution
签到题，直接枚举时间复杂度是够的，不需要用筛法预处理加上哈希表检索，时间复杂度为 $O(S \sqrt{S})$ 。

```py
def pd(x):
    if x == 1:
        return False
    elif x == 2 or x == 3:
        return True
    else:
        for i in range(2, x + 1):
            if i * i > x:
                return True
            if x % i == 0:
                return False
    return True


s = int(input())
ans = 0
for i in range(1, (s // 2) + 1):
    if pd(i) == True and pd(s - i) == True:
        ans = max(ans, i * (s - i))
print(ans)

```

## 最接近的分数
### 描述
分母不超过 $N$ 且小于 $\frac{A}{B}$ 的最大最简分数是多少？

### 输入
三个正整数 $N,A,B(1 \leq A < B < N \leq 1000) $ 相邻两个数之间用单个空格隔开。

```
100 7 13
```

### 输出
两个正整数，分别是所求分数的分子和分母，中间用单个空格隔开。

```
50 93
```

### Solution
注意，在``math``库中，是有最大公约数函数的。

然后看到这道题的数据范围， $O(n^2)$ 的时间复杂度完全没问题，因此遍历分子和分母判断即可。

```py
import math

lst = input().split()
n = int(lst[0])
a = int(lst[1])
b = int(lst[2])
te = 0
tem = 1
temp = 0
for i in range(1, n + 1):
    for j in range(1, i):

        if j / i < a / b and j / i > te / tem and math.gcd(i, j) == 1:
            te = j
            tem = i
print(te, end=' ')
print(tem)
```

## 谁是你的潜在朋友
### 描述
“臭味相投”——这是我们描述朋友时喜欢用的词汇。两个人是朋友通常意味着他们存在着许多共同的兴趣。然而作为一个宅男，你发现自己与他人相互了解的机会并不太多。幸运的是，你意外得到了一份北大图书馆的图书借阅记录，于是你挑灯熬夜地编程，想从中发现潜在的朋友。

首先你对借阅记录进行了一番整理，把 $N$ 个读者依次编号为 $1,2,\ldots,N$ ，把 $M$ 本书依次编号为 $1,2,\ldots,M$ 。同时，按照“臭味相投”的原则，和你喜欢读同一本书的人，就是你的潜在朋友。你现在的任务是从这份借阅记录中计算出每个人有几个潜在朋友。

### 输入
第一行两个整数 $N,M,2 \leq N,M \leq 200$ 。

接下来有 $N$ 行，第 $i(i = 1,2,\ldots,N)$ 行每一行有一个数，表示读者 $i-1$ 最喜欢的图书的编号 $P(1 \leq P \leq M)$ 。

```
4  5
2
3
2
1
```

### 输出
包括 $N$ 行，每行一个数，第 $i$ 行的数表示读者 $i$ 有几个潜在朋友。如果i和任何人都没有共同喜欢的书，则输出“BeiJu”（即悲剧，^ ^） 。

```
1
BeiJu
1
BeiJu
```

### Solution
直接先记录喜欢某本书的人数，然后逐一遍历人，如果他最喜欢的书只有一个人喜欢，那么就是悲剧。否则输出喜欢的人数减一即可。

```py
lst = input().split()
n = int(lst[0])
m = int(lst[1])
ans = [0] * (m + 1)
ma = [0] * (n + 1)
for i in range(1, n + 1):
    k = int(input())
    ma[i] = k
    ans[k] += 1
for i in range(1, n + 1):
    if ans[ma[i]] == 1:
        print("BeiJu")
    else:
        print(ans[ma[i]] - 1)
```

## 特殊日历计算
### 描述
有一种特殊的日历法，它的一天和我们现在用的日历法的一天是一样长的。它每天有10个小时，每个小时有100分钟，每分钟有100秒。10天算一周，10周算一个月，10个月算一年。现在要你编写一个程序，将我们常用的日历法的日期转换成这种特殊的日历表示法。这种日历法的时、分、秒是从0开始计数的。日、月从1开始计数，年从0开始计数。秒数为整数。假设 0:0:0 1.1.2000 等同于特殊日历法的 0:0:0 1.1.0。
### 输入
第一行是一个正整数 $N$ ,表明下面有 $N$ 组输入。每组输入有一行，格式如下：hour:minute:second day.month.year  。

表示常规的日期。日期总是合法的。$2000 \leq year \leq 50000$ 。
```
7
0:0:0 1.1.2000
10:10:10 1.3.2001
0:12:13 1.3.2400
23:59:59 31.12.2001
0:0:1 20.7.7478
0:20:20 21.7.7478
15:54:44 2.10.20749
```
### 输出
每组输入要求输出一行。格式如下：mhour:mmin:msec mday.mmonth.myear 是输入日期的特殊日历表示方法。

```
0:0:0 1.1.0
4:23:72 26.5.0
0:8:48 58.2.146
9:99:98 31.8.0
0:0:1 100.10.2000
0:14:12 1.1.2001
6:63:0 7.3.6848
```
### Solution
这道题就是之前说的日历类题目，因为调细节需要花很多时间，因此赛时通过率（做的人数）都很低。

这道题难在题意理解，感觉也没啥好讲的，一个比较好的思路是将日期和时间分成两个层次看待，这样方便debug。

同时，一个小技巧是，对于天数，可以适当举特例来找出需要特判的情况，从而完善程序。
```py
ddef pd(x):
    if x % 4 == 0 and x % 100 != 0:
        return True
    if x % 400 == 0:
        return True
    return False


n = int(input())
rc = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 30]
c = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 30]
for i in range(1, n + 1):
    lst = input().split()
    m = lst[0].split(':')
    l = lst[1].split('.')
    d = 0
    d += int(l[0]) - 1
    y = int(l[2])
    if pd(y):
        for j in range(1, int(l[1])):
            d += rc[j]
    else:
        for j in range(1, int(l[1])):
            d += c[j]
    tem = 0
    tem += (y - 2001) // 4 + (y - 2001) // 400 - (y - 2001) // 100 + 1
    if y == 2000:
        tem = 0
    d += (y - 2000 - tem) * 365 + tem * 366
    if d % 1000 == 0:
        year = d // 1000
        month = 1
        day = 1
    else:
        year = d // 1000
        if (d % 1000) % 100 == 0:
            month = (d % 1000) // 100 + 1
            day = 1
        else:
            month = (d % 1000) // 100 + 1
            day = d % 100 + 1
    temp = 0
    temp += int(m[0]) * 3600
    temp += int(m[1]) * 60
    temp += int(m[2])
    te = temp * 100000 // 86400
    hour = te // 10000
    minute = (te % 10000) // 100
    second = te % 100
    print(f"{hour}:{minute}:{second} {day}.{month}.{year}")
```
## 相关月
### 描述
“相关月”是指那些在一年中月份的第一天星期数相同的月份。例如，九月和十二月是相关的，因为九月一日和十二月一日的星期数总是相同的。两个月份相关，当且仅当两个月份第一天相差的天数能被7整除，也就是说，这两天相差为几个整星期。又如，二月和三月一般都是相关月，因为二月有28天，能被7整除，也恰好为4个星期。而在闰年，一月和二月的相关月与它们在平年的相关月是不同的，因为二月有29天，其后每个月份的第一天星期数都推后了一天。

### 输入
输入的第一行为整数 $n(n \leq 200）$ 。

其后 $n$ 行，每行三个整数，依次为一个年份和两个月份，整数之间用一个空格分隔。

```
5
1994 10 9
1935 12 1
1957 1 9
1917 9 12
1948 1 4
```
### 输出
输出有 $n$ 行，对应于每个输入的年份和相应两个月份，如果这两个月份是相关的，则输出YES，否则，输出NO。

```
NO
NO
NO
YES
YES
```
### Solution
赛时笔者直接用纸笔算出闰年和平年的相关月，然后直接条件判断，代码见下。

事实上读者可以直接记录每个月的月数，并在每次相加判断（或者使用前缀和），代码会比较短。

```py
def pd(x):
    if x % 4 == 0 and x % 100 != 0:
        return True
    elif x % 400 == 0:
        return True
    return False


n = int(input())
for i in range(1, n + 1):
    lst = input().split()
    y = int(lst[0])
    m1 = int(lst[1])
    m2 = int(lst[2])
    if m2 < m1:
        tem = m2
        m2 = m1
        m1 = tem
    if pd(y):
        if m1 == 1:
            if m2 == 4 or m2 == 7:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 2:
            if m2 == 8:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 3:
            if m2 == 11:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 4:
            if m2 == 7:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 9:
            if m2 == 12:
                print("YES")
            else:
                print("NO")
            continue
        else:
            print("NO")
    else:
        if m1 == 1:
            if m2 == 10:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 2:
            if m2 == 11 or m2 == 3:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 3:
            if m2 == 11:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 4:
            if m2 == 7:
                print("YES")
            else:
                print("NO")
            continue
        elif m1 == 9:
            if m2 == 12:
                print("YES")
            else:
                print("NO")
            continue
        else:
            print("NO")
```
## 更强的卷王查询系统
### 描述
古人云：“开卷有益”。但是，著名的社会学家小明认为内卷是有害的，并且他正在写一篇与P大内卷现状有关的论文，需要选取具有代表性的“卷王”们进行访谈。小明现在搞到了一份长长的成绩单，拜托你写个程序，帮他找出成绩单上的“卷王”们。

“卷王”的定义是：给定一组课程，这组课程全部上过的学生中，这组课程平均分最高的学生。小明已经通过复杂的数据挖掘手段得到了要分析的课程组，现在需要你按照上述定义，对每组课程找出那个真正的“卷王”。

### 输入
第 $1$ 行：一个整数 $n(1 \leq n \leq 100000)$ 。 

第 $2 \sim (n+1)$ 行：每行有用空格分隔的两个字符串和一个整数，前两个字符串分别代表课程名和学生名，最后一个整数代表这个学生在此课程中取得的成绩。输入保证课程名和学生名只包含字母，且一个学生在一个课程中不会出现两次成绩。输入保证课程数量不超过 $1000$ 门，且每门课的学生数量不超过 $100$ 人。输入不保证任何顺序。

第 $n+2$ 行：一个整数 $m(1 \leq m \leq 10)$ ，代表查询的个数，即课程组的组数。

接下来 $m$ 行：每行是一个课程组，第一个整数 $k(1 \leq k \leq 100)$代表该组课程的数量，后面有 $k$ 个字符串，表示 $k$ 个课程名。整数 $k$ 和字符串之间均用一个空格分隔。数据保证课程名一定在之前出现过。

```
22
JiSuanGaiLunA XiaoWang 100
JiSuanGaiLunA XiaoZhang 98
JiSuanGaiLunA XiaoHong 95
GaoDengShuXue XiaoHong 95
GaoDengShuXue XiaoZhang 84
GaoDengShuXue XiaoWang 82
GaoDengShuXue XiaoHuang 88
MeiRenLiJieJiSuanJiXiTong XiaoWang 82
MeiRenLiJieJiSuanJiXiTong XiaoZhang 84
MeiRenLiJieJiSuanJiXiTong XiaoHong 99
MeiRenLiJieJiSuanJiXiTong XiaoDuan 100
PythonCongRuMengDaoFangQi HYL 100
PythonCongRuMengDaoFangQi SWE 98
PythonCongRuMengDaoFangQi CDW 95
PythonCongRuMengDaoFangQi ASC 92
PythonCongRuMengDaoFangQi DEF 90
GuHanYu HYL 95
GuHanYu ASC 90
GuHanYu CDW 86
CollegeEnglish SWE 82
CollegeEnglish CDW 85
CollegeEnglish DEF 82
3
3 JiSuanGaiLunA GaoDengShuXue MeiRenLiJieJiSuanJiXiTong
2 PythonCongRuMengDaoFangQi GuHanYu
2 PythonCongRuMengDaoFangQi CollegeEnglish
```
### 输出
输出为 $m$ 行，每行对应一个课程组，输出该组课程平均分最高的学生，只考虑学过该组全部课程的学生。如果平均分最高的学生多于一个，输出姓名按英文词典排序最靠前的学生。数据保证对每组课程，都存在学过该组所有课程的学生。

```
XiaoHong
HYL
CDW
```
### Solution
重题，原题思路见[elainafan-从零开始的C++补充题(2)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E6%9C%9F%E4%B8%ADc-%E8%A1%A5%E5%85%85%E9%A2%982/#%E6%9B%B4%E5%BC%BA%E7%9A%84%E5%8D%B7%E7%8E%8B%E6%9F%A5%E8%AF%A2%E7%B3%BB%E7%BB%9F)，此处只需要翻译为Python即可。
```py
n = int(input())
dict = {}
name = []
dict_2 = {}
for i in range(1, n + 1):
    k = input().split()
    x = k[0]
    y = k[1]
    z = int(k[2])
    if y not in name:
        name.append(y)
    if y in dict:
        dict[y][x] = z
    else:
        dict[y] = {}
        dict[y][x] = z
m = int(input())
for i in range(1, m + 1):
    k = input().split()
    num = int(k[0])
    ma = 0
    res = []
    for j in name:
        temp = 0
        flag = 1
        for v in range(1, num + 1):
            if k[v] in dict[j].keys():
                temp += dict[j][k[v]]
            else:
                flag = 0
                break
        temp = temp / num
        if flag == 0:
            continue
        if temp > ma:
            ma = temp
            res.clear()
            res.append(j)
        elif temp == ma:
            res.append(j)
    res.sort()
    print(res[0])
```

## P大卷王查询系统
### 描述
古人云：“开卷有益”。但是，著名的社会学家小明认为内卷是有害的，并且他正在写一篇与P大内卷现状有关的论文，需要选取具有代表性的“卷王”们进行访谈。小明现在搞到了一份长长的成绩单，拜托你写个程序，帮他找出成绩单上的“卷王”们。

小明把“卷王”定义为：学过的课程数量大于等于 $x$ 门，且课程得分平均分大于 $y$ 的学生。

### 输入
第1行：三个用空格分隔的整数 $n,x,y,1 \leq n \leq 100000，x \geq 0，0 \leq y leq 100$ 。

第 $2 \sim (n+1)$ 行：每行有用空格分隔的两个字符串和一个整数，前两个字符串分别代表课程名和学生名，最后一个整数代表这个学生在此课程中取得的成绩。输入保证课程名和学生名只包含字母，且一个学生在一个课程中不会出现两次成绩。输入不保证任何顺序。

第 $n+2$ 行：一个整数 $m$ ，代表查询的个数，$1 \leq m \leq 1000$ 。

第 $(n+3) \sim (n+m+2)$ 行：每行是一个查询字符串，代表学生名，数据保证学生名一定在前面出现过。

```
7 3 90
JiSuanGaiLunA XiaoWang 100
JiSuanGaiLunA XiaoZhang 98
GaoDengShuXue XiaoHong 90
GaoDengShuXue XiaoWang 99
MeiRenLiJieJiSuanJiXiTong XiaoWang 93
PythonCongRuMengDaoFangQi XiaoHong 92
JiSuanGaiLunA XiaoHong 88
3
XiaoWang
XiaoHong
XiaoZhang
```

### 输出
输出为 $m$ 行，对于每个查询，如果这个学生是卷王，输出yes；如果不是卷王，输出no，注意，输出都是小写。

```
yes
no
no
```

### Solution
如你所见，这是一道nq题，也就是回应``q``个查询的题目。

但是这道题由于太过简单，完全不需要使用轮椅，呃，千万别让yiren看见这条。

回到原题，只需要维护每个学生学过课程数量和他的总分，用字典表示，然后查询时算一下就行，注意是平均分大于 $y$ ，且这里整除如果刚好向下取整等于 $y$ 但是有余数也算大于，不过Python有单整除可以避免这个（其实是笔者期中考同一道题被C++这里坑了，调了五分钟）。

```py
lst = input().split()
n = int(lst[0])
x = int(lst[1])
y = int(lst[2])
dict = {}
for i in range(1, n + 1):
    k = input().split()
    a = k[0]
    b = k[1]
    c = int(k[2])
    if b in dict:
        dict[b][1] += 1
        dict[b][0] += c
    else:
        dict[b] = [c, 1]
m = int(input())
for i in range(1, m + 1):
    k = input()
    if dict[k][1] >= x and dict[k][0] / dict[k][1] > y:
        print("yes")
    else:
        print("no")
```

## 扫雷
### 描述
不知道大家有没有玩过Windows上的扫雷游戏（也许已经变成时泪了QAQ）？

雷场可以用一个矩阵表示，为1的地方有地雷，为0的地方没地雷。

给定一个矩阵的位置，问该位置有没有地雷，若没有，则问它周围有几个地雷。周围指的是上、下、左、右、左上、左下、右上、右下八个位置。

### 输入
第 $1$ 行：雷场的行数 $r$ 和列数 $c(1 \leq r,c \leq 200)$ ，中间以空格分隔。

接下来 $r$ 行：每行 $c$ 个正整数，中间以空格分隔，0代表没有地雷，1代表有地雷。

接下来的1行：一个整数 $n(1 \leq n \leq 4000)$ ，代表要询问的位置个数。

接下来的 $n$ 行：两个用空格分隔的整数 $x$ 和 $y$ ，表示询问第 $x$ 行第 $y(0 \leq x,y \leq 199)$ 列的地雷情况，行数和列数都是从0开始计算。

```
5 6
0 0 1 0 1 1
1 0 0 1 0 1
1 1 0 0 1 1
1 0 0 0 0 1
0 0 1 1 0 0
5
0 0
2 1
1 4
3 4
0 3
```
### 输出
对每个询问的位置，输出一行。如果这个位置没有地雷，则输出一个整数，代表这个位置周围的地雷的个数；如果这个位置有地雷，则输出 BOOM!

```
1
BOOM!
6
4
3
```

### Solution
由于数据范围不大，因此直接模拟即可，每次询问遍历周围八个位置，对地雷进行计数，如果当前位置就有地雷，那么输出BOOM。

这里可以采用``1-based``，同时数组范围开成 $(r+2) \times (c+2)$ ，这样不需要检验数组是否越界。

```py
lst = input().split()
r = int(lst[0])
c = int(lst[1])
ma = [[0] * (c + 2) for _ in range(r + 2)]
for i in range(1, r + 1):
    k = input().split()
    for j in range(0, c):
        ma[i][j + 1] += int(k[j])
n = int(input())
for i in range(1, n + 1):
    k = input().split()
    x = int(k[0]) + 1
    y = int(k[1]) + 1
    temp = 0
    if ma[x][y] == 1:
        print("BOOM!")
        continue
    else:
        temp += ma[x - 1][y]
        temp += ma[x + 1][y]
        temp += ma[x][y - 1]
        temp += ma[x][y + 1]
        temp += ma[x - 1][y - 1]
        temp += ma[x - 1][y + 1]
        temp += ma[x + 1][y - 1]
        temp += ma[x + 1][y + 1]
        print(temp)
```

## 密码强度
### 描述
校内更新了刷卡机系统，为确保同学们的资金安全，要求设置具有一定强度的密码。符合要求的密码长度需要大于8，注意，是**大于**8，且必须包含特殊字符（"#"、"*"、或"&"）、字母和数字（字母既可以是大写字母也可以是小写字母）。现需要校验所输入的密码强度是否符合要求。

### 输入
为多行字符串，每行为一个密码。每个密码长度不超过25个字符。

```
asdff1234AZ
asdff123#Z
a#j
```
### 输出
对每个密码，强度符合要求输出“YES”，否则输出“NO”。

```
NO
YES
NO
```
### Solution
到了期末了，跟C++一样，由于比较少写不定组输入，所以格式容易忘记，需要注意。

其它就是直接遍历模拟，然后认真看题即可。

```py
while True:
    try:
        lst = input()
        flag1 = 0
        flag2 = 0
        flag3 = 0
        flag4 = 0
        if len(lst) > 8:
            flag3 = 1
        for i in range(0, len(lst)):
            if lst[i] == '#' or lst[i] == '*' or lst[i] == '&':
                flag1 = 1
            if lst[i] >= '0' and lst[i] <= '9':
                flag4 = 1
            if lst[i] >= 'a' and lst[i] <= 'z':
                flag2 = 1
            if lst[i] >= 'A' and lst[i] <= 'Z':
                flag2 = 1
        if flag1 == 1 and flag2 == 1 and flag3 == 1 and flag4 == 1:
            print("YES")
        else:
            print("NO")
    except EOFError:
        break
```
## 打印任意年份任意月份的日历
### 描述
给定公元year年month月，打印该月月历。

### 输入
第一行一个输入整数 $n$ ，表示有 $n$ 组数据。  
后面 $n$ 行，每行一组数据，是两个整数，分别代表 $year(0 < year \leq 100000)$ 和 $month(1 \leq month \leq 12)$ ，用空格隔开。

```
3
2019 12
403 5
23456 7
```
### 输出
对于每组数据：  

第一行输出月份（英文表示，首字母大写）和年份，用逗号隔开；  

第二行输出星期几， Sun Mon Tue Wed Thu Fri Sat，用``\t``隔开；  

接下来输出当月日期，日期用\t隔开，第一周缺天直接输出``\t``。（行与行之间无空行，每组数据之间无空行），行末多出来``\t``没有关系 。

12个月份的单词是： 

"January","February", "March", "April", "May", "June", "July", "August", "September", "October","November", "December"

```
December,2019
Sun	Mon	Tue	Wed	Thu	Fri	Sat
1 	2 	3 	4 	5 	6 	7 	
8 	9 	10 	11 	12 	13 	14 	
15 	16 	17 	18 	19 	20 	21 	
22 	23 	24 	25 	26 	27 	28 	
29 	30 	31 	
May,403
Sun	Mon	Tue	Wed	Thu	Fri	Sat
				1 	2 	3 	
4 	5 	6 	7 	8 	9 	10 	
11 	12 	13 	14 	15 	16 	17 	
18 	19 	20 	21 	22 	23 	24 	
25 	26 	27 	28 	29 	30 	31 	
July,23456
Sun	Mon	Tue	Wed	Thu	Fri	Sat
		1 	2 	3 	4 	5 	
6 	7 	8 	9 	10 	11 	12 	
13 	14 	15 	16 	17 	18 	19 	
20 	21 	22 	23 	24 	25 	26 	
27 	28 	29 	30 	31
```
### Solution 
跟上面的题目一样，还是日历类大模拟，没啥好讲的。

不过，一个小提醒是，对于公历题目，公元1年1月1日是星期几需要自己推，一般是星期六或者星期一，这道题是星期一，一般可以在完善框架后调整参数来匹配题目给定的样例。

还有，不要忘了打印每个数据完了之后的换行符。
```py
def pd(x):
    if x % 4 == 0 and x % 100 != 0:
        return True
    if x % 400 == 0:
        return True
    return False


n = int(input())
rc = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 30]
c = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 30]
name = [
    0, "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]
name_1 = [0, "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
for i in range(1, n + 1):
    lst = input().split()
    y = int(lst[0])
    m = int(lst[1])
    print(f"{name[m]},{y}")
    for j in range(1, 8):
        if j <= 6:
            print(name_1[j], end='\t')
        else:
            print(name_1[j])
    day = 0
    if pd(y):
        for j in range(1, m):
            day += rc[j]
        d = rc[m]
    else:
        for j in range(1, m):
            day += c[j]
        d = c[m]
    tem = (y - 1) // 4 + (y - 1) // 400 - (y - 1) // 100
    day += tem * 366 + (y - 1 - tem) * 365
    temp = (day + 1) % 7
    ma = temp % 7 + 1
    for j in range(1, ma):
        print('\t', end="")
    for j in range(1, d + 1):
        print(j, end='\t')
        if ma >= 7 and j != d:
            ma = 0
            print()
        ma += 1
    print()
```