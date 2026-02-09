---
title: 从零开始的上机(9)
date: 2025-05-25
categories:
    - 程序设计实习
---
本次上机内容：Python基础(I)(II)
## 寻找波峰
### 描述
小明在一条河上从西向东顺序测得 $n$ 个水位监测点的水位。如果一个监测点的水位比上一个和下一个监测点的水位都高，则称该监测点是一个波峰。最西边的监测点水位只要比下一个监测点高，就算波峰；最东边的监测点，水位只要比上一个监测点高，也算波峰。求波峰数目。

### 输入
第一行是整数 $n ( 2 \leq n \leq 100)$ ，表示监测点数目。

第二行有 $n$ 个整数，即从西向东 $n$ 个监测点的水位。

```
样例1：
5
8 12 7 3 6
样例2：
7
8 2 3 1 1 2 1
样例3:
5
1 2 3 3 2
样例4:
2
1 2
```

### 输出
一个整数，波峰数目。

```
样例1：
2
样例2：
3
样例3:
0
样例4:
1
```

### Solution
直接模拟即可，这里不多说了，注意可以在开头结尾都存一个0，这样不用特判边界。

```py
n = int(input())
ma = [0]
lst = input().split()
for i in range(0, n):
    ma.append(int(lst[i]))
ma.append(0)
ans = 0
for i in range(1, n + 1):
    if ma[i] > ma[i - 1] and ma[i] > ma[i + 1]:
        ans += 1
print(ans)
```

## 慈善晚宴排座次
### 描述
富豪们参加慈善晚宴，每个人都要捐款，首先按捐款数目从多到少排座次。 

在捐款数目相同的富豪中，名字首字母是'P'、'K'或 'U'的三大传统慈善家族人士，都会排在其它人前面。而捐款相同的传统慈善家族人士互相比较，以及非传统慈善家族人士互相比较时，谁先捐款谁就排在前面。

### 输入
第一行是整数 $n(0 < n < 100)$ , 表示富豪人数。

接下来 $n$ 行，每行有一个大写字母字符串和一个整数，分别代表一位富豪的名字和捐款数目。 

先出现的就是先捐款的。  

```
6
SS 10
AE 10
JACK 20
UDI 10
PBC 10
LNO 30
```
### 输出
按座次前后输出所有富豪名字及其捐款数目。每行一个富豪。

```
LNO 30
JACK 20
UDI 10
PBC 10
SS 10
AE 10
```
### 提示
如果sort的key参数写成一个lambda表达式不太容易，就专门写一个key函数，例如叫f。f返回一个构造出来的列表或元组，其中有元素能体现是不是属于三大家族

### Solution
首先，直接给名字首字母赋值权重为0，否则赋值为1，作为一个关键字，再存上一个关键字作为捐款次序，最后直接使用``lambda``表达式进行排序即可。

```py
n = int(input())
ma = []
for i in range(0, n):
    lst = input().split()
    id = i
    pd = 0
    k = lst[0]
    value = int(lst[1])
    if k[0] == 'P' or k[0] == 'K' or k[0] == 'U':
        pd = 1
    ma.append([k, value, pd, id])
ma.sort(key=lambda x: (-x[1], -x[2], x[3]))
for l in ma:
    print(l[0], end=' ')
    print(l[1])
```

## 捕鱼
### 描述
小明养了一池塘的鱼。捕鱼前小明会播放渔舟唱晚，那些鱼就听呆了动不了了。

鱼塘可以看作是一个方阵，分为 $n$ 行 $n$ 列共 $n \times n$ 个方格，有的方格里有鱼，有的没有。小明要撒网捕鱼，网也是一个方阵，撒下去可以覆盖 $m \times m$ 个方格，落在网里的鱼就被捕了。问小明一网最多能捕多少条鱼，以及有多少种放网的方法能捕这么多条鱼。请注意，小明下网时，网的左上角一定在鱼塘内，但是渔网可以有一部分落在鱼塘外面。

