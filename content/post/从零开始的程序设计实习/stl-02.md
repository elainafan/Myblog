---
title: 从零开始的STL(2)
date: 2025-04-23
categories:
    - 程序设计实习
slug: 从零开始的stl2
hidden: true
seriesOrder: 17
---
## List
### 描述
写一个程序完成以下命令：  

new id ——新建一个指定编号为 $id(id < 10000) $ 的序列。

add id num——向编号为 $id$ 的序列加入整数 $num$ 。  

num merge id1 id2——如果 $id_1$ 等于 $id_2$ ，不做任何事，否则归并序列 $id_1$ 和 $id_2$ 中的数，并将 $id_2$ 清空。

unique id——去掉序列 $id$ 中重复的元素。

out id ——从小到大输出编号为 $id$ 的序列中的元素，以空格隔开。
### 输入
第一行一个数 $n(n \leq 200000)$ ，表示有多少个命令。以后 $n$ 行每行一个命令。

```
16
new 1
new 2
add 1 1
add 1 2
add 1 3
add 2 1
add 2 2
add 2 3
add 2 4
out 1
out 2
merge 1 2
out 1
out 2
unique 1
out 1
```
### 输出
按题目要求输出。

```
1 2 3 
1 2 3 4
1 1 2 2 3 3 4

1 2 3 4
```
### Solution
其实题目没有强求你用题干的数据结构，但是这题还是用list（双向链表），虽然用multimap或者multiset也可以的。

那题目中的指令就变为:  

``new``，其实也没啥用。  

``add``，就是push_back。 

``merge``，就是merge。  

``unique``就是先sort后unique（因为便于删除，跟某个称作离散化的trick是一样的）。

``out``，就是用迭代器输出，使用更方便的auto关键字而不是iterator。  

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define maxn 200005
using namespace std;
int n;
list<int> ma[maxn];
string s;
int id, num;
int main() {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        cin >> s;
        if (s[0] == 'n') {
            cin >> id;
        } else if (s[0] == 'a') {
            cin >> id >> num;
            ma[id].push_back(num);
        } else if (s[0] == 'm') {
            cin >> id >> num;
            if (id == num)
                continue;
            else {
                ma[id].merge(ma[num]);
            }
        } else if (s[0] == 'u') {
            cin >> id;
            ma[id].sort();
            ma[id].unique();
        } else if (s[0] == 'o') {
            cin >> id;
            if (ma[id].empty())
                cout << endl;
            else {
                ma[id].sort();
                for (auto i = ma[id].begin(); i != ma[id].end(); i++) {
                    cout << *i << ' ';
                }
                cout << endl;
            }
        }
    }
    system("pause");
    return 0;
}
```
## RPN Calculator
### 描述
逆波兰表示法（或简称 RPN），与相关的波兰表示法类似，波兰表示法是波兰数学家扬・武卡谢维奇（Jan Łukasiewicz）于 1920 年引入的一种前缀表示法。逆波兰表示法是一种数学表示法，其中每个运算符都紧跟在其所有操作数之后。它也被称为后缀表示法。  

在逆波兰表示法中，运算符紧跟在操作数之后；例如，要计算 3 加 4 ，应写成 “3 4 +”，而不是 “3 + 4”。如果有多个运算，运算符会紧跟在第二个操作数之后；所以常规中缀表示法下写成 “3 - 4 + 5” 的表达式，在逆波兰表示法中应写成 “3 4 - 5 +” ：先计算 3 减 4 ，然后再加上 5。逆波兰表示法的一个优点是它无需中缀表示法中所需的括号。“3 - 4 * 5” 也可以写成 “3 - (4 * 5)” ，但这与 “(3 - 4) * 5” 的含义截然不同，只有括号能区分这两种不同的含义。在后缀表示法中，前者应写成 “3 4 5 * -” ，它明确表示 “3 (4 5 *) -” 。

你需要设计一个简单的逆波兰表示法计算器，该计算器需支持 “+”、“-”、“*”、“/”（除数的绝对值不小于 $10^{-9}$ ）和 “^”（幂运算符，若底数 $b \leq 0$ ，指数 $e$ 必须是不大于 $10^9$ 的正整数 ）运算符。可以假设计算过程中的所有数字都可以用双精度浮点数表示。  

此外，我们的计算器有一定的内存。每次计算一个表达式时，内存中最小的数字将被删除，并替换为该表达式的值。  
### 输入
第一行包含一个整数 $n$ ，它是我们计算器的内存大小。  

从第二行开始，将给出 $n$ 个数字，这些是内存的初始值。除最后一行外，每行将有 $10$ 个数字。  

然后每行是一个有效的逆波兰表示法表达式，以 “=” 结尾，“=” 是计算命令。每个项的长度不超过 $20$ 个字符。

```
4
1e6 1e-6 0.001 1000
1 2 + 3 4 + * =
1 0.1 / 8 ^ =
```
### 输出
对于每个表达式，在一行中输出其值。

然后输出一个空行，将两部分内容分隔开。 

最后，按升序输出内存中的所有数字，每行 10 个数字。  

每个数字应采用科学计数法格式，保留 $6$ 位小数，指数部分占 $2$ 位，类似于 C 语言中 printf () 函数的 “% e” 格式字符串。一行中的数字之间用空格分隔。  

```
2.100000e+01
1.000000e+08

