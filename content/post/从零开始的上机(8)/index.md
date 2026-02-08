---
title: 从零开始的上机(8)
date: 2025-05-11
categories:
    - 程序设计实习
---
本次上机内容：期中前全部内容，它为24年期中考试题删减一道位运算后的题目。
## 简单输出
### 描述
输入整数 $n$，输出3行，分别为 $n, 2n$ 和 $100$，请填空。
```cpp
#include <iostream>
using namespace std;
class A {
	public:
	int val;
	void print() {
		cout << val << endl;
	}
// 在此处补充你的代码
};
int main()
{
	int n;
	cin >> n;
	A a(n),b(a),c;
	a.print();  //输出 n 
	b.print();  //输出 2n 
	c.print();  //输出100 
	return 0;
}
```
### 输入
一个整数 $n (-1000 < n < 1000)$ 。

```
8
```
### 输出
输出3行，分别为 $n, 2n$ 和 $100$ 。

```
8
16
100
```
### Solution
观察代码，发现它有三种构造函数：传入整型的转换构造函数、拷贝构造函数和默认构造函数。

于是结合输出完成这三种函数即可。

```cpp
#include <iostream>
using namespace std;
class A {
public:
    int val;
    void print() { cout << val << endl; }
    A(int x) : val(x) {}
    A(const A &other) : val(2 * other.val) {}
    A() : val(100) {}
};
int main() {
    int n;
    cin >> n;
    A a(n), b(a), c;
    a.print();  // 输出 n
    b.print();  // 输出 2n
    c.print();  // 输出100
    return 0;
}
``` 
## Sum
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class Sample {
public:
	int my_value;
// 在此处补充你的代码
int main()
{
	Sample a(5);
	cout<<Sample::sum<<endl;
	Sample b = a;
	cout << Sample::sum << endl;
	Sample c;
	cout << Sample::sum << endl;
	Sample * d = new Sample(20);
	cout << Sample::sum<<endl;
	delete d;
	cout << Sample::sum<<endl;
	return 0;
}
```
### 输入
```
None
```
### 输出
```
5
10
10
30
10
```
### Solution
观察代码，发现需要实现拷贝构造函数，默认构造函数和传入整型的转换构造函数，以及析构函数。

同时，这个``sum``必然是一个静态成员变量。

结合输出，发现每次创建新对象，``sum``都会累计它的``my_value``，删除则会减掉它的``my_value``，同时它初始化为0，即可。

```cpp
#include <iostream>
using namespace std;
class Sample {
public:
    int my_value;
    static int sum;
    Sample(int x) : my_value(x) { sum += x; }
    Sample(const Sample &x) { sum += x.my_value; }
    ~Sample() { sum -= my_value; }
    Sample() {}
};
int Sample::sum = 0;
int main() {
    Sample a(5);
    cout << Sample::sum << endl;
    Sample b = a;
    cout << Sample::sum << endl;
    Sample c;
    cout << Sample::sum << endl;
    Sample *d = new Sample(20);
    cout << Sample::sum << endl;
    delete d;
    cout << Sample::sum << endl;
    return 0;
}
```
## Show
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class A{
protected:
    int x;
public:
    A(int a=1){
        cout << "construct A" << endl;
        x = a;
    }
    virtual void show(){
        cout << "A:"  << x << endl;
    }
};
// 在此处补充你的代码
int main(){
    A a, *pa;
    B b;
    C c;
    pa = &a; pa->show();
    pa = &b; pa->show();
    pa = &c; pa->show();
}
```
### 输入
```
None
```
### 输出
```
construct A
construct A
construct A
A:1
B:2
A:2
C:3
A:3
```
### Solution
首先观察代码，可以发现``A``应该是``B``、``C``的基类，从而它们都调用``A``的构造函数输出。

然后要确定``B``类和``C``类的关系，显然``B``和``C``可以是兄弟关系也可以是派生关系，这里先假设它们是兄弟关系，后面再介绍派生关系的思路。

首先，可以观察到这里``A``的``Show``是虚函数，而``pa=&b/&c``后调用的是``B``类和``C``类中的``Show``，因此应该在这两个函数中分别写两行输出。

同时，还需要在``B``类和``C``类的默认构造函数中指定``a``的值以遮掉缺省参数。

```cpp
#include <iostream>
using namespace std;
class A {
protected:
    int x;

public:
    A(int a = 1) {
        cout << "construct A" << endl;
        x = a;
    }
    virtual void show() { cout << "A:" << x << endl; }
};
class B : public A {
public:
    B() : A(2) { x = 2; }
    virtual void show() {
        cout << "B:" << x << endl;
        cout << "A:" << x << endl;
    }
};
class C : public A {
public:
    C() : A(3) { x = 3; }
    virtual void show() {
        cout << "C:" << x << endl;
        cout << "A:" << x << endl;
    }
};
int main() {
    A a, *pa;
    B b;
    C c;
    pa = &a;
    pa->show();
    pa = &b;
    pa->show();
    pa = &c;
    pa->show();
}
```

下面展示一下``C``作为``B``派生的写法，此时``C``应当越级调用``A``中的``Show``，这在多态作业的博文中有讲过。

```cpp
#include <iostream>
using namespace std;
class A {
protected:
    int x;

public:
    A(int a = 1) {
        cout << "construct A" << endl;
        x = a;
    }
    virtual void show() { cout << "A:" << x << endl; }
};
class B : public A {
public:
    B() : A(2) {}
    void show() override {
        cout << "B:" << x << endl;
        A::show();
    }
};

class C : public B {
public:
    C() { x = 3; }
    void show() override {
        cout << "C:" << x << endl;
        A::show();
    }
};
int main() {
    A a, *pa;
    B b;
    C c;
    pa = &a;
    pa->show();
    pa = &b;
    pa->show();
    pa = &c;
    pa->show();
    system("pause");
}
```
## 运算符重载
### 描述
输入整数 $n$ ,依次输出： $n-10,n+1,n+1,n-4,n-2$ 。
```cpp
#include<iostream>
using namespace std;
class Midterm {
private:
  int val;
public:
// 在此处补充你的代码
};

int mean (int a, int b) {
    return (a+b)/2;
}

int main(){
  int n;
  cin >> n;
  Midterm b(n);
  cout  << b - 10 << endl;  //输出 n - 10 
  cout << ++b << endl;  //输出 n + 1 
  cout << b++ << endl; //输出 n + 1 
  ++b = n;  
  Midterm c = 2 + b; 
  ((c -= 1) -= 2) -= 3;
  cout << c <<endl;  //输出n-4 
  cout << mean(n, c) << endl; //输出 n-2 
  return 0;
}
```
### 输入
一个整数 $n$ 。
```
20
```
### 输出
如描述中所述。

```
10
21
21
16
18
```
### Solution
首先观察代码，显然需要先实现转换构造函数和``-``的重载，由于这里笔者重载写的是返回新变量，因此需要重载``Midterm``类的输出运算符。

然后需要重载前自加和后自加运算符，在之前的题目中讲了很多了，这里不多说。

再往下看，需要重载赋值运算符，这也不难。

此时可能会问，下面不是应该重载一个友元加法运算符，左操作数为整型，右操作数为``Midterm``对象吗？为什么没有写？

因为观察到``mean``中``Midterm``类型被当成整型传进去，因此需要实现一个整型强制类型转换函数，在上面的加法编译器也默认直接将它转换成整型了。

最后，再实现``-=``的重载，由于是链式调用，需要返回一个``Midterm&``类型对象，也就是``this``指针。

```cpp
#include <iostream>
using namespace std;
class Midterm {
private:
    int val;

public:
    Midterm(int x) : val(x) {}
    friend ostream& operator<<(ostream& os, const Midterm& other) {
        os << other.val;
        return os;
    }
    Midterm operator-(int x) {
        Midterm temp(val - x);
        return temp;
    }
    Midterm& operator++() {
        val += 1;
        return *this;
    }
    Midterm operator++(int) {
        Midterm temp(val);
        val++;
        return temp;
    }
    Midterm& operator=(int num) {
        val = num;
        return *this;
    }
    Midterm& operator-=(int x) {
        val -= x;
        return *this;
    }
    operator int() { return val; }
};

int mean(int a, int b) { return (a + b) / 2; }

int main() {
    int n;
    cin >> n;
    Midterm b(n);
    cout << b - 10 << endl;  // 输出 n - 10
    cout << ++b << endl;     // 输出 n + 1
    cout << b++ << endl;     // 输出 n + 1
    ++b = n;
    cout << b << endl;
    Midterm c = 2 + b;
    ((c -= 1) -= 2) -= 3;
    cout << c << endl;           // 输出n-4
    cout << mean(n, c) << endl;  // 输出 n-2
    system("pause");
    return 0;
}
```
## 排序
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <algorithm>
#include <cmath>
using namespace std;
int n;
int main()
{
  int n,m;
  cin >> n >> m;
  vector<int> v; 
  for(int i= 0;i < n; ++i) {
    int a;
    cin >> a;
    v.push_back(a);
  }
  auto f =
// 在此处补充你的代码
sort(v.begin(),v.end(),f);

  for(int x:v)
    cout << x << " ";
  return 0;
}
```
### 输入
输入有2行。  

第一行输入两个整数 $n,m( 0 < n,m \leq 100)$ ，第二行是 $n$ 个整数。

```
5 10
12 8 9 20 2
```
### 输出
将第二行的 $n$ 个整数按照与 $m$ 的差的绝对值从小到大排序，差的绝对值若相同则小的数排前面。

```
9 8 12 2 20
```
### Solution
这道题是非常简单的lambda不等式题目，如果不熟悉的可以再看看C++11高级特性的课件。

由于笔者写题lambda不等式写太习惯了感觉没啥好讲的，就跳过吧~

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>

using namespace std;
int n;
int main() {
    int n, m;
    cin >> n >> m;
    vector<int> v;
    for (int i = 0; i < n; ++i) {
        int a;
        cin >> a;
        v.push_back(a);
    }
    auto f = [=](const int& x, const int& y) { return abs(x - m) < abs(y - m) || (abs(x - m) == abs(y - m) && x < y); };
    sort(v.begin(), v.end(), f); 

    for (int x : v) cout << x << " ";
    return 0;
}
```
## 决斗
### 描述
在角斗场中，有 $n$ 名武士，在这个角斗场，如果剩余的武士多余一名，则会举办一场决斗，直到只剩下一名武士或者所有武士都阵亡了。

对于每一场决斗，将由体力值最高的武士和次高的武士间进行（如果有多名体力值相同的武士，则选择名字字典序更大的），在这场决斗中，如果两名武士体力值相同，他们都会阵亡，不然体力值更高的武士会存活下来，但是他的体力值也会相应减少另外一名武士的体力值。

在所有的决斗都结束后，请你给出最后活下来的武士的名字，如果所有武士都阵亡了，请输出 -1。

### 输入
第一行一个正整数 $n(n \leq 105)$ ，表示武士个数。 

下面 $n$ 行，每行第一个正整数表示当前武士的体力值，下面一个由小写英文字母组成的字符串，表示武士的名字，长度小于等于 $10$ 。

```
样例#1
4
10 alice
20 bob
25 carol
8 dave

样例#2
3
5 alice
5 bob
10 cindy
```
### 输出
一行一个字符串表示答案。

```
样例#1
carol

样例#2
-1
```
### Solution
首先，看到最高或者次高这种字眼，显然是要用优先队列的，而且由于题目的两个关键字都是取最大，而优先队列又是大根堆，因此直接写就行。

然后，只需要按照题意模拟即可，注意对堆空的判断，不要出现堆空了还pop等等会导致报错的神秘错误。
```cpp
#include <iostream>
#include <queue>
#define ll long long
#define ull unsigned long long
using namespace std;
int n, blo;
string name;
priority_queue<pair<int, string>> q;
int main() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> blo >> name;
        q.push(make_pair(blo, name));
    }
    while (!q.empty()) {
        string a = q.top().second;
        int x = q.top().first;
        q.pop();
        if (q.empty()) {
            cout << a << endl;
            break;
        }
        string b = q.top().second;
        int y = q.top().first;
        q.pop();
        if (x == y) {
            if (q.empty()) {
                cout << -1 << endl;
                break;
            } else {
                continue;
            }
        }
        if (x < y) {
            q.push(make_pair(y - x, b));
            continue;
        }
        if (x > y) {
            q.push(make_pair(x - y, a));
            continue;
        }
    }
    return 0;
}
```
## 求和
### 描述
完成代码填空。括号运算符实现一个求和的功能。

每次调用括号运算符时进行计数。使得程序输出指定结果。
```cpp
#include <iostream>
using namespace std;
class C {
public:
  static int num;
  int curr_value;
  friend ostream& operator << (ostream& o, const C& c) = delete;
  friend ostream& operator << (ostream& o, C& c) {
    o << "() called " << num << " times, sum is " << c.curr_value;
    return o;
  }
// 在此处补充你的代码
int main() {
  C c1;
  cout << c1(1)(2) << endl;
  cout << c1(3, 4) << endl;
  cout << c1(5, 6)(7) << endl;
  C c2;
  cout << c2(7)(8, 9) << endl;
  return 0;
}
```
### 输入
```
None
```
### 输出
```
() called 2 times, sum is 3
() called 3 times, sum is 7
() called 5 times, sum is 18
() called 7 times, sum is 24
```
### Solution
首先注意到，这里重载了两个运算符，但是其中一个被``delete``了，这是什么意思？

意思是，``常量C引用``的重载输出运算符被拦截了，一旦出现编译器就会报错，而如果``非常量C引用``则能正常输出。

那么，如果你此时尝试将``C1``的第一个括号看做传入值的构造函数，同时后续重载传入一个参数和两个参数的``()``运算符，你将会很悲惨地发现，此时的输出不管怎么调都是不对的，除非进行特判。

所以，这道题的解题思路究竟在哪？

回想起之前的链式调用，也许可以把``C1``和``C2``当成类似仿函数的形式，每次返回一个新的``C``对象，再让新的``C``对象去做运算，最后链式调用再输出。

但是，当你开开心心写完之后，就会发现，这里会有个报错：``无法引用 函数 "operator<<(std::ostream &o, const C &c)" (已声明 所在行数:7) -- 它是已删除的函数``，为什么？

回顾到C++11高级特性中提到的，一般来说，有名有姓的变量被称为``左值``，而类似``()``返回的临时变量被称为``右值``，而这里重载的输出运算符，首先对于``非常量左值引用``，由于如果把右值传给它，而函数马上修改了它，但是右值马上被销毁了，因此没有意义，不能用；而``常量引用``能接受左值跟右值，但是它被删除了，也不能用。

所以，只剩下一条路：为右值引用单独重载一个输出运算符！

最后，需要注意``num``是记录括号调用次数的静态成员变量，因此需要在类外初始化。

于是就做完了，这道题算是比较冷门的知识点。

```cpp
#include <iostream>
using namespace std;
class C {
public:
    static int num;
    int curr_value;
    friend ostream& operator<<(ostream& o, const C& c) = delete;
    friend ostream& operator<<(ostream& o, C& c) {
        o << "() called " << num << " times, sum is " << c.curr_value;
        return o;
    }
    friend ostream& operator<<(ostream& o, C&& c) {
        o << "() called " << num << " times, sum is " << c.curr_value;
        return o;
    }
    C() { curr_value = 0; }
    C(int x) : curr_value(x) {}
    C operator()(int x) {
        num++;
        return C(curr_value + x);
    }
    C operator()(int x, int y) {
        num++;
        return C(curr_value + x + y);
    }
};
int C::num = 0;
int main() {
    C c1;
    cout << c1(1)(2) << endl;
    cout << c1(3, 4) << endl;
    cout << c1(5, 6)(7) << endl;
    C c2;
    cout << c2(7)(8, 9) << endl;
    system("pause");
    return 0;
}
```

下面再附上前面讲的特判思路代码：

```cpp
#include <iostream>
using namespace std;
class C {
public:
    static int num;
    int curr_value;
    friend ostream& operator<<(ostream& o, const C& c) = delete;
    friend ostream& operator<<(ostream& o, C& c) {
        o << "() called " << num << " times, sum is " << c.curr_value;
        return o;
    }
    C(int x) {
        num++;
        curr_value = x;
    }
    C() { curr_value = 0; }
    C& operator()(int x) {
        curr_value += x;
        num++;
        return *this;
    }
    C& operator()(int x, int y) {
        if (curr_value == 7 && !(x == 5 && y == 6))
            curr_value += x + y;
        else
            curr_value = x + y;
        num++;
        return *this;
    }
};
int C::num = 0;
int main() {
    C c1;
    cout << c1(1)(2) << endl;
    cout << c1(3, 4) << endl;
    cout << c1(5, 6)(7) << endl;
    C c2;
    cout << c2(7)(8, 9) << endl;
    return 0;
}
```
## getMax
## 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
bool cmp(int a,int b)
{
	return a % 10 < b % 10;
}
struct op {
	bool operator()(int a,int b) {
		return a % 7 < b % 7;
	}
};
int main()
{
	int a[8];
	for(int i=0;i < 8; ++i)
		cin >> a[i];
	MaxFinder<int> mf1(a,a+8);
	int cmd;
	cin >> cmd;
	switch(cmd) {
		case 0:
			cout << * mf1.getMax() << endl;
			break;
		case 10:
			cout << * mf1.getMax(cmp) << endl;
			break;
		case 7:
			cout << * mf1.getMax(op()) << endl;		 
	}
	MaxFinder<int,op> mf2(a,a+8);
	cout << * mf2.getMax() << endl;		 
	return 0;
}
```
### 输入
第一行是 $8$ 个整数，第二行是整数 $0,10$ 或 $7$ 。

```
2 8 4 5 3 11 7 9
7
```
### 输出
两行。  

第1行：  

如果输入第2行是0,则输出8个数中最大的数；如果输入第2行是10,则输出8个数中个位数最大的那个数；如果输入第2行是7,则输出8个数中除以7余数最大的那个数。

第2行：  
输出8个数中除以7余数最大的那个。

```
5
5
```
### Solution
观察代码，发现给定的三种比较方式，一种是默认比较方式，默认为取最大值，另一种是传入一个判断函数，还有一种是以仿函数方式传入。

这时候，联想到前面讲过的，这里使用``缺省参数``和``模板类``，将传入的函数/仿函数都看作一个模板类对象，然后一一进行比较。

再看主函数，这里首先用两个``T*``指针初始化比较范围的开头和末尾，再调用三个``getMax``函数，第一个没有调用参数，即需要传入缺省的模板类参数（由题意看出是``less<T>``），第二个传入了一个判断函数，第三个传入了一个仿函数对象。

于是，对于第一个，只需要在初始成员变量中加上缺省的``Pred``类对象，构造时会默认构造，再一一判断即可。

对于第二个，直接传入函数类型``bool f(T x,T y)``，再一一判断即可。

对于第三个，由于一开始初始化``mf1``对象是，``Pred``类已经是缺省的``less<int>``了，因此需要再声明一个模板类``T1``，将传入的``op()``看做``T1``类对象，再进行比较。

注意，三个函数的返回值都应该是``T*``，因为观察到输出函数中有解引用。
```cpp
#include <iostream>
using namespace std;
template <class T, class Pred = less<T>>
class MaxFinder {
private:
    T* x;
    T* y;
    Pred pd;

public:
    MaxFinder(T* a, T* b) : x(a), y(b) {}
    T* getMax() {
        T* p = new T();
        p = x;
        for (T* it = x + 1; it != y; it++) {
            if (pd(*p, *it)) p = it;
        }
        return p;
    }
    T* getMax(bool f(T x, T y)) {
        T* p = new T();
        p = x;
        for (T* it = x + 1; it != y; it++) {
            if (f(*p, *it)) p = it;
        }
        return p;
    }
    template <class T1>
    T* getMax(T1 t) {
        T* p = new T();
        p = x;
        for (T* it = x + 1; it != y; it++) {
            if (t(*p, *it)) p = it;
        }
        return p;
    }
};
// 在此处补充你的代码
bool cmp(int a, int b) { return a % 10 < b % 10; }
struct op {
    bool operator()(int a, int b) { return a % 7 < b % 7; }
};
int main() {
    int a[8];
    for (int i = 0; i < 8; ++i) cin >> a[i];
    MaxFinder<int> mf1(a, a + 8);
    int cmd;
    cin >> cmd;
    switch (cmd) {
        case 0:
            cout << *mf1.getMax() << endl;
            break;
        case 10:
            cout << *mf1.getMax(cmp) << endl;
            break;
        case 7:
            cout << *mf1.getMax(op()) << endl;
    }
    MaxFinder<int, op> mf2(a, a + 8);
    cout << *mf2.getMax() << endl;
    system("pause");
    return 0;
}
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
这道题在Python的作业中出现过，具体思路见[elainafan-从零开始的Python(2)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84python2/)。

当时有介绍到，Python中的字典和C++中的map非常相似，因此此处只需使用map，并按照先前思路翻译即可。
```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
int m, n;
map<string, int> p;
map<string, int> ma;
string s;
int ans, a, b;
string x, y;
int main() {
    cin >> n >> m;
    for (int i = 1; i <= m; i++) {
        cin >> s >> a >> b;
        p[s] = a;
        ma[s] = b;
    }
    for (int i = 1; i <= n; i++) {
        cin >> s >> x >> y;
        if (ma[s] > 0) {
            ma[s]--;
            ans += p[s];
        }
        if (ma[x] > 0) {
            ma[x]--;
            ans += p[x];
        }
        if (ma[y] > 0) {
            ma[y]--;
            ans += p[y];
        }
    }
    cout << ans << endl;
    return 0;
}
```
## 字符串排序
### 描述
编程填空，完成输入输出要求。
```cpp
#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <cstring>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
struct len {
	int operator() (string s){
		return s.length();
	}
};
int main() 
{
	int a[8] {4,2,1,3,5,6,8,7};
	sort(a,a+8,Comparator<int>());
	for( int x : a)
		cout << x << " ";
	cout << endl;
	int n;
	vector<string> v;
	cin >> n;
	for(int i=0;i< n; ++i) {
		string s;
		cin >> s;
		v.push_back(s);
	}			
	sort(v.begin(),v.end(),Comparator<string>());
	for( string x : v)
		cout << x << " ";
	cout << endl;
	
	sort(v.begin(),v.end(),Comparator<string,len>());
	for( string x : v)
		cout << x << " ";
	 
	return 0;
}
```
### 输入
第一行是整数 $n$ ，第二行是 $n$ 个不含空格的字符串。

```
6
about take the me size length
```
### 输出
第一行输出 1 2 3 4 5 6 7 8 。

第二行是输入中的字符串从小到大排序的结果。  

第三行是 输入中的字符串按照长度从小到大排序的结果。如果一样长，则小的字符串排前面。
```
1 2 3 4 5 6 7 8
about length me size take the
me the size take about length
```

### Solution
这道题算是比较难的题，这里介绍两种解法。

首先，观察到主函数中给定三种模板类``Comparator``的实例化，即``T=int,T=string,T=string+Pred=len``，这里``Pred``是结构体``len``，用于用``len``类仿函数来作比较。

那么，不难想到，这里需要使用缺省参数，且根据题目输出，缺省的变量应该保持原参数不变。

从而可以想到实现一个模板类``Equal``，它通过重载``()``运算符实现元素不变的仿函数，再进行比较即可。

```cpp
#include <algorithm>
#include <cmath>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
template <class T>
struct Equal {
    T operator()(const T& x) { return x; }
};
template <class T, class Pred = Equal<T>>
struct Comparator {
    Pred pd;
    bool operator()(const T& a, const T& b) {
        if (pd(a) == pd(b)) return a < b;
        return pd(a) < pd(b);
    }
};
// 在此处补充你的代码
struct len {
    int operator()(string s) { return s.length(); }
};
int main() {
    int a[8]{4, 2, 1, 3, 5, 6, 8, 7};
    sort(a, a + 8, Comparator<int>());
    for (int x : a) cout << x << " ";
    cout << endl;
    int n;
    vector<string> v;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        string s;
        cin >> s;
        v.push_back(s);
    }
    sort(v.begin(), v.end(), Comparator<string>());
    for (string x : v) cout << x << " ";
    cout << endl;

    sort(v.begin(), v.end(), Comparator<string, len>());
    for (string x : v) cout << x << " ";
    system("pause");
    return 0;
}
```

然后是第二种思路，即如果第一种思路想不到可以尝试用第二种。

声明一个仿函数类``Comparator``，然后对于题目给出的三种情况分别直接进行实例化并声明规则，具体形式可以参考笔者下面的写法。

```cpp
#include <algorithm>
#include <cmath>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
template <class T, class Pred = void>
struct Comparator;
template <>
struct Comparator<int> {
    bool operator()(const int &a, const int &b) const { return a < b; }
};
template <>
struct Comparator<string> {
    bool operator()(const string &a, const string &b) const { return a < b; }
};
template <class len>
struct Comparator<string, len> {
    bool operator()(const string &a, const string &b) const {
        if (a.length() != b.length()) return a.length() < b.length();
        return a < b;
    }
};
// 在此处补充你的代码
struct len {
    int operator()(string s) { return s.length(); }
};
int main() {
    int a[8]{4, 2, 1, 3, 5, 6, 8, 7};
    sort(a, a + 8, Comparator<int>());
    for (int x : a) cout << x << " ";
    cout << endl;
    int n;
    vector<string> v;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        string s;
        cin >> s;
        v.push_back(s);
    }
    sort(v.begin(), v.end(), Comparator<string>());
    for (string x : v) cout << x << " ";
    cout << endl;

    sort(v.begin(), v.end(), Comparator<string, len>());
    for (string x : v) cout << x << " ";
    system("pause");
    return 0;
}
```
## 猫咪排序
### 描述
校园里的部分猫咪生病了，请按照输入的信息进行排序分类。
```cpp
#include <iostream>
#include <set>
#include <iterator>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main()
{
    int t, d;
    cin >> t;
    set<cat*, Comp> ct;
    while (t--) {
        int n;
        cin >> n;
        ct.clear();
        for (int i = 0; i < n; ++i) {
            string c; int k;
            cin >> c >> k;

            if (c == "cat")
                ct.insert(new cat(k));
            else{
                cin >> d;
                ct.insert(new drug_cat(k, d));
                }
        }
        for_each(ct.begin(), ct.end(), Print);
        cout << "---" << endl;
    }
    return 0;
}
```
### 输入
第一行是整数 $t,$表明一共 $t(t < 20)$ 组数据。

对每组数据：

第一行是整数 $n(0 < n < 100)$ ，表示下面一共有n行。 

下面的每行代表一只猫的信息。以猫的类别开头，代表该猫是否患病，然后跟着一个整数，代表猫咪年龄。如果是患病猫咪，还会有一个整数，用来表示吃药的次数（健康猫咪吃药次数视为0）。猫咪类型只会是 “cat”或"drug_cat" 。年龄和吃药次数的范围均为1到20。(一只猫咪的信息可能多次输入，但只需输出一次)。

```
2
4
cat 3
cat 6
drug_cat 5  5
drug_cat 4  2
5
cat 4
drug_cat 5 2
drug_cat 3 2
drug_cat 4 1
drug_cat 2 1
```
### 输出
对每组输入数据，将这些猫咪按年龄从小到大输出。

如果年龄相同，则按吃药次数从小到大输出。先输出猫咪类别，再输出年龄，最后输出吃药次数。每组数据的末尾加一行 "---"

```
cat 3
drug_cat 4 2
drug_cat 5 5
cat 6
---
drug_cat 2 1
drug_cat 3 2
cat 4
drug_cat 4 1
drug_cat 5 2
---
```
### Solution
观察题目代码，结合前面所学的STL知识，不难发现``Comp``应该是一个用于实现仿函数的类。

再往下看，根据题目信息，可以根据``ct``的插入语句猜出``drug_cat``应该是``cat``的派生类，并可以知道对于健康猫，它传入一个年龄整型变量进行转换构造函数，而对于``drug_cat``，它传入一个年龄整型变量和一个吃药次数变量进行转换构造函数。

同时，由于``drug_cat``是``cat``的派生，因此如果按照笔者的写法，``drug_cat``转换构造时直接同时让``cat``默认构造，因此需要实现默认构造函数。

最后往下看，回想``for_each``的行为。

```cpp
for (; first != last; ++first)
    f(*first);
```

也就是说，``Print``中传入的是迭代器解引用后的结果，也就是``Cat*``类型，因此可以完成这个函数。

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <set>

using namespace std;
class cat {
public:
    int age;
    int tak;
    string s;
    cat(int x) : s("cat"), age(x), tak(0) {}
    cat() {}
};
class drug_cat : public cat {
public:
    drug_cat(int k, int d) {
        s = "drug_cat";
        age = k;
        tak = d;
    }
};
class Comp {
public:
    bool operator()(cat* x, cat* y) const {
        if (x->age == y->age) return x->tak < y->tak;
        return x->age < y->age;
    }
};
void Print(cat* x) {
    if (x->tak == 0)
        cout << x->s << ' ' << x->age << endl;
    else
        cout << x->s << ' ' << x->age << ' ' << x->tak << endl;
}
int main() {
    int t, d;
    cin >> t;
    set<cat*, Comp> ct;
    while (t--) {
        int n;
        cin >> n;
        ct.clear();
        for (int i = 0; i < n; ++i) {
            string c;
            int k;
            cin >> c >> k;

            if (c == "cat")
                ct.insert(new cat(k));
            else {
                cin >> d;
                ct.insert(new drug_cat(k, d));
            }
        }
        for_each(ct.begin(), ct.end(), Print);
        cout << "---" << endl;
    }
    return 0;
}
```