### 输入
第1行：两个整数，鱼塘边长 $n(5 \les n \les 10)$ 和渔网边长 $p (0 \leq p \leq 100)$ 。

接下来 $n$ 行：每行 $n$ 个整数，中间以空格分隔，表示鱼塘里每个方格的情况。0代表没有鱼，1代表有鱼。

```
6 3
0 0 0 0 1 0
0 0 0 1 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 1 0 0 0
0 1 0 0 0 0
```

### 输出
先输出一网能捕的最多鱼的数目，再输出有多少种放渔网的方法能捕到这么多鱼。

```
2 6
```

### Solution
枚举每次网的左上角并模拟即可，注意这道题可以初始化一个 $(n+m) \times (n+m) $ 的二维数组，以防止数组越界。

```py
k = input().split()
n = int(k[0])
m = int(k[1])
ans = 0
ret = 0
ma = [[0] * (n + m + 1) for _ in range(n + m + 1)]
for i in range(1, n + 1):
    t = input().split()
    for j in range(1, n + 1):
        ma[i][j] = int(t[j - 1])
for i in range(1, n + 1):
    for j in range(1, n + 1):
        temp = 0
        for k in range(i, i + m):
            for v in range(j, j + m):
                temp += ma[k][v]
        if temp == ans:
            ret += 1
        if temp > ans:
            ans = temp
            ret = 1
print(ans, end=' ')
print(ret)

```

## 访问的ip地址
### 描述
某网站统计了最近一段时间访问该网站的ip地址，但是由于意外，访问的记录被打乱了顺序。每一条访问记录包含三个信息：访问次序，访问ip地址，访问是否成功，保证输入数据每一条记录的访问次序均不相同。

请你统计这一段时间访问了该网站的所有ip地址，并统计每个ip地址的成功访问次数和失败访问次数。输出按照ip地址成功访问次数降序排序，成功访问次数相同的则按失败访问次数降序排序。如果两者均相同则按照每个ip地址的最初访问次序，早的在前，晚的在后。

### 输入
第一行是整数 $n( n \leq 10000)$ ，表示记录数量。 

下面 $n$ 行每行是一条ip地址访问记录，包括访问次序（最早的访问次序从1开始），访问的ip地址，是否成功访问（1为成功，0为失败），用空格隔开。

```
10
6 179.196.37.246 0
4 179.196.37.246 0
7 128.156.5.132 0
5 128.156.5.132 0
8 128.156.5.132 1
2 128.156.5.132 1
9 119.95.172.179 1
3 119.95.172.179 0
1 128.156.5.132 1
10 179.196.37.246 0
```
### 输出
多行排序后的结果，每一行包括：ip地址，成功访问的次数，访问失败的次数。

```
128.156.5.132 3 2
119.95.172.179 1 1
179.196.37.246 0 3
```
### Solution
首先，这里需要使用字典记录每个ip地址的成功访问次数和失败访问次数，同时需要记录它的最早访问时间，因此需要套一层列表。

然后注意，``dict.items()``函数返回的是一个列表，元素是一个元组，元组的第一个元素是键，第二个是值。

于是模拟即可。
```py
n = int(input())
dict = {}
for i in range(0, n):
    lst = input().split()
    x = int(lst[0])
    y = int(lst[2])
    if lst[1] not in dict:
        if y == 0:
            dict[lst[1]] = [0, 1, x]
        else:
            dict[lst[1]] = [1, 0, x]
    else:
        if y == 0:
            dict[lst[1]][1] += 1
        else:
            dict[lst[1]][0] += 1
        dict[lst[1]][2] = min(dict[lst[1]][2], x)
dict_2 = sorted(dict.items(), key=lambda x: (-x[1][0], -x[1][1], x[1][2]))
for l in dict_2:
    print(l[0], end=' ')
    print(l[1][0], end=' ')
    print(l[1][1])

```