2.100000e+01 1.000000e+03 1.000000e+06 1.000000e+08
```
### 提示
输入量较大，建议使用``scanf``或者`` cin.tie(nullptr)->sync_with_stdio(false);``

%e格式输出在windows环境下指数部分为3位，在系统的测试环境下为2位。

### Solution
恼人的大模拟题目，首先介绍一下逆波兰表达式的求法吧，这个在数算中也会学到。

依次顺序读入表达式的符号序列（假设等号是结尾），并根据读入的元素符号逐一分析。

当遇到的是一个操作数，则压入栈顶。

当遇到的是一个运算符，就从栈中两次取出栈顶，按照运算符对这两个操作数进行计算。然后将计算结果压入栈顶。

如此往复，直到遇到等号，此时栈顶的值就是后缀表达式的值。

然后模拟内存，可以用``multiset``来模拟内存，最后输出就行了。

注意这里的``atof(x.c_str())``，``c_str()``指的是将``string``类型变量``x``转换成``char*``类型变量，``atof()``表示将``char*``型变量转换成双精度浮点数。

同时，``cin``碰到空格跟换行会自动断，这很方便解析表达式。

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
int n;
int main() {
    cin >> n;
    stack<double> ma;
    multiset<double> res;
    for (int i = 1; i <= n; i++) {
        double x;
        cin >> x;
        res.insert(x);
    }
    string x;
    while (cin >> x) {
        if (x == "=") {
            double s = ma.top();
            printf("%e\n", s);
            ma.pop();
            auto it = res.begin();
            res.erase(it);
            res.insert(s);
        } else if (x == "+" || x == "-" || x == "*" || x == "/" || x == "^") {
            double a, b, c;
            a = ma.top();
            ma.pop();
            b = ma.top();
            ma.pop();
            if (x == "+") {
                c = a + b;
            } else if (x == "-") {
                c = b - a;
            } else if (x == "*") {
                c = a * b;
            } else if (x == "/") {
                c = b / a;
            } else {
                c = pow(b, a);
            }
            ma.push(c);
        } else {
            double num;
            num = atof(x.c_str());
            ma.push(num);
        }
    }
    cout << endl;
    int count = 0;
    for (auto it = res.begin(); it != res.end(); it++) {
        count++;
        if (count % 10 == 0) {
            printf("%e\n", *it);
        } else {
            printf("%e ", *it);
        }
    }
    system("pause");
    return 0;
}
```
## Set
### 描述
现有一整数集（允许有重复元素），初始为空。我们定义如下操作：

add x 把 $x$ 加入集合。  

del x 把集合中所有与 $x$ 相等的元素删除。 

ask x 对集合中元素 $x$ 的情况询问 。

对每种操作，我们要求进行如下输出。  

add 输出操作后集合中x的个数  

del 输出操作前集合中x的个数  

ask 先输出0或1表示x是否曾被加入集合（0表示不曾加入），再输出当前集合中x的个数，中间用空格分隔。  