## 损失评估
### 描述
危险品仓库发生爆炸，因为有安全防护机制，爆炸只会殃及其上下左右四个方向的临近区域，且不会发生连环爆炸。现在，由你对爆炸的损失作评估，你将获得一个 $N \times M$ 的矩阵，表示仓库的爆炸情况和每个区域危险品的价值。

### 输入
第一行为两个整数 $N$ 和 $M(2 \leq N,M \leq 100)$ ，表示仓库地图的行数和列数。

接下来 $N$ 行，每行为 $M$ 个以空格分隔的字符串，记录仓库各区域的爆炸情况和危险品的价值。每个字符串的格式为 “{爆炸情况}:{危险品价值}”。其中，爆炸情况'X'表示爆炸，'Y'表示未发生爆炸，':'是分隔符，危险品价值是一个整数。

```
3 4
X:10 Y:20 Y:30 Y:40
Y:50 X:60 X:70 Y:80
Y:90 Y:100 X:110 Y:120
```

### 输出
第一部分：分行输出每个爆炸点的位置和产生的损失（包含自身损失和殃及区域的损失，不必考虑殃及区域是否发生爆炸），格式为 “(i,j):{loss}” $(1 \leq i \leq N, 1 \leq j \leq M)$ ，表示第 $i$ 行，第 $j$ 列。请按爆炸点在地图中的顺序，从左到右，从上到下，依次输出即可。

第二部分：输出一个整数，表示爆炸造成的总损失(请注意爆炸殃及的区域可能存在重叠的情况，重叠区域的损失不要重复计算)。

### Solution
由于不会产生连续爆炸，因此可以直接存原图，然后枚举整个图，计算每个爆炸点的收益，并且对会被爆炸波及的点打上标记。

最后，再遍历整个图，计算会被爆炸波及的点和总收益即可。

```py
k = input().split()
n = int(k[0])
m = int(k[1])
ma = [[0] * (m + 2) for _ in range(n + 2)]
vis = [[0] * (m + 2) for _ in range(n + 2)]
pd = [[0] * (m + 2) for _ in range(n + 2)]
dx = [0, 1, -1, 0, 0]
dy = [0, 0, 0, 1, -1]
for i in range(1, n + 1):
    row = input().split()
    for j in range(1, m + 1):
        if row[j - 1][0] == 'X':
            vis[i][j] = 1
            pd[i][j] = 1
        ma[i][j] = int(row[j - 1][2:])
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if vis[i][j] == 1:
            temp = ma[i][j]
            for k in range(1, 5):
                ax = i + dx[k]
                ay = j + dy[k]
                if ax >= 1 and ax <= n and ay >= 1 and ay <= m:
                    temp += ma[ax][ay]
                    pd[ax][ay] = 1
            print(f"({i},{j}):{temp}")
ans = 0
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if pd[i][j] == 1:
            ans += ma[i][j]
print(ans)
```

## 逃出迷宫
### 描述
"Boom!" 小锅一觉醒来发现自己落入了一个 $N \times N(2 \leq N \leq 20)$ 的迷宫之中，为了逃出这座迷宫，小锅需要从左上角 $(0, 0)$ 处的入口跑到右下角 $(N-1, N-1)$ 处的出口逃出迷宫。由于小锅每一步都想缩短和出口之间的距离，所以他只会向右和向下走。假设我们知道迷宫的地图（以0代表通路，以1代表障碍），请你编写一个程序，判断小锅能否从入口跑到出口？

### 输入
第一行为一个整数 $N$ ，代表迷宫的大小。

接下来 $N$ 行为迷宫地图，迷宫地块之间以空格分隔。

输入保证 $(0, 0)$ 和 $(N - 1, N - 1)$ 处可以通过。

```
5
0 0 1 1 0
0 0 0 0 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
```
### 输出
一行字符串，如果能跑到出口则输出Yes，否则输出No