### 输入
第一行是一个整数 $n$ ，表示命令数。 $0 \leq n \leq 100000$ 。

后面 $n$ 行命令，如描述中所述。

```
7
add 1
add 1
ask 1
ask 2
del 2
del 1
ask 1
```
### 输出
共 $n$ 行，每行按要求输出。

```
1
2
1 2
0 0
0
2
1 0
```
### Solution
由于题目中需要记录重复元素的数量，所以用``map``更加合适，这样可以记录所有被插入过的元素的数量。

然后，用一个``map``或者``set``记录所有被加入过集合的元素。

于是操作转变为：

``add``：``ma``中的元素加一，``ma2``中元素加一。

``del``：若``ma``中有当前元素，则输出数量并删除，若没有则输出0。

``ask``：若``ma2``中有当前元素，则输出``ma``中当前元素数量，反之输出0。

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n;
map<int, int> ma;
map<int, int> ma2;
string s;
int x;
int main() {
    cin.tie(nullptr)->sync_with_stdio(false);
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> s >> x;
        if (s[1] == 'd') {
            ma[x]++;
            ma2[x]++;
            cout << ma[x] << endl;
        } else if (s[1] == 'e') {
            if (ma.count(x)) {
                cout << ma[x] << endl;
                ma.erase(ma.find(x));
            } else
                cout << 0 << endl;
        } else {
            if (ma2.count(x)) {
                cout << 1 << ' ';
                if (ma.count(x))
                    cout << ma[x] << endl;
                else
                    cout << 0 << endl;
            } else
                cout << 0 << endl;
        }
    }
    system("pause");
    return 0;
}
```
## 字符串操作
### 描述
给定 $n$ 个字符串（从1开始编号），每个字符串中的字符位置从0开始编号，长度为1-500，现有如下若干操作：

copy N X L：取出第 $N$ 个字符串第 $X$ 个字符开始的长度为 $L$ 的字符串。  

add S1 S2：判断 $S_1,S_2$ 是否为 $0 \sim 99999$ 之间的整数，若是则将其转化为整数做加法，若不是，则作字符串加法，返回的值为一字符串。 

find S N：在第 $N$ 个字符串中从左开始找寻 $S$ 字符串，返回其第一次出现的位置，若没有找到，返回字符串的长度。  

rfind S N：在第 $N$ 个字符串中从右开始找寻 $S$ 字符串，返回其第一次出现的位置，若没有找到，返回字符串的长度。  

insert S N X：在第 $N$ 个字符串的第 $X$ 个字符位置中插入 $S$ 字符串。  
reset S N：将第 $N$ 个字符串变为 $S$ 。  

print N：打印输出第 $N$ 个字符串。  

printall：打印输出所有字符串
。  
over：结束操作。  

其中 $N，X，L$ 可由find与rfind操作表达式构成， $S，S1，S2$ 可由copy与add操作表达式构成。

### 输入
第一行为一个整数 $n(1 \leq n \leq 20)$ 。

接下来 $n$ 行为 $n$ 个字符串，字符串不包含空格及操作命令等。

接下来若干行为一系列操作，直到over结束。

```
3
329strjvc
Opadfk48
Ifjoqwoqejr
insert copy 1 find 2 1 2 2 2
print 2
reset add copy 1 find 3 1 3 copy 2 find 2 2 2 3
print 3
insert a 3 2
printall
over
```

### 输出
根据操作提示输出对应字符串。

```
Op29adfk48
358
329strjvc
Op29adfk48
35a8
```
### 提示
推荐使用string类中的相关操作函数。
### Solution
这是一道大模拟题，重点在于处理嵌套的指令。题目指出 $N, X, L$ 等参数可能是 `find` 或 `rfind` 的表达式，而 $S$ 可能是 `copy` 或 `add` 的表达式。这种定义方式提示我们需要使用递归的思想。

可以为每一个命令（`copy`, `add`, `find`, `rfind`, `insert`, `reset`, `print`）编写对应的处理函数。在读取参数时，先以字符串形式读入。如果读到的是嵌套命令的关键字（如 "copy", "find"），则递归调用相应的函数来获取返回值；否则，直接解析为数值或字符串。

利用 C++ 的 `std::string` 类及其成员函数（如 `substr`, `find`, `rfind`, `insert`），配合 `<string>` 库中的 `stoi` 和 `to_string`，可以大大简化实现的复杂度。`cin` 能够自动跳过空白字符，非常适合处理这里的指令流。

对于 `add` 指令，需要检查两个操作数是否为 $0 \sim 99999$ 之间的整数。可以通过检查字符串长度和每一位字符是否为数字来实现。

上述内容来自Gemini，笔者看这题实在燃尽了。
```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
#define maxn 25
using namespace std;
string Copy();
string Add();
bool isnum(string x);
int Find();
int Rfind();
string Insert();
string Reset();
void Print(int x);
void Printall();
int n0;
string str[maxn];
int tot;
string Copy() {
    string N, X, L;
    int n, x, l;
    cin >> N;
    if (N == "find") {
        n = Find();
    } else if (N == "rfind") {
        n = Rfind();
    } else
        n = stoi(N);
    cin >> X;
    if (X == "find") {
        x = Find();
    } else if (X == "rfind") {
        x = Rfind();
    } else
        x = stoi(X);
    cin >> L;
    if (L == "find") {
        l = Find();
    } else if (L == "rfind") {
        l = Rfind();
    } else
        l = stoi(L);
    string temp = str[n].substr(x, l);
    return temp;
}
string Add() {
    string S1, S2, s1, s2;
    cin >> S1;
    if (S1 == "copy") {
        s1 = Copy();
    } else if (S1 == "add") {
        s1 = Add();
    } else
        s1 = S1;
    cin >> S2;
    if (S2 == "copy") {
        s2 = Copy();
    } else if (S2 == "add") {
        s2 = Add();
    } else
        s2 = S2;
    if (isnum(s1) && isnum(s2)) {
        int a = stoi(s1), b = stoi(s2);
        return to_string(a + b);
    } else
        return s1 + s2;
}
bool isnum(string x) {
    int l = x.length();
    if (l >= 5) return false;
    bool flag = true;
    for (int i = 0; i <= l - 1; i++) {
        if (!(x[i] >= '0' && x[i] <= '9')) {
            flag = false;
            break;
        }
    }
    return flag;
}
int Find() {
    string S, N, s;
    int n;
    cin >> S;
    if (S == "copy") {
        s = Copy();
    } else if (S == "add") {
        s = Add();
    } else
        s = S;
    cin >> N;
    if (N == "find") {
        n = Find();
    } else if (N == "rfind") {
        n = Rfind();
    } else
        n = stoi(N);
    int temp;
    if (str[n].find(s) != string::npos) {
        temp = str[n].find(s);
    } else
        temp = str[n].size();
    return temp;
}
int Rfind() {
    string S, s, N;
    int n;
    cin >> S;
    if (S == "copy") {
        s = Copy();
    } else if (S == "add") {
        s = Add();
    } else
        s = S;
    cin >> N;
    if (N == "find") {
        n = Find();
    } else if (N == "rfind") {
        n = Rfind();
    } else
        n = stoi(N);
    int temp;
    if (str[n].rfind(s) != string::npos) {
        temp = str[n].rfind(s);
    } else
        temp = str[n].size();
    return temp;
}
string Insert() {
    string N, X, S, s;
    int n, x;
    cin >> S;
    if (S == "copy") {
        s = Copy();
    } else if (S == "add") {
        s = Add();
    } else
        s = S;
    cin >> N;
    if (N == "find") {
        n = Find();
    } else if (N == "rfind") {
        n = Rfind();
    } else {
        n = stoi(N);
    }
    cin >> X;
    if (X == "find") {
        x = Find();
    } else if (X == "rfind") {
        x = Rfind();
    } else
        x = stoi(X);
    string temp = str[n].insert(x, s);
    return temp;
}
string Reset() {
    string S, s, N;
    int n;
    cin >> S;
    if (S == "copy") {
        s = Copy();
    } else if (S == "add") {
        s = Add();
    } else
        s = S;
    cin >> N;
    if (N == "find") {
        n = Find();
    } else if (N == "rfind") {
        n = Rfind();
    } else
        n = stoi(N);
    swap(str[n], s);
    return str[n];
}
void Print(int x) {
    cout << str[x] << endl;
    return;
}
void Printall() {
    for (int i = 1; i <= n0; i++) {
        cout << str[i] << endl;
    }
    return;
}
int main() {
    cin >> n0;
    for (int i = 1; i <= n0; i++) {
        cin >> str[i];
    }
    while (1) {
        string op;
        cin >> op;
        if (op == "over")
            break;
        else if (op == "copy") {
            Copy();
        } else if (op == "add") {
            Add();
        } else if (op == "find") {
            Find();
        } else if (op == "rfind") {
            Rfind();
        } else if (op == "insert") {
            Insert();
        } else if (op == "reset") {
            Reset();
        } else if (op == "print") {
            int x;
            cin >> x;
            Print(x);
        } else if (op == "printall") {
            Printall();
        }
    }
    system("pause");
    return 0;
}
```
## 热血格斗场
### 描述
为了迎接08年的奥运会，让大家更加了解各种格斗运动，facer新开了一家热血格斗场。格斗场实行会员制，但是新来的会员不需要交入会费，而只要同一名老会员打一场表演赛，证明自己的实力。

我们假设格斗的实力可以用一个正整数表示，成为实力值。另外，每个人都有一个唯一的 $id$ ，也是一个正整数。为了使得比赛更好看，每一个新队员都会选择与他实力最为接近的人比赛，即比赛双方的实力值之差的绝对值越小越好，如果有两个人的实力值与他差别相同，则他会选择比他弱的那个（显然，虐人必被虐好）。

不幸的是，Facer一不小心把比赛记录弄丢了，但是他还保留着会员的注册记录。现在请你帮facer恢复比赛纪录，按照时间顺序依次输出每场比赛双方的 $id$ 。

### 输入
第一行一个数 $n(0 < n \leq 100000)$ ，表示格斗场新来的会员数（不包括facer）。

以后 $n$ 行每一行两个数，按照入会的时间给出会员的id和实力值。一开始，facer就是会员，id为1，实力值1000000000。输入保证两人的实力值不同。

```
3
2 1
3 3
4 2
```

### 输出
$N$ 行，每行两个数，为每场比赛双方的id，新手的id写在前面。

```
2 1
3 2
4 2
```
### Solution
本题要求插入后找出相邻人并进行比赛，那么可以采用``multimap``，其实用``multiset``也可以。

也就是，每次插入后的迭代器获取后，判一下边界，比较一下两边的人的power，直接输出id就可以了，这题不难。

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n;
int id, p;
multimap<int, int> lst;
int main() {
    scanf("%d", &n);
    lst.insert(make_pair(1000000000, 1));
    for (int i = 1; i <= n; i++) {
        cin >> id >> p;
        auto it = lst.insert(make_pair(p, id));
        cout << id << ' ';
        if (it != lst.begin() && it != --lst.end()) {
            auto it_1 = it;
            auto it_2 = it;
            it_1--;
            it_2++;
            if (abs(it_1->first - p) <= abs(it_2->first - p)) {
                cout << it_1->second << endl;
            } else
                cout << it_2->second << endl;
        } else if (it == lst.begin()) {
            cout << (++it)->second << endl;
        } else if (it == --lst.end()) {
            cout << (--it)->second << endl;
        }
    }
    system("pause");
    return 0;
}
```
## 冷血格斗场
### 描述
为了迎接08年的奥运会，让大家更加了解各种格斗运动，facer新开了一家冷血格斗场。格斗场实行会员制，但是新来的会员不需要交入会费，而只要同一名老会员打一场表演赛，证明自己的实力。

我们假设格斗的实力可以用一个``非负整数``表示，称为实力值，两人的实力值可以相同。另外，每个人都有一个唯一的id，也是一个正整数。为了使得比赛更好看，每一个新队员都会选择与他实力最为接近的人比赛，即比赛双方的实力值之差的绝对值越小越好，如果有多个人的实力值与他差别相同，则他会选择id最小的那个。

不幸的是，Facer一不小心把比赛记录弄丢了，但是他还保留着会员的注册记录。现在请你帮facer恢复比赛纪录，按照时间顺序依次输出每场比赛双方的id。

### 输入
第一行一个数 $n(0 < n \leq 100000)$，表示格斗场新来的会员数（不包括facer）。

以后 $n$ 行每一行两个数，按照入会的时间给出会员的id和实力值。一开始，facer就算是会员，id为1，实力值1000000000。

```
3
2 3
3 1
4 2
```

### 输出
N行，每行两个数，为每场比赛双方的id，新手的id写在前面。

```
2 1
3 2
4 2
```
### Solution
本题的不同点在于，如果有多个人的实力值和他相同，那么，它会选择id最小的那个。

可以转化为，对于后输入的，如果power相同且后输入的id比前面的小，那么前面输入的id就没有意义了，因为后续也不会找到它。

所以，只需维护一个map，因为在上述说法下不会存在冲突。