```
Yes
```
### Solution
相当于将C++的网格图DFS直接翻译为Python，注意审题是只能向右和向下走，其他不解释了。

```py
def dfs(x, y):
    global n, ma, vis, dx, dy, flag
    if x == n and y == n:
        flag = 1
        return
    for i in range(1, 3):
        ax = x + dx[i]
        ay = y + dy[i]
        if ax >= 1 and ay >= 1 and ax <= n and ay <= n and vis[ax][
                ay] == 0 and ma[ax][ay] == 0:
            vis[ax][ay] = 1
            dfs(ax, ay)
            vis[ax][ay] = 0


n = int(input())
ma = [[0] * (n + 1) for _ in range(n + 1)]
vis = [[0] * (n + 1) for _ in range(n + 1)]
dx = [0, 1, 0]
dy = [0, 0, 1]
for i in range(1, n + 1):
    lst = input().split()
    for j in range(1, n + 1):
        ma[i][j] = int(lst[j - 1])
vis[1][1] = 1
flag = 0
dfs(1, 1)
if flag == 1:
    print("Yes")
else:
    print("No")

```
## 学生排序
### 描述
有若干个学生的语数英考试成绩，要将这些学生排序。

首先按照总分从高到低排序。

如果总分相同，就按语文分数排；语文还相同，就按数学分数排，都是从高到低排。

如果三门课分数都一样，就按名字的英文词典顺序排。

如果名字也一样，就按学号的词典顺序排

### 输入
第1行是整数 $n ( n < 1000)$ ，表示有 $n$ 个学生。

接下来 $n$ 行，每行是一个学生的信息，格式为：

学号 姓名 语文分数 数学分数 英文分数

姓名由英文字母构成。学号是6个数字字符

```
10
210501 eve 90 95 100
212916 lime 89 105 86
210001 dave 100 90 95
211005 kane 75 80 90
212811 bob 75 95 81
210811 nell 85 90 95
211011 pawn 97 86 86
212107 tyler 99 85 86
212409 bobby 90 80 100
212111 sunny 97 86 92
```

### 输出
排号序后的排名和相应排名的学生的学号。每行一个学生。

```
1 210001
2 210501
3 212916
4 212111
5 212107
6 212409
7 210811
8 211011
9 212811
10 211005
```

### Solution
这道题还是考察``lambda``表达式的应用，存储一个列表，其中元素为列表，一维是总分，一维是语文分数，一维是数学分数，一维是名字，一维是学号，然后排就可以，不细讲了。

```cpp
n = int(input())
ans = []
for i in range(0, n):
    lst = input().split()
    a = int(lst[2])
    b = int(lst[3])
    c = int(lst[4])
    temp = a + b + c
    x = lst[0]
    y = lst[1]
    ans.append([temp, a, b, c, y, x])
ans.sort(key=lambda x: (-x[0], -x[1], -x[2], x[4], x[5]))
for i in range(0, n):
    print(i + 1, end=' ')
    print(ans[i][5])
```

## 垂直直方图
### 描述
输入4行全部由大写字母组成的文本，输出一个垂直直方图，给出每个字符出现的次数。注意：只用输出字符的出现次数，不用输出空白字符，数字或者标点符号的输出次数。
### 输入
输入包括4行由大写字母组成的文本，每行上字符的数目不超过80个。

```
THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG.
THIS IS AN EXAMPLE TO TEST FOR YOUR
HISTOGRAM PROGRAM.
HELLO!
```
### 输出
输出包括若干行。其中最后一行给出26个大写英文字母，这些字母之间用一个空格隔开。前面的几行包括空格和星号，每个字母出现几次，就在这个字母的上方输出一个星号。注意：输出的第一行不能是空行。

```
                            *
                            *
        *                   *
        *                   *     *   *
        *                   *     *   *
*       *     *             *     *   *
*       *     * *     * *   *     * * *
*       *   * * *     * *   * *   * * * *
*     * * * * * *     * * * * *   * * * *     * *
* * * * * * * * * * * * * * * * * * * * * * * * * *
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
```
### Solution
也许换成横着输出很多同学就会做了哈哈哈。

那么，竖着输出怎么做呢？可以先确定有多少行，也就是找到所有里面计数最多字母的数量，然后从上往下一个个减就可以了。

这里注意``ord``和``chr``函数的用法。

```py
lst = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
cnt = [0] * 26
for i in range(1, 5):
    k = input()
    for j in range(0, len(k)):
        if ord(k[j]) - ord('A') >= 0 and ord(k[j]) - ord('A') <= 25:
            cnt[ord(k[j]) - ord('A')] += 1
ans = 0
for i in range(0, 26):
    ans = max(ans, cnt[i])
for i in range(0, ans):
    for j in range(0, 26):
        if cnt[j] < ans:
            print(' ', end=' ')
        else:
            print('*', end=' ')
    print()
    ans -= 1
for i in range(0, 26):
    print(lst[i], end=' ')
```
## 垃圾炸弹
### 描述
2018年俄罗斯世界杯（2018 FIFA World Cup）开踢啦！为了方便球迷观看比赛，莫斯科街道上很多路口都放置了的直播大屏幕，但是人群散去后总会在这些路口留下一堆垃圾。为此俄罗斯政府决定动用一种最新发明——“垃圾炸弹”。这种“炸弹”利用最先进的量子物理技术，爆炸后产生的冲击波可以完全清除波及范围内的所有垃圾，并且不会产生任何其他不良影响。炸弹爆炸后冲击波是以正方形方式扩散的，炸弹威力（扩散距离）以 $d$ 给出，表示可以传播 $d$ 条街道。

假设莫斯科的布局为严格的1025*1025的网格状，由于财政问题市政府只买得起一枚“垃圾炸弹”，希望你帮他们找到合适的投放地点，使得一次清除的垃圾总量最多（假设垃圾数量可以用一个非负整数表示，并且除设置大屏幕的路口以外的地点没有垃圾）。
### 输入
第一行给出“炸弹”威力 $d(1 \leq d \leq 50)$ 。第二行给出一个数组 $n(1 \leq n \leq 20)$ 表示设置了大屏幕(有垃圾)的路口数目。接下来 $n$ 行每行给出三个数字 $x, y, i,$ 分别代表路口的坐标 $(x, y)$ 以及垃圾数量 $i$ . 点坐标 $(x, y)$ 保证是有效的（区间在0到1024之间），同一坐标只会给出一次。

```
1
2
4 4 10
6 6 20
```
### 输出
输出能清理垃圾最多的投放点数目，以及能够清除的垃圾总量。

```
1 30
```
### Solution
注意，Python考试一般不会考很难的算法，一般最难就到简单DFS，连DP都不会出现。

这道题，考虑直接遍历所有炸弹能放到的位置，然后遍历垃圾，计算这个炸弹能炸到多少垃圾即可，时间复杂度为 $O(1024^2 \cdot n)$ 。
```py
d = int(input())
n = int(input())
mx = []
my = []
ma = []
for i in range(0, n):
    k = input().split()
    mx.append(int(k[0]))
    my.append(int(k[1]))
    ma.append(int(k[2]))
ans = 0
ret = 0
for i in range(0, 1025):
    for j in range(0, 1025):
        temp = 0
        for k in range(0, n):
            if abs(mx[k] - i) <= d and abs(my[k] - j) <= d:
                temp += ma[k]
        if temp == ans:
            ret += 1
        if temp > ans:
            ret = 1
            ans = temp
print(ret, end=' ')
print(ans)
```
## 画家问题
### 描述
有一个正方形的墙，由 $N \times N$ 个正方形的砖组成，其中一些砖是白色的，另外一些砖是黄色的。Bob是个画家，想把全部的砖都涂成黄色。但他的画笔不好使。当他用画笔涂画第 $(i, j)$ 个位置的砖时， 位置 $(i-1, j),(i+1, j),(i, j-1),(i, j+1)$ 上的砖都会改变颜色。请你帮助Bob计算出最少需要涂画多少块砖，才能使所有砖的颜色都变成黄色。
### 输入
第一行是一个整数 $n (1 \leq n \leq 15)$ ，表示墙的大小。接下来的 $n$ 行表示墙的初始状态。每一行包含 $n$ 个字符。第 $i$ 行的第 $j$ 个字符表示位于位置 $(i,j)$ 上的砖的颜色。“w”表示白砖，“y”表示黄砖。