剩下的部分跟上一题差不多，同样需要注意边界的判断~

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n, id, p;
map<int, int> ma;
int main() {
    scanf("%d", &n);
    ma[1000000000] = 1;
    for (int i = 1; i <= n; i++) {
        cin >> id >> p;
        cout << id << ' ';
        auto it = ma.find(p);
        if (it != ma.end()) {
            cout << ma[p] << endl;
            ma[p] = min(id, ma[p]);
            continue;
        } else
            ma[p] = id;
        it = ma.find(p);
        if (it != ma.begin() && it != --ma.end()) {
            auto it_1 = it;
            auto it_2 = it;
            it_1--;
            it_2++;
            if (abs(it_1->first - p) < abs(it_2->first - p)) {
                cout << it_1->second << endl;
            } else if (abs(it_1->first - p) == abs(it_2->first - p)) {
                cout << min(it_1->second, it_2->second) << endl;
            } else
                cout << it_2->second << endl;
        } else if (it == ma.begin()) {
            cout << (++it)->second << endl;
        } else if (it == --ma.end()) {
            cout << (--it)->second << endl;
        }
    }
    system("pause");
    return 0;
}
```
## Priority_queue 练习题
### 描述
我们定义一个正整数 $a$ 比正整数 $b$ 优先的含义是：

- $a$ 的质因数数目（不包括自身）比 $b$ 的质因数数目多；  
- 当两者质因数数目相等时，数值较大者优先级高。  

现在给定一个容器，初始元素数目为 $0$ ，之后每次往里面添加 $10$ 个元素，每次添加之后，要求输出优先级最高与最低的元素，并把这两个元素从容器中删除。

### 输入
第一行: $num$ (添加元素次数，$num \leq 30$ )

下面 $10 \times num$行，每行一个正整数 $n$ （ $n < 10000000$ ）。

```
1
10 7 66 4 5 30 91 100 8 9
```

### 输出
每次输入 $10$ 个整数后，输出容器中优先级最高与最低的元素，两者用空格间隔。

```
66 5
```
### Solution
本题没叫你用优先队列，那么其实可以不用。  

所以用``set``来完成（便于获取最大最小值），虽然``multiset``也可以，但是``set``可以去除不必要的元素，所以使用``set``。

顺便说一句，例如对顶堆这样的数据结构trick，有时候也会使用两个``multiset``而不是两个``priority_queue``，稍微慢一点但是好写。

接着需要注意的就是自定义优先规则需要传入一个仿函数（前面讲过，用类的重载运算符模拟函数功能），同时这个仿函数的重载必须是``const``，这是所有STL的约定，需要它通过静态成员函数形式被调用，否则编译器会报错。

这里用结构体``node``记录了一个数的原始数值和它的因数个数，由于这题数据范围较小直接筛了，不然预处理可以更快。

```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
bool isprime(int x) {
    if (x == 1) return false;
    if (x == 2) return true;
    for (int i = 2; i * i <= x; i++) {
        if (x % i == 0) return false;
    }
    return true;
}
int count(int x) {
    int ans = 0;
    for (int i = 1; i < x; i++) {
        if (x % i != 0) continue;
        if (isprime(i)) ans++;
    }
    return ans;
}
struct node {
    int num, rnum;
};
struct cmp {
    bool operator()(const node a, const node b) const {
        if (a.rnum == b.rnum) return a.num < b.num;
        return a.rnum < b.rnum;
    }
};
int main() {
    int n, k;
    cin >> n;
    set<node, cmp> queue;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= 10; j++) {
            cin >> k;
            node a;
            a.num = k;
            a.rnum = count(k);
            queue.insert(a);
        }
        auto it = queue.end();
        it--;
        cout << (*it).num << ' ';
        auto it_2 = queue.begin();
        cout << (*it_2).num << endl;
        queue.erase(it);
        queue.erase(it_2);
    }
    system("pause");
    return 0;
}
```
## 数据库内的学生信息
### 描述
程序填空，使得下面的程序，先输出以下内容：

```
(Tom,80),(Tom,70),(Jone,90),(Jack,70),(Alice,100),