```
5
wwwww
wwwww
wwwww
wwwww
wwwww
```
### 输出
一行，如果Bob能够将所有的砖都涂成黄色，则输出最少需要涂画的砖数，否则输出“inf”。

```
15 
```
### Solution
事实上最后ZQJ老师班最后只有五个同学赛时做了这道题，而且都AC了。

这道题其实算是一个搜索题，但是注意这个数据范围 $1 \leq n \leq 15$ ，是非常经典的状压问题。

先不考虑状压，需要注意到一个事实，就是下一行的状态是由上一行确定的（想一想为什么？）。

那么，只要第一行的状态确定，那么一直到最后一行的状态都确定了，所以只需要进行DFS并确定最后一行是否满足条件，并计数更新次数。

怎么枚举第一行的状态？由于每个点有两种情况，因此整个状态集合有 $2^{n}$ 种情况，将每个点看成一个二进制数的位，于是状态可以表示为 $0 \sim 2^{n}-1$ ，枚举即可。

最后，需要注意一下Corner Case，也就是 $n=1$ 的情况。
```py
def dfs(x):
    global n,ma,pa,dx,dy,mi,tem,flag
    for i in range(1,n+1):
        if pa[x-1][i]==0:
            pa[x][i]=(pa[x][i]+1)%2
            tem+=1
            for k in range(1,5):
                ax=x+dx[k]
                ay=i+dy[k]
                if ax>=1 and ay>=1 and ax<=n and ay<=n:
                    pa[ax][ay]=(pa[ax][ay]+1)%2
    if x!=n:
        dfs(x+1) 
    if x==n:
        f=0
        for i in range(1,n+1):
            if pa[n][i]==0:
                return 
        if tem<mi:
            mi=tem
        flag=1
        return 
    return 
    
n=int(input())
ma=[[]]
pa=[[]]
dx=[0,1,-1,0,0]
dy=[0,0,0,1,-1]
mi=9999
tem=0
for i in range(0,n):
    ma.append([0])
    pa.append([0])
for i in range(1,n+1):
    k=input()
    for j in range(0,n):
        if k[j]=='w':
            ma[i].append(0)
        else:
            ma[i].append(1)
        pa[i].append(0)
for i in range(1,n+1):
    for j in range(1,n+1):
        pa[i][j]=ma[i][j]
if n==1:
    if ma[1][1]==0:
        print(1)
    else:
        print(0)
else:
    flag=0
    for i in range(0,1<<n):
        temp=i
        tem=0
        for j in range(1,n+1):
            if ((temp>>(j-1))&1)==1:
                tem+=1
                pa[1][j]=(pa[1][j]+1)%2
                for k in range(1,5):
                    ax=1+dx[k]
                    ay=j+dy[k]
                    if ax>=1 and ax<=n and ay>=1 and ay<=n:
                        pa[ax][ay]=(pa[ax][ay]+1)%2
        dfs(2)
        for j in range(1,n+1):
            for k in range(1,n+1):
                pa[j][k]=ma[j][k]
    if flag==0:
        print("inf")
    else:
        print(mi)
```