(Tom,78),(Tom,78),(Jone,90),(Jack,70),(Alice,100),

(70,Jack),(70,Tom),(80,Tom),(90,Jone),(100,Alice),

(70,Error),(70,Error),(80,Tom),(90,Jone),(100,Alice),

******
```

然后，再根据输入数据按要求产生输出数据。
```cpp
#include <iostream>
#include <string>
#include <map>
#include <iterator>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
struct Student 
{
	string name;
	int score;
};
template <class T>
void Print(T first,T last) {
	for(;first!= last; ++ first)
		cout << * first << ",";
	cout << endl;
}
int main()
{
	
	Student s[] = { {"Tom",80},{"Jack",70},
					{"Jone",90},{"Tom",70},{"Alice",100} };
	
	MyMultimap<string,int> mp;
	for(int i = 0; i<5; ++ i)
		mp.insert(make_pair(s[i].name,s[i].score));
	Print(mp.begin(),mp.end()); //按姓名从大到小输出

	mp.Set("Tom",78); //把所有名为"Tom"的学生的成绩都设置为78
	Print(mp.begin(),mp.end());
	
	
	
	MyMultimap<int,string,less<int> > mp2;
	for(int i = 0; i<5; ++ i) 
		mp2.insert(make_pair(s[i].score,s[i].name));
	
	Print(mp2.begin(),mp2.end()); //按成绩从小到大输出
	mp2.Set(70,"Error");          //把所有成绩为70的学生，名字都改为"Error"
	Print(mp2.begin(),mp2.end());
	cout << "******" << endl;
	
	mp.clear();
	
	string name;
	string cmd;
	int score;		
	while(cin >> cmd ) {
		if( cmd == "A") {
			cin >> name >> score;
			if(mp.find(name) != mp.end() ) {
				cout << "erroe" << endl;
			}
			mp.insert(make_pair(name,score));
		}
		else if(cmd == "Q") {
			cin >> name;
			MyMultimap<string,int>::iterator p = mp.find(name);
			if( p!= mp.end()) {
				cout << p->second << endl;
			}
			else {
				cout << "Not Found" << endl; 
			}		
		}
	}
	return 0;
}
```
### 输入
输入数据的每一行，格式为以下之一：A name score 或 Q name score

name是个不带个空格的字符串，长度小于 20，score是个整数，能用int表示  

A name score 表示往数据库中新增一个姓名为name的学生，其分数为score。开始时数据库中一个学生也没有。  

Q name 表示在数据库中查询姓名为name的学生的分数。

数据保证学生不重名，输入数据少于200,000行。

```
A Tom1 30
A Tom2 40
Q Tom3 
A Tom4 89
Q Tom1
Q Tom2
```
### 输出
对于每个查询，输出学生的分数。如果查不到，则输出 "Not Found"

```
(Tom,80),(Tom,70),(Jone,90),(Jack,70),(Alice,100),
(Tom,78),(Tom,78),(Jone,90),(Jack,70),(Alice,100),
(70,Jack),(70,Tom),(80,Tom),(90,Jone),(100,Alice),
(70,Error),(70,Error),(80,Tom),(90,Jone),(100,Alice),
******
Not Found
30
40
```
### 提示
1) 编写模板的时候，连续的两个 “>”最好要用空格分开，以免被编译器看作是 ``>>``运算符。VS可能无此问题，但是Dev C++和服务器上的编译环境会有这个问题。比如 ``vector<vector<int>>`` 有可能出错，要改成 ``vector<vector<int> >``

2) 在模板中写迭代器时，最好在前面加上``typename``关键字，否则可能会编译错。VS可能无此问题，但是Dev C++和服务器上的编译环境会有这个问题。 
 
### Solution
观察代码，需要实现一个``MyMultimap``，这个类完全可以直接在里面存一个``multimap``，然后额外实现一些功能。

先看代码，需要实现``insert``、``Set``、``begin``、``end``、``clear``、``find``函数，其中除了``Set``没有原生定义，都可以直接调用``multimap``的功能实现。

然后，``Set``功能可以直接遍历整个``multimap``实现。

比较麻烦的是这个模板怎么写，第三个参数，在第一次实例化的时候没有传入，而第二次实例化的时候传入了一个比较模板类``less<int>``，根据第一次实例化的行为，第三个模板类参数应该缺省为``greater<T1>``。

然后，可以发现，对于一个模板``pair``，并没有合适的输出函数，因此需要重载输出函数，而且因为它不是类对象，应该写在类外面。

最后，由于编译器无法识别``MyMultimap<string,int>::iterator``是一个类型，因此需要将其用``typename``，让编译器认为它是``iterator``的别名。
```cpp
#include <iostream>
#include <string>
#include <map>
#include <iterator>
#include <algorithm>
using namespace std;
template<class T1,class T2,class Pred=greater<T1>>
class MyMultimap{
private:
	multimap<T1,T2,Pred>ma;
public:
	typedef typename multimap<T1,T2,Pred>::iterator iterator;
	MyMultimap(){
		ma.clear();
	}
	void insert(pair<T1,T2>x){
		ma.insert(x);
	}
	auto begin(){
		return ma.begin();
	}
	auto end(){
		return ma.end();
	}
	void Set(T1 x,T2 y){
		for(auto it=ma.begin();it!=ma.end();it++){
			if(it->first==x) it->second=y;
		}
	}
	void clear(){
		ma.clear();
	}
	auto find(T1 x){
		return ma.find(x);
	}
	
};
template<class T1,class T2>
ostream &operator<<(ostream &os,const pair<T1,T2>x){
	os<<'('<<x.first<<','<<x.second<<')';
	return os;
}
struct Student 
{
	string name;
	int score;
};
template <class T>
void Print(T first,T last) {
	for(;first!= last; ++ first)
		cout << * first << ",";
	cout << endl;
}
int main()
{
	
	Student s[] = { {"Tom",80},{"Jack",70},
					{"Jone",90},{"Tom",70},{"Alice",100} };
	
	MyMultimap<string,int> mp;
	for(int i = 0; i<5; ++ i)
		mp.insert(make_pair(s[i].name,s[i].score));
	Print(mp.begin(),mp.end()); //按姓名从大到小输出

	mp.Set("Tom",78); //把所有名为"Tom"的学生的成绩都设置为78
	Print(mp.begin(),mp.end());
	
	
	
	MyMultimap<int,string,less<int> > mp2;
	for(int i = 0; i<5; ++ i) 
		mp2.insert(make_pair(s[i].score,s[i].name));
	
	Print(mp2.begin(),mp2.end()); //按成绩从小到大输出
	mp2.Set(70,"Error");          //把所有成绩为70的学生，名字都改为"Error"
	Print(mp2.begin(),mp2.end());
	cout << "******" << endl;
	
	mp.clear();
	
	string name;
	string cmd;
	int score;		
	while(cin >> cmd ) {
		if( cmd == "A") {
			cin >> name >> score;
			if(mp.find(name) != mp.end() ) {
				cout << "erroe" << endl;
			}
			mp.insert(make_pair(name,score));
		}
		else if(cmd == "Q") {
			cin >> name;
			MyMultimap<string,int>::iterator p = mp.find(name);
			if( p!= mp.end()) {
				cout << p->second << endl;
			}
			else {
				cout << "Not Found" << endl; 
			}		
		}
	}
	return 0;
}
```