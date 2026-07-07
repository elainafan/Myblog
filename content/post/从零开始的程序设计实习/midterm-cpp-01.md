---
title: 从零开始的期中C++补充题(1)
date: 2025-05-09
categories:
    - 算法
slug: 从零开始的期中c补充题1
hidden: true
seriesOrder: 20
---
## Hero和Priest
### 描述
根据输出完善代码。
```cpp
Hero::defense()

Hero::attack()

Priest::defense()

Priest::attack()

Priest::defense()

#include <iostream>
using namespace std;
class Hero {
public:
// 在此处补充你的代码
};
class Priest: public Hero {
public:
    virtual void attack() { cout << "Priest::attack()" << endl; }
    virtual void defense() { cout << "Priest::defense()" << endl; } 
}; 

int main() {
    Priest anduin;
    Hero h;
    h.defense();
    Hero *player = &anduin;
    player->attack();
    player->defense();
    anduin.attack();
    anduin.defense();
    return 0;
}
```
### 输入
```
None
```
### 输出
```
Hero::defense()
Hero::attack()
Priest::defense()
Priest::attack()
Priest::defense()
```
### Solution
首先观察主函数，结合输出可以观察到``player``的``attack``函数输出的是``Hero``的，同时它的``defense``函数输出的是``Priest``的，因此可以看出``defense``是多态，而``attack``不是多态。

注意，在派生类中写虚函数，是没有什么意义的，多态完全取决于基类。

```cpp
#include <iostream>
using namespace std;
class Hero {
public:
    virtual void defense() { cout << "Hero::defense()" << endl; }
    void attack() { cout << "Hero::attack()" << endl; }
    // 在此处补充你的代码
};
class Priest : public Hero {
public:
    virtual void attack() { cout << "Priest::attack()" << endl; }
    virtual void defense() { cout << "Priest::defense()" << endl; }
};

int main() {
    Priest anduin;
    Hero h;
    h.defense();
    Hero *player = &anduin;
    player->attack();
    player->defense();
    anduin.attack();
    anduin.defense();
    system("pause");
    return 0;
}
```
## 可恶的括号
### 描述
根据输出完善程序。
```cpp
#include <cstdio>
#include <iostream>
using namespace std;

class f {
// 在此处补充你的代码
};

int main() {
  cout << f(3)(5) << endl;
  cout << f(4)(10) << endl;
  cout << f(114)(514) << endl;
  cout << f(9,7) << endl;
  cout << f(2,3) << endl;
  cout << f(2,5) << endl;
}
```
### 输入
```
None
```
### 输出
```
2
6
400
63
6
10
```
### Solution
这道题可以显然地看出，如果是传入一个参数的转换构造函数，那么得到的值就是它的值，否则是两个值的乘积。

再往下看，可以发现括号运算符被重载为相减，这里因为没有链式调用直接返回整型了。

最后，重载一下``f``类的输出运算符，就做完了。

```cpp
#include <cstdio>
#include <iostream>
using namespace std;

class f {
private:
    int x;

public:
    f(int t) : x(t) {}
    f(int a, int b) { x = a * b; }
    int operator()(int k) { return k - x; }
    friend ostream &operator<<(ostream &os, const f &t) {
        os << t.x;
        return os;
    }
    // 在此处补充你的代码
};

int main() {
    cout << f(3)(5) << endl;
    cout << f(4)(10) << endl;
    cout << f(114)(514) << endl;
    cout << f(9, 7) << endl;
    cout << f(2, 3) << endl;
    cout << f(2, 5) << endl;
    system("pause");
    return 0;
}
```
## Dog!Dog!Dog!
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class Mammal {
public:
  Mammal() { cout << "Mammal constructor...\n"; }
  virtual ~Mammal() { cout << "Mammal destructor...\n"; }
  Mammal (const Mammal & rhs);
  virtual void Speak() const { cout << "Mammal speak!\n"; }
  virtual Mammal* Clone() { return new Mammal(*this); }
};
  
class Dog : public Mammal {
// 在此处补充你的代码
};

Mammal::Mammal (const Mammal & rhs) {
  cout << "Mammal Copy Constructor...\n";
}
  
Dog::Dog(){ cout << "Dog constructor...\n"; }
Dog::~Dog(){ cout << "Dog destructor...\n"; }
void Dog::Speak()const { cout << "Woof!\n"; }

int main() {
  Mammal* x=new Dog, *y=new Mammal;
  Mammal* x1=x->Clone(), *y1=y->Clone();
  x1->Speak(); y1->Speak();
  return 0;
}
```
### 输入
```
None
```
### 输出
```
Mammal constructor...
Dog constructor...
Mammal constructor...
Mammal Copy Constructor...
Dog copy constructor...
Mammal Copy Constructor...
Woof!
Mammal speak!
```
### Solution
观察代码，首先发现题目已经定义了``Dog``类的默认构造函数和析构函数，以及``Speak``函数，但是还是要在类中做一下声明。

接着往下看，这里第一个``x1->Clone``输出了``Mammal Copy Constructor``和``Dog copy constructor``，说明调用的是``Dog``类中的``Clone``，且因为``Mammal``类中的``Clone``是虚函数，因此学着``Mammal``中的样子实现一下即可。


```cpp
#include <iostream>
using namespace std;
class Mammal {
public:
    Mammal() { cout << "Mammal constructor...\n"; }
    virtual ~Mammal() { cout << "Mammal destructor...\n"; }
    Mammal(const Mammal& rhs);
    virtual void Speak() const { cout << "Mammal speak!\n"; }
    virtual Mammal* Clone() { return new Mammal(*this); }
};

class Dog : public Mammal {
public:
    void Speak() const;
    Dog();
    Dog(const Dog& t) : Mammal(t) { cout << "Dog copy constructor...\n"; }
    ~Dog();
    Mammal* Clone() { return new Dog(*this); }
    // 在此处补充你的代码
};

Mammal::Mammal(const Mammal& rhs) { cout << "Mammal Copy Constructor...\n"; }

Dog::Dog() { cout << "Dog constructor...\n"; }
Dog::~Dog() { cout << "Dog destructor...\n"; }
void Dog::Speak() const { cout << "Woof!\n"; }

int main() {
    Mammal *x = new Dog, *y = new Mammal;
    Mammal *x1 = x->Clone(), *y1 = y->Clone();
    x1->Speak();
    y1->Speak();
    system("pause");
    return 0;
}
```
## cmp函数模板
### 描述
填写代码，按要求输出结果。要求实现cmp函数模板，不能实现cmp函数。
```cpp
#include <vector>
#include <set>
#include <list>
#include <iostream>
using namespace std;

template <class T>
// 在此处补充你的代码
int main(){
  int A[100];
  A[0]=1; A[1]=2;
  cmp(A[0],2);
  printf("finish 1\n");
  cmp(1, A[1]);
  printf("finish 2\n");
  cmp(A,A[1]);
  printf("finish 3\n");
}
```
### 输入
```
None
```
### 输出
```
a
finish 1
b
finish 2
c
finish 3
```
### Solution
就笔者看来，这道题是一道比较难的题，为什么难呢？因为这道题打破了通常的思路，即只使用一次模板化。

好的，下面介绍一种比较新的思路，也就是多次使用不同的模板声明同一个函数。

首先要明确的是，比如这里传入了``A[1]``，那么它在模板中的类型既可以是``T&``，也可以是``T``，而传入常数则只能是``T``。

下面，就可以根据这个区别，分别重载三个``cmp``为如代码所示的三个模板，而编译器在执行主函数的时候能自动匹配到最合适的模板，而不会混淆。

```cpp
#include <iostream>
#include <list>
#include <set>
#include <vector>

using namespace std;
template <class T>
void cmp(T& a, T b) {
    cout << "a" << endl;
}

template <class T>
void cmp(T a, T& b) {
    cout << "b" << endl;
}

template <class T>
void cmp(T* a, T& b) {
    cout << "c" << endl;
}
// 在此处补充你的代码
int main() {
    int A[100];
    A[0] = 1;
    A[1] = 2;
    cmp(A[0], 2);
    printf("finish 1\n");
    cmp(1, A[1]);
    printf("finish 2\n");
    cmp(A, A[1]);
    printf("finish 3\n");
    system("pause");
    return 0;
}
```
## 花里胡哨的求和
### 描述
读入 $n$ 个数, 输出 $n$ 个数, 其中第 $i$ 个数是读入中前 $i$ 个数的和。
```cpp
#include<iostream>
#include<vector>
using namespace std;
class A{
// 在此处补充你的代码
};
int A::presum=0;
int main(){
  int n;cin>>n;
  vector<A*> p;
  for(int i=0;i<n;i++){
    int x;cin>>x;
    p.push_back(new A(x));
  }
  for(int i=0;i<n;i++){
    p[i]->output();
  }
  return 0;
}
```
### 输入
```
3
1 2 3
```
### 输出

```
1
3
6
```
### Solution
首先观察到，这里需要一个传入整型的转换构造函数，随后观察不到任何可以执行前缀和的操作。

注意这里有一个静态成员变量``presum``，完全可以在``output``这个函数中执行加操作并输出。
```cpp
#include <iostream>
#include <vector>
using namespace std;
class A {
private:
    int x;
    static int presum;

public:
    A(int t) : x(t) {}
    void output() {
        presum += x;
        cout << presum << endl;
    }
    // 在此处补充你的代码
};
int A::presum = 0;
int main() {
    int n;
    cin >> n;
    vector<A*> p;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        p.push_back(new A(x));
    }
    for (int i = 0; i < n; i++) {
        p[i]->output();
    }
    system("pause");
    return 0;
}
```
## Midterm
### 描述
根据输出完善程序。
```cpp
#include<iostream>
using namespace std;

class Midterm {
private:
  int val; 
public:
// 在此处补充你的代码
};

int Min(int a,int b) {
  if(a < b)
    return a;
  else
    return b;
}
int main(){
  Midterm a; 
  cout << a << endl;
  cout << a + 2021 << endl;
  Midterm b(1000);
  cout << b ++ << endl; 
  ((b-=10)-=20)-=30;
  cout << b ++ << endl; 
  cout << Min(255,b) <<endl;
  return 0;
}
```
### 输入
```
None
```
### 输出

```
0
2021
1001
942
255
```
### Solution
首先观察主函数，很明显需要重载``输出``运算符和``右操作数为整型的加法``运算符。

再往下看，还需要实现传入整型的转换构造函数，以及重载后自加运算符。

接着，由于链式调用，需要重载``-=``运算符，并且返回``Midterm&``类型，即``this``指针。

最后，由于``Min``中传入的是整型，因此需要实现``Midterm``类到整型的强制类型转换函数。

```cpp
#include <iostream>
using namespace std;

class Midterm {
private:
    int val;

public:
    friend ostream &operator<<(ostream &os, const Midterm &t) {
        os << t.val;
        return os;
    }
    Midterm operator+(int x) {
        val += x;
        Midterm temp;
        temp.val = val;
        return temp;
    }
    Midterm(int x) : val(x) {}
    Midterm() {}
    Midterm operator++(int) {
        Midterm temp;
        val++;
        temp.val = val;
        return temp;
    }
    operator int() { return val; }
    Midterm &operator-=(int x) {
        val -= x;
        return *this;
    }
    // 在此处补充你的代码
};

int Min(int a, int b) {
    if (a < b)
        return a;
    else
        return b;
}
int main() {
    Midterm a;
    cout << a << endl;
    cout << a + 2021 << endl;
    Midterm b(1000);
    cout << b++ << endl;
    ((b -= 10) -= 20) -= 30;
    cout << b++ << endl;
    cout << Min(255, b) << endl;
    system("pause");
    return 0;
}
```
## 统计个数
### 描述
请补充下列代码，使其可以根据输入分别统计不同数字个数以及不同字符串个数。
```cpp
#include <iostream>
#include <string>
#include <set>
using namespace std;

class Counter{
    int cnt;
public:
    Counter():cnt(0){}
    virtual void push(void*) = 0;
    virtual string name() = 0;
    void inc(){
        ++cnt;
    }
    int number(){
        return cnt;
    }
};

template<class T>
class TCounter: public Counter{
// 在此处补充你的代码
};

Counter* build_counter(string name){
    if (name == "int") return new TCounter<int>("int");
    else return new TCounter<string>("string");
}



int main(){
    int n, m;
    cin >> n >> m;
    Counter *a = build_counter("int"), *b = build_counter("string");
    for (int i = 0; i < n; ++i){
        int x;
        cin >> x;
        a->push(&x);
    }
    for (int i = 0; i < m; ++i){
        string x;
        cin >> x;
        b->push(&x);
    }
    cout << a->name() << ": " << a->number() << endl;
    cout << b->name() << ": " << b->number();
    return 0;
}
```
### 输入
第一行两个整数 $n,m(1 \leq n,m \leq 1e5)$ ，分别代表接下来将会输入的数字个数以及字符串个数。  
接下来两行分别是 $n$ 个数字以及 $m$ 个字符串，由空格分隔。  
数字大小不超过int的表示范围，字符串长度不超过10。

```
5 5
1 2 3 4 3
a b b a ab
```
### 输出
输出两行，分别代表不同的数字个数以及不同的字符串个数。

```
int: 4
string: 3
```
### Solution
首先，介绍一下``void*``这个类型，这个类型的好处在于能够被能被任意类型的指针赋值，本身只表示指向一块地址，没有包含具体类型，而坏处是，这个类型无法被解引用。

接着看主函数，可以看到需要实现``Counter``类中两个虚函数的重载，从而实现多态（否则模板就失效了）。

至于要统计不同个数，那当然是使用``set``这个STL容器更方便（你看头文件是什么），然后再用一个字符串记录当前类的``name``即可。

```cpp
#include <iostream>
#include <set>
#include <string>

using namespace std;

class Counter {
    int cnt;

public:
    Counter() : cnt(0) {}
    virtual void push(void*) = 0;
    virtual string name() = 0;
    void inc() { ++cnt; }
    int number() { return cnt; }
};

template <class T>
class TCounter : public Counter {
private:
    set<T> s;
    string a;

public:
    TCounter(string k) : Counter() { a = k; }
    void push(void* x) {
        T* k = (T*)(x);
        if (s.find(*k) == s.end()) {
            inc();
            s.insert(*k);
        }
        return;
    }
    string name() { return a; }
    // 在此处补充你的代码
};

Counter* build_counter(string name) {
    if (name == "int")
        return new TCounter<int>("int");
    else
        return new TCounter<string>("string");
}

int main() {
    int n, m;
    cin >> n >> m;
    Counter *a = build_counter("int"), *b = build_counter("string");
    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        a->push(&x);
    }
    for (int i = 0; i < m; ++i) {
        string x;
        cin >> x;
        b->push(&x);
    }
    cout << a->name() << ": " << a->number() << endl;
    cout << b->name() << ": " << b->number();
    system("pause");
    return 0;
}
```
## P园食宿预订系统
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
重题，详细解析见[elainafan-从零开始的上机(8)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E4%B8%8A%E6%9C%BA8/#%E6%A0%A1%E5%9B%AD%E9%A3%9F%E5%AE%BF%E9%A2%84%E8%AE%A2%E7%B3%BB%E7%BB%9F)。
## MySet模板
### 描述
程序填空，从set模板派生一个MySet模板，并按要求输出。
```cpp
#include <iostream>
#include <map>
#include <algorithm>
#include <string>
#include <vector> 
#include <set>
#include <cstdio>
using namespace std;
// 在此处补充你的代码
struct A {
	int n;
	A(int i):n(i) { }
	operator int() {
		return n;
	}
	bool operator >(const A & a) const {
		return n > a.n;
	}
};
template <class IT>
void print(IT s,IT e)
{	
	for(; s != e; ++s)
		cout << *s << ",";
	cout << endl;
}
int main()
{
	MySet<int> mst;
	for (int i = 0;i < 10; ++i)
		mst.insert(i);
	print(mst.begin(),mst.end());
	int a[] = {1,2,3,4};
	mst.erase(a,a+3);
	print(mst.begin(),mst.end());
	
	A b[] = {{7},{8}};
	mst.erase(b,b+2);
	print(mst.begin(),mst.end());	
	mst.erase(mst.find(6));
	print(mst.begin(),mst.end());
	for(int i = 0;i < 1000000; ++i)
		mst.insert(i);
	for(int i = 0; i < 1000000 - 10; ++i) 
		mst.erase(mst.find(i));
	int n;
	cin >> n;
	MySet<A> msta;
	
	for(int i = 0;i < n; ++i) {
		string cmd;
		int n;
		cin >> cmd >> n;
		if( cmd == "ADD") 
			msta.insert(A(n));
		else {
			if (msta.find(A(n))!= msta.end())
				cout << "YES"  <<endl; 
			else
				cout << "NO" <<endl;
		}
	}
	return 0;
}
```
### 输入
第一行是整数 $n (n \leq 10000)$   
接下来 $n$ 行，每行一个命令，是以下两种格式之一：

ADD n 要求将整数 $n$加入集合。

FIND n 查询集合中有无整数 $n$ 。

```
6
ADD 1
ADD 2
FIND 3
FIND 2
ADD 3
FIND 3
```
### 输出
先产生一些固有的输出，然后对每个FIND命令， 如果集合中有整数 $n$ ，则输出"YES"，否则输出"NO"。

```
9,8,7,6,5,4,3,2,1,0,
9,8,7,6,5,4,0,
9,6,5,4,0,
9,5,4,0,
NO
YES
YES
```
### Solution
首先，观察代码，完全可以发现这里需要一个模板类来声明``MySet``类，同时它应该有``insert``、``begin``、``end``、``erase(传入一个迭代器或者某个区间的开头和结尾迭代器)``、``find``函数。

于是，可以用一个``set``作为这个类的成员变量，不过因为需要倒序排列，应该传入比较类为``greater<T>``。

同时，注意由于STL对于重载或者增加判断函数十分严格，因此最好要将没有修改成员变量的函数改为静态成员函数。

```cpp
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
template <class T>
class MySet {
private:
    set<T, greater<T>> ma;

public:
    MySet() { ma.clear(); }
    void insert(T x) { ma.insert(x); }
    auto begin() const { return ma.begin(); }
    auto end() const { return ma.end(); };
    auto find(T x) const { return ma.find(x); }
    void erase(auto x) { ma.erase(x); }
    void erase(auto x, auto y) {
        for (auto it = x; it != y; it++) {
            ma.erase(ma.find(*it));
        }
    }
};
// 在此处补充你的代码
struct A {
    int n;
    A(int i) : n(i) {}
    operator int() { return n; }
    bool operator>(const A& a) const { return n > a.n; }
};
template <class IT>
void print(IT s, IT e) {
    for (; s != e; ++s) cout << *s << ",";
    cout << endl;
}
int main() {
    MySet<int> mst;
    for (int i = 0; i < 10; ++i) mst.insert(i);
    print(mst.begin(), mst.end());
    int a[] = {1, 2, 3, 4};
    mst.erase(a, a + 3);
    print(mst.begin(), mst.end());

    A b[] = {{7}, {8}};
    mst.erase(b, b + 2);
    print(mst.begin(), mst.end());
    mst.erase(mst.find(6));
    print(mst.begin(), mst.end());
    for (int i = 0; i < 1000000; ++i) mst.insert(i);
    for (int i = 0; i < 1000000 - 10; ++i) mst.erase(mst.find(i));
    int n;
    cin >> n;
    MySet<A> msta;

    for (int i = 0; i < n; ++i) {
        string cmd;
        int n;
        cin >> cmd >> n;
        if (cmd == "ADD")
            msta.insert(A(n));
        else {
            if (msta.find(A(n)) != msta.end())
                cout << "YES" << endl;
            else
                cout << "NO" << endl;
        }
    }
    system("pause");
    return 0;
}
```
## C++也能函数式编程
### 描述
填写代码，按要求输出结果。
```cpp
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// 设 vector v = [x1, x2, ..., xn], 表示其内顺序存储了 x1 ~ xn 共 n 个值

template <class T, class F>
vector<T> vecMap(vector<T> v, F f) {
    // 返回 retV = [f(x1), f(x2), ..., f(xn)]
    vector<T> retV;
    for (auto x : v)
        retV.push_back(f(x));
    return retV;
}

template <class T, class F>
T vecReduce(T init, vector<T> v, F f) {
    // 返回 ret = f(...f(f(f(init, x1), x2), x3) ..., xn)
    T ret = init;
    for (auto x : v)
        ret = f(ret, x);
    return ret;
}

template <class T, class F>
vector<T> vecFilter(vector<T> v, F f) {
    // 返回 retV = [xi : 1 <= i <= n 且 f(xi) 成立]
    vector<T> retV;
    for (auto x : v)
        if (f(x)) retV.push_back(x);
    return retV;
}

template <class T>
void vecPrintln(vector<T> v) {
    // 依次输出 vector v 中的元素
    cout << "[ ";
    for (auto x : v)
        cout << x << ", ";
    cout << "]" << endl;
}

vector<int> vecRangeInt(int l, int r) {
    // 返回一个包含 [l, r) 中整数的 vector
    vector<int> retV;
    for (int x = l; x < r; ++x)
        retV.push_back(x);
    return retV;
}

class UnaryAdd;
class BinaryAdd;
class GetSecond;
class IsPrime;
// 在此处补充你的代码
int main() {
    // 测试 vecMap, UnaryAdd
    vector<int> a = vecRangeInt(0, 5);
    vecPrintln(a);                                  // [ 0, 1, 2, 3, 4, ]
    UnaryAdd addTen(10);
    vecPrintln(vecMap(a, addTen));                  // [ 10, 11, 12, 13, 14, ]
    UnaryAdd addOne(1);
    vecPrintln(vecMap(vecMap(a, addOne), addOne));  // [ 2, 3, 4, 5, 6, ]
    // 测试 vecReduce, GetSecond, BinaryAdd
    vector<int> b1 {1, 0, 2, 4};
    vector<int> b2 {8, 1, 9, 2};
    vector<int> b3 {2, 0, 4, 8};
    GetSecond getSecond;
    BinaryAdd binAdd;
    cout << vecReduce(-2, b1, getSecond) << endl;  // 4
    cout << vecReduce(-1, b2, getSecond) << endl;  // 2
    cout << vecReduce(0, b3, getSecond) << endl;   // 8
    cout << vecReduce(0, b1, binAdd) << endl;  // 0 + 1 + 0 + 2 + 4 = 7
    cout << vecReduce(1, b2, binAdd) << endl;  // 1 + 8 + 1 + 9 + 2 = 21
    cout << vecReduce(2, b3, binAdd) << endl;  // 2 + 2 + 0 + 4 + 8 = 16
    // 测试 vecFilter, isPrime
    vector<int> c1 = vecRangeInt(1, 10);
    vector<int> c2 {17, 11, 10, 19, 15, 23};
    IsPrime isPrime;
    vecPrintln(vecFilter(c1, isPrime));  // [ 2, 3, 5, 7, ]
    vecPrintln(vecFilter(c2, isPrime));  // [ 17, 11, 19, 23, ]

    vector<int> v1 = vecRangeInt(0, 8);
    cout << vecReduce(
            -1000000,
            vecMap(v1, [](int x) { return 7 * x - x * x + 2; }),
            [](int x, int y) { return max(x, y); }
    ) << endl;
    // max { 7x - x^2 + 2 : 0 <= x < 8 } = 14

    vector<int> v2 = vecRangeInt(0, 12);
    vecPrintln(vecFilter(
        vecMap(v2, [](int x) { return 2 * x + 1; }),
        [](int x) { return x % 3 == 0; }
    ));
    // [ 2x + 1 : 0 <= x < 12 且 (2x + 1) 是 3 的倍数 ] = [ 3, 9, 15, 21, ]
    return 0;
}
```
### 输入
```
None
```
### 输出

```
[ 0, 1, 2, 3, 4, ]
[ 10, 11, 12, 13, 14, ]
[ 2, 3, 4, 5, 6, ]
4
2
8
7
21
16
[ 2, 3, 5, 7, ]
[ 17, 11, 19, 23, ]
14
[ 3, 9, 15, 21, ]
```
### Solution
首先阅读好代码中的注释来理解题意，这是非常重要的。

根据代码，这里声明了四个类``UnaryAdd``、``BinaryAdd``、``GetSecond``、``IsPrime``，但是却没有实现，这里非常显然是要实现它们。

接着往下看，这些类实例化后被``vecMap``等等调用，再结合注释，可以知道它们作为仿函数被使用。

接着，结合每个类的名称和功能，逐一实现即可。

```cpp
#include <cmath>
#include <iostream>
#include <vector>

using namespace std;

// 设 vector v = [x1, x2, ..., xn], 表示其内顺序存储了 x1 ~ xn 共 n 个值

template <class T, class F>
vector<T> vecMap(vector<T> v, F f) {
    // 返回 retV = [f(x1), f(x2), ..., f(xn)]
    vector<T> retV;
    for (auto x : v) retV.push_back(f(x));
    return retV;
}

template <class T, class F>
T vecReduce(T init, vector<T> v, F f) {
    // 返回 ret = f(...f(f(f(init, x1), x2), x3) ..., xn)
    T ret = init;
    for (auto x : v) ret = f(ret, x);
    return ret;
}

template <class T, class F>
vector<T> vecFilter(vector<T> v, F f) {
    // 返回 retV = [xi : 1 <= i <= n 且 f(xi) 成立]
    vector<T> retV;
    for (auto x : v)
        if (f(x)) retV.push_back(x);
    return retV;
}

template <class T>
void vecPrintln(vector<T> v) {
    // 依次输出 vector v 中的元素
    cout << "[ ";
    for (auto x : v) cout << x << ", ";
    cout << "]" << endl;
}

vector<int> vecRangeInt(int l, int r) {
    // 返回一个包含 [l, r) 中整数的 vector
    vector<int> retV;
    for (int x = l; x < r; ++x) retV.push_back(x);
    return retV;
}

class UnaryAdd;
class BinaryAdd;
class GetSecond;
class IsPrime;
class UnaryAdd {
private:
    int x;

public:
    UnaryAdd(int t) : x(t) {}
    int operator()(int y) { return x + y; }
};
class GetSecond {
public:
    int operator()(int x, int y) { return y; }
};
class BinaryAdd {
public:
    int operator()(int x, int y) { return x + y; }
};
class IsPrime {
public:
    bool operator()(int x) {
        if (x == 1) return false;
        if (x == 2 || x == 3) return true;
        for (int i = 2; i * i <= x; i++) {
            if (x % i == 0) return false;
        }
        return true;
    }
};
// 在此处补充你的代码
int main() {
    // 测试 vecMap, UnaryAdd
    vector<int> a = vecRangeInt(0, 5);
    vecPrintln(a);  // [ 0, 1, 2, 3, 4, ]
    UnaryAdd addTen(10);
    vecPrintln(vecMap(a, addTen));  // [ 10, 11, 12, 13, 14, ]
    UnaryAdd addOne(1);
    vecPrintln(vecMap(vecMap(a, addOne), addOne));  // [ 2, 3, 4, 5, 6, ]
    // 测试 vecReduce, GetSecond, BinaryAdd
    vector<int> b1{1, 0, 2, 4};
    vector<int> b2{8, 1, 9, 2};
    vector<int> b3{2, 0, 4, 8};
    GetSecond getSecond;
    BinaryAdd binAdd;
    cout << vecReduce(-2, b1, getSecond) << endl;  // 4
    cout << vecReduce(-1, b2, getSecond) << endl;  // 2
    cout << vecReduce(0, b3, getSecond) << endl;   // 8
    cout << vecReduce(0, b1, binAdd) << endl;      // 0 + 1 + 0 + 2 + 4 = 7
    cout << vecReduce(1, b2, binAdd) << endl;      // 1 + 8 + 1 + 9 + 2 = 21
    cout << vecReduce(2, b3, binAdd) << endl;      // 2 + 2 + 0 + 4 + 8 = 16
    // 测试 vecFilter, isPrime
    vector<int> c1 = vecRangeInt(1, 10);
    vector<int> c2{17, 11, 10, 19, 15, 23};
    IsPrime isPrime;
    vecPrintln(vecFilter(c1, isPrime));  // [ 2, 3, 5, 7, ]
    vecPrintln(vecFilter(c2, isPrime));  // [ 17, 11, 19, 23, ]

    vector<int> v1 = vecRangeInt(0, 8);
    cout << vecReduce(-1000000, vecMap(v1, [](int x) { return 7 * x - x * x + 2; }), [](int x, int y) { return max(x, y); }) << endl;
    // max { 7x - x^2 + 2 : 0 <= x < 8 } = 14

    vector<int> v2 = vecRangeInt(0, 12);
    vecPrintln(vecFilter(vecMap(v2, [](int x) { return 2 * x + 1; }), [](int x) { return x % 3 == 0; }));
    // [ 2x + 1 : 0 <= x < 12 且 (2x + 1) 是 3 的倍数 ] = [ 3, 9, 15, 21, ]
    system("pause");
    return 0;
}
```
## 计算数组的低3位之和
### 描述
输入一个正整数构成的数组 $a_0, a_1, a_2, \ldots , a_{n-1},$ 计算它们的二进制低3位之和。
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main(int argc, char* argv[]) {
	int  v, my_sum=0;
	vector<int> vec;		
	cin>>v;
	while ( v ) {
		vec.push_back(v);
		cin>>v;
	}
	for_each(vec.begin(), vec.end(), CMy_add(my_sum));
	cout<<my_sum<<endl;	
	return 0;
}
```
### 输入
数组 $a$ ,以0表示输入结束。

```
1 3 9 7 3 6 20 15 18 17 4 8 18 0 
```
### 输出
一个整数 , 所输入数组各元素的二进制低3位之和。

```
41
```
### Solution
这里要先知道低三位是什么，就是二进制最低三位，范围是 $0 \sim 7$ 。

于是，由于这里使用了``for_each``，它的原理这里就不回顾了，如果需要回顾可以看之前的博文。

但是这里最后输出的是``my_sum``，说明传入的应该作为引用被修改，即``CMy_add``中的成员变量应该是一个``int&``变量，再根据``for_each``的原理重载``()``运算符进行运算。
```cpp
#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;
class CMy_add {
private:
    int& result;

public:
    CMy_add(int& x) : result(x) {}
    void operator()(int x) {
        result += (x & 1);
        result += ((x >> 1) & 1) * 2;
        result += ((x >> 2) & 1) * 4;
    }
};
// 在此处补充你的代码
int main(int argc, char* argv[]) {
    int v, my_sum = 0;
    vector<int> vec;
    cin >> v;
    while (v) {
        vec.push_back(v);
        cin >> v;
    }
    for_each(vec.begin(), vec.end(), CMy_add(my_sum));
    cout << my_sum << endl;
    system("pause");
    return 0;
}
```
## 求平均数的类真叫mean
### 描述
输入一系列正整数, 计算它们的平均值，结果去尾取整数。
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;
class CMean {
// 在此处补充你的代码
};

int main(int argc, char* argv[]) {
	int  v;
	int t;
	cin >> t;
	while ( t -- ) {
		cin >> v;
		vector<int> vec;
		while (v) {
			vec.push_back(v);
			cin >> v;
		}
		int myAver = 0;
		for_each(vec.begin(), vec.end(), CMean(myAver));
		cout << myAver << endl;
	}
	return 0;
}
```
### 输入
第一行是测试数据组数 $T$ 。

接下来 $T$ 行，每行一组数据。每行是若干个正整数，以0表示输入结束(0不算)。

```
1
17 4 8 18 0
``` 
### 输出
对每组数据，输出所有数的平均值，结果去尾取整数。

```
11
```
### Solution
这道题跟上道题的思路非常类似，还是通过存一个``int&``变量，保证``myAver``在每次进行括号运算后都被修改。

但是本题不一样的地方在于，应该多存总和和个数两个整型成员变量，从而每次用这两个变量对``myAver``进行修改。
```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

using namespace std;
class CMean {
private:
    int result;
    int num;
    int& res;

public:
    CMean(int& t) : result(t), num(0), res(t) {}
    void operator()(const auto& x) {
        result += x;
        num++;
        res = result / num;
        return;
    }
    // 在此处补充你的代码
};

int main(int argc, char* argv[]) {
    int v;
    int t;
    cin >> t;
    while (t--) {
        cin >> v;
        vector<int> vec;
        while (v) {
            vec.push_back(v);
            cin >> v;
        }
        int myAver = 0;
        for_each(vec.begin(), vec.end(), CMean(myAver));
        cout << myAver << endl;
    }
    system("pause");
    return 0;
}
```
## 积分图
### 描述
对于一幅灰度的图像，积分图中的任意一点 $(x,y)$ 的值是指从图像的左上角到这个点的所构成的矩形区域内所有的点的灰度值之和。
```cpp
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
class IntegralImage{
// 在此处补充你的代码
};
int main(){
    int H, W;
    cin >> H >> W;
    int ** image = new int*[H];
    for(int i=0;i<H;++i){
        image[i]=new int[W];
    }
    for(int i=0;i<H;++i)
    for(int j=0;j<W;++j)
        cin >> image[i][j];
    IntegralImage it(H,W);
    for_each(image, image+H, it);
    for(int i=0;i<H;++i){
        for(int j=0;j<W;++j)
            cout<<it[i][j]<<" ";
        cout<<endl;
    }
   
}
```
### 输入
第一行两个整数，分别是图像的宽、高 $H, W$。

接下来 $H \times W$ 的矩阵，分别代表图像的每个像素值。

```
2 3
1 2 3
1 0 0
```
### 输出
积分图中每个点的值,  $H \times W$ 的矩阵，每个像素之间用空格分开。

```
1 3 6
2 4 7
```
### Solution
首先，这里还是``for_each``，因此``IntegralImage``类还是重载``()``运算符实现反函数。

然后，就需要存储传入的矩阵，回想起之前使用的形式，这里还是使用二维指针，在转换构造函数时注意要向堆取空间，并且要初始化为0，不然会发生UB。

同时，这里在输出的时候，需要重载``[]``运算符。

再看这个``for_each``，每次传入仿函数``()``的是``*(image+i)``，即``int*``类型。

然后，根据传入形式，这里使用了贡献法对二维前缀和进行了求解，复杂度 $O(n^3)$ ，事实上有 $O(n^2)$ 的算法，但是这题不卡时间复杂度，而且那样比较不方便。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;
class IntegralImage {
private:
    int h, w;
    int** dd;
    int num;

public:
    IntegralImage(int a, int b) : h(a), w(b), num(0) {
        dd = new int*[h];
        for (int i = 0; i < h; i++) {
            dd[i] = new int[w];
        }
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                dd[i][j] = 0;
            }
        }
    }
    void operator()(int* x) {
        for (int i = 0; i < w; i++) {
            for (int j = num; j < h; j++) {
                for (int v = i; v < w; v++) {
                    dd[j][v] += x[i];
                }
            }
        }
        num++;
    }
    int* operator[](int x) { return dd[x]; }
    // 在此处补充你的代码
};
int main() {
    int H, W;
    cin >> H >> W;
    int** image = new int*[H];
    for (int i = 0; i < H; ++i) {
        image[i] = new int[W];
    }
    for (int i = 0; i < H; ++i)
        for (int j = 0; j < W; ++j) cin >> image[i][j];
    IntegralImage it(H, W);
    for_each(image, image + H, it);
    for (int i = 0; i < H; ++i) {
        for (int j = 0; j < W; ++j) cout << it[i][j] << " ";
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## 序列累加和字符串复制
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <set>
#include <string>
#include <stdio.h>
#include <vector>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main(){
    vector<int> v1;
    vector<string> v2;
    int N, val, num_repeat,result_int=0;
    string str,result_str="";
    cin>>N;
    cin>>num_repeat;
    for(int i=0;i<N;++i){
        cin>>val;
        v1.push_back(val);
    }
    for_each(v1.begin(),v1.end(),MyFunc<int>(num_repeat,result_int));
    for(int i=0;i<N;++i){
        cin>>str;
        v2.push_back(str);
    }
    for_each(v2.begin(),v2.end(),MyFunc<string>(num_repeat,result_str));
    cout<<result_int<<endl;
    cout<<"--------------"<<endl;
    cout<<result_str<<endl;
}
```
### 输入
首先读入两个整数 $N$ 和 $M$ ，表示数字/字符串序列的元素个数及累加次数。

接下来输入 $N$ 个整数，形成这个数字序列。  

接下来输入 $N$ 个字符串，形成一个字符串序列。  

```
3 4
9 8 1
ab cd ef
```
### 输出
对数字序列进行累加，并将结果乘以 $M$ 之后输出。  

对字符串序列进行拼接，并将结果复制 $M$ 次之后输出。

```
72
--------------
abcdefabcdefabcdefabcdef
```
### Solution
这道题看似跟上面的题没有区别，但是实际上还是有的。

问题就在于，结果复制这个操作，必须在所有操作结束之后，才能进行这个操作，而没有明显的所有操作结束这个标志。

于是，有一种新的想法，就是从仿函数类本身入手，也许在它的析构函数中作结果操作，就可以？

开开心心地写完，发现答案是错的，为什么？

回到``for_each``的原理，注意``for_each``函数的底层是传入值的，也就是会按照默认拷贝函数传入值，如果是只使用析构函数操作，那么``for_each``拷进去的参数的析构函数会被执行一次，同时``for_each``语句里生成的临时变量也会析构，也就是被析构两次，执行了两次，导致错误。

所以得再考虑从拷贝构造函数入手，使得只有临时变量的析构函数进行结果操作，这只需要在成员变量中加上一个布尔型变量就可以。

```cpp
##include <stdio.h>

#include <algorithm>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std;
template <class T>
class MyFunc {
private:
    int& num_repeat;
    T& result;
    bool flag;

public:
    MyFunc(int& n, T& k) : num_repeat(n), result(k), flag(true) {}
    MyFunc(const MyFunc& other) : num_repeat(other.num_repeat), result(other.result), flag(false) {}
    void operator()(const T& a) const {
        result += a;
        return;
    }
    ~MyFunc() {
        if (flag) {
            const T temp = result;
            for (int i = 1; i <= num_repeat - 1; i++) {
                result += temp;
            }
        }
    }
};
// 在此处补充你的代码
int main() {
    vector<int> v1;
    vector<string> v2;
    int N, val, num_repeat, result_int = 0;
    string str, result_str = "";
    cin >> N;
    cin >> num_repeat;
    for (int i = 0; i < N; ++i) {
        cin >> val;
        v1.push_back(val);
    }
    for_each(v1.begin(), v1.end(), MyFunc<int>(num_repeat, result_int));
    for (int i = 0; i < N; ++i) {
        cin >> str;
        v2.push_back(str);
    }
    for_each(v2.begin(), v2.end(), MyFunc<string>(num_repeat, result_str));
    cout << result_int << endl;
    cout << "--------------" << endl;
    cout << result_str << endl;
    system("pause");
    return 0;
}
```
## 人群的排序和分类
### 描述
对人群按照输入的信息进行排序和分类。
```cpp
#include <iostream>
#include <set>
#include <iterator>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main()
{

	int t;
	cin >> t;
	set<A*,Comp> ct;
	while( t -- ) {
		int n;
		cin >> n;
		ct.clear();
		for( int i = 0;i < n; ++i)	{
			char c; int k;
			cin >> c >> k;
			
			if( c == 'A')
				ct.insert(new A(k));
			else
				ct.insert(new B(k));
		}	
		for_each(ct.begin(),ct.end(),Print);
		cout << "****" << endl;
	}
}
```
### 输入
第一行是整数 $t,$ 表明一共 $t(t < 20 )$ 组数据。

对每组数据：

第一行是整数 $n,$ 表示下面一共有 $n(0 < n < 100  )$ 行。 

下面的每行代表一个人。每行以一个字母开头，代表该人所属的类别，然后跟着一个整数，代表年龄。字母只会是 'A‘或‘B' 。整数范围0到100。数据保证年龄都不相同。  

```
2
4
A 3
B 4
A 5
B 6
3
A 4
A 3
A 2
```
### 输出
对每组输入数据，将这些人按年龄从小到大输出。每个人先输出类别，再输出年龄。每组数据的末尾加一行 ``****`` 。

```
A 3
B 4
A 5
B 6
****
A 2
A 3
A 4
****
```
### Solution
观察代码，发现需要实现一个``A``类，同时这里需要将``B``实现为``A``类的派生，因为``set``中传入的都是``A*``类型。

然后，它们需要成员变量来记录当前类别和年龄，``A``类和``B``类需要一个传入整型的转换构造函数，同时由于``B``类实现了转换构造函数而对应的``A``类默认构造函数不存在，因此需要实现``A``类的默认构造函数。

接着，还需要实现一个仿函数``Comp``类，重载它的``()``运算符实现比较功能，注意STL容器的仿函数/比较函数都需要定义为静态函数，否则会报错。

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <set>

using namespace std;
class A {
public:
    int age;
    char id;
    A(int x) : age(x) { id = 'A'; }
    A() {}
};
class B : public A {
public:
    B(int x) {
        id = 'B';
        age = x;
    }
};
struct Comp {
    bool operator()(A* x, A* y) const { return x->age < y->age; }
};
void Print(const A* a) { cout << a->id << ' ' << a->age << endl; }
// 在此处补充你的代码
int main() {
    int t;
    cin >> t;
    set<A*, Comp> ct;
    while (t--) {
        int n;
        cin >> n;
        ct.clear();
        for (int i = 0; i < n; ++i) {
            char c;
            int k;
            cin >> c >> k;

            if (c == 'A')
                ct.insert(new A(k));
            else
                ct.insert(new B(k));
        }
        for_each(ct.begin(), ct.end(), Print);
        cout << "****" << endl;
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
重题，详细解析见[elainafan-从零开始的STL(2)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84stl2/#%E6%95%B0%E6%8D%AE%E5%BA%93%E5%86%85%E7%9A%84%E5%AD%A6%E7%94%9F%E4%BF%A1%E6%81%AF)。

## 矩形排序
### 描述
给定一系列边长已知的矩形，输出对矩形进行两种排序的结果。

在第一种排序中，先按矩形的面积从大到小排序；若两个矩形的面积相同，则周长大的排在前。

在第二种排序中，先按矩形的周长从小到大排序；若两个矩形的周长相同，则面积小的排在前。

```cpp
#include <iostream>
#include <set>
using namespace std;
// 在此处补充你的代码
int main() {
    multiset<Rectangle> m1;
    multiset<Rectangle, Comp> m2;
    int n, a, b;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a >> b;
        m1.insert(Rectangle(a, b));
        m2.insert(Rectangle(a, b));
    }
    for (multiset<Rectangle>::iterator it = m1.begin(); it != m1.end(); it++) {
        cout << *it << endl;
    }
    cout << endl;
    for (multiset<Rectangle>::iterator it = m2.begin(); it != m2.end(); it++) {
        cout << *it << endl;
    }
	return 0;
}
```
### 输入
第一行是一个整数 $n$ ，表示输入的矩形个数。 

接下来 $n$ 行表示了 $n$ 个矩形。每行有两个整数 $a$ 与 $b$ ，表示该矩形的长与宽。

```
6
3 8
4 6
10 2
6 6
4 8
3 6
```
### 输出
先用 $n$ 行输出第一种排序的结果。每行两个整数，依次表示该矩形的面积与周长。  

再输出一个空行。  

最后用 $n$ 行输出第二种排序的结果。每行两个整数，依次表示该矩形的面积与周长。

```
36 24
32 24
24 22
24 20
20 24
18 18

18 18
24 20
24 22
20 24
32 24
36 24
```
### Solution
观察代码，发现需要记录矩形的周长和面积，因此在矩阵类``Rectangle``的转换构造函数中，可以直接记录周长和面积。

随后，观察到这里有对迭代器的解引用得到``Rectangle``类对象，因此需要重载它的输出运算符。

同时，``m1``中需要采用``Rectangle``类重载的小于运算符进行比较，而``m2``中需要使用仿函数类``Comp``重载``()``运算符进行比较，注意STL的容器比较都需要实现为静态函数形式。

```cpp
#include <iostream>
#include <set>
using namespace std;
class Rectangle {
public:
    int l, w;
    int c, s;
    Rectangle(int a, int b) : l(a), w(b) {
        c = 2 * (a + b);
        s = a * b;
    }
    friend ostream &operator<<(ostream &os, const Rectangle &t) {
        os << t.s << ' ' << t.c;
        return os;
    }
    bool operator<(const Rectangle &k) const {
        if (s == k.s) return c > k.c;
        return s > k.s;
    }
};
struct Comp {
    bool operator()(Rectangle a, Rectangle b) const {
        if (a.c == b.c) return a.s < b.s;
        return a.c < b.c;
    }
};
// 在此处补充你的代码
int main() {
    multiset<Rectangle> m1;
    multiset<Rectangle, Comp> m2;
    int n, a, b;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a >> b;
        m1.insert(Rectangle(a, b));
        m2.insert(Rectangle(a, b));
    }
    for (multiset<Rectangle>::iterator it = m1.begin(); it != m1.end(); it++) {
        cout << *it << endl;
    }
    cout << endl;
    for (multiset<Rectangle>::iterator it = m2.begin(); it != m2.end(); it++) {
        cout << *it << endl;
    }
    system("pause");
    return 0;
}
```
## 学生考勤记录查询
### 描述
学生考勤记录查询，可以完成下面三条操作：

1) add date id，例如add 1 1500012755，学号为1500012755的学生，在本月1日缺勤

2) querydate_begin date_end，例如query 1 3，查询本月1日至本月3日（包含1日及3日）缺勤学生名单，输出格式为（同一日内缺勤的学生输出顺序与add操作顺序一致）：

date id id ……

date id ……

3) exit 结束程序

请实现QueryResult函数。

```cpp
#include <iostream>
#include <string>
#include <map>
#include <list>
using namespace std;
// 在此处补充你的代码
int main(int argc, char* argv[])
{
	map<int, list<int> > Attendance;
	map<int, list<int> >::iterator it;
	string cmd;
	int date, id, date_lower, date_upper;
	while (cin >> cmd){
		if (cmd == "add"){
			cin >> date >> id;
			it = Attendance.find(date);
			if (it != Attendance.end()){
				it->second.push_back(id);
			}
			else{
				list<int> lst_id;
				lst_id.push_back(id);
				Attendance.insert(make_pair(date,lst_id));
			}
		}
		else if (cmd == "query"){
			cin >> date_lower>>date_upper;
			QueryResult(Attendance.lower_bound(date_lower), Attendance.upper_bound(date_upper));
		}
		else if (cmd == "exit")
			return 0;
	}
	return 0;
}
```
### 输入
每一行数据格式如上述两条命令，其中date是int型，0 < date < 32，id为int型，以15开头的10位学号。

```
add 1 1500012755
add 1 1500012796
add 3 1500012755
query 1 2
add 4 1500012737
query 1 4
exit
```
### 输出
在输入数据有query命令时，输出相应格式的缺勤名单(每个学号后面有一个空格)。

```
1: 1500012755 1500012796
1: 1500012755 1500012796
3: 1500012755
4: 1500012737
```
### Solution
首先观察主函数，发现需要实现``Print``和``QueryResult``函数。

前者接受一个链表输出，直接遍历即可。

而后者接受两个迭代器，注意``map``的迭代器类型需要取``it->first``或者``it->second``表示键和值，这里仍然需要使用模板。

```cpp
#include <iostream>
#include <list>
#include <map>
#include <string>

using namespace std;
void Print(list<int> x) {
    for (auto i = x.begin(); i != x.end(); i++) {
        cout << *i << ' ';
    }
    cout << endl;
}
template <class T>
void QueryResult(T x, T y) {
    for (T i = x; i != y; i++) {
        cout << i->first << ": ";
        Print(i->second);
    }
}
// 在此处补充你的代码
int main(int argc, char* argv[]) {
    map<int, list<int> > Attendance;
    map<int, list<int> >::iterator it;
    string cmd;
    int date, id, date_lower, date_upper;
    while (cin >> cmd) {
        if (cmd == "add") {
            cin >> date >> id;
            it = Attendance.find(date);
            if (it != Attendance.end()) {
                it->second.push_back(id);
            } else {
                list<int> lst_id;
                lst_id.push_back(id);
                Attendance.insert(make_pair(date, lst_id));
            }
        } else if (cmd == "query") {
            cin >> date_lower >> date_upper;
            QueryResult(Attendance.lower_bound(date_lower), Attendance.upper_bound(date_upper));
        } else if (cmd == "exit") {
            system("pause");
            return 0;
        }
    }
    system("pause");
    return 0;
}
```
## 维护平面点
### 描述
程序填空，一开始平面上一个点都没有。

每次可以插入一个点，删除一个已经存在的点，或者按照 $x$ 或 $y$ 来查询一个存在的点。

保证任何时候任意两个点一定是一个点严格在另一个点的右下方。

即两点 $(x_1, y_1), (x_2, y_2),$ 必定有 $x_1 > x_2$ 且 $y_1 < y_2$ ，或者 $x_1 < x_2$ 且 $y_1 > y_2$ 。

```cpp
#include <set>
#include <iostream>
#include <string>
using namespace std;
// 在此处补充你的代码
int main() {
	string cmd;
	set<pair<int, int>, myComp> S;
	while (cin >> cmd) {
		if (cmd == "A") {
			int x, y;
			cin >> x >> y;
			S.insert(make_pair(x, y));
		} else if (cmd == "Qx") {
			int x;
			cin >> x;
			cout << S.lower_bound(make_pair(x, -1))->second << endl;
		} else if (cmd == "Qy") {
			int y;
			cin >> y;
			cout << S.lower_bound(make_pair(-1, y))->first << endl;
		} else {
			int x, y;
			cin >> x >> y;
			S.erase(make_pair(x, y));
		}
	}
	return 0;
}
```
### 输入
输入数据的每一行，格式为以下之一：

A x y  

R x y  

Qx x  

Qy y

其中 $x$ 与 $y$ 都是 $0$ 到 $10^9$ 之间的整数。

A x y 表示插入点 $(x, y)$  

R x y 表示删除点 $(x, y)$ ，保证存在。

Qx x 表示在当前所有点中，找到第一维为 $x$ 的点，输出其第二维的值，保证存在  

Qy y 表示在当前所有点中，找到第二维为 $y$ 的点，输出其第一维的值，保证存在  

总共操作数不超过100000。

```
A 3 5
A 4 2
Qx 4
R 4 2
A 4 3
Qy 3
```
### 输出
对于每一个 Qx 和 Qy 操作，输出一行表示对应的答案。

```
2
4
```
### Solution
这里首先注意到使用STL自带的``lower_bound``进行二分查找。

通常的使用场景是，在给定的容器中查找第一个大于等于给定值的值。

因此，就是第一个不小于给定值的值，这里需要改变小于的定义就可以。

这里的``Set``传入一个仿函数类，只需要重载它的``()``运算符即可。

再结合题干和给定的代码，首先为了查找，应该把点对按照左上到右下来排序，这就得到了第一个条件判断。

首先看查找``x``的例子，不难发现，设查找到的点对为``mid``，则当``mid.x<x``时，应该返回``false``，反之应该返回``true``（结合二分查找的原理理解），于是有了第三个条件判断。

同样地，从``y``的维度考虑，可以得到第二个条件判断。

```cpp
#include <iostream>
#include <set>
#include <string>

using namespace std;
struct myComp {
    bool operator()(const pair<int, int>& x, const pair<int, int>& y) const {
        if (x.first > 0 && y.first > 0 && x.second > 0 && y.second > 0) return x.first > y.first;
        if (x.first < 0 || y.first < 0) return x.second < y.second;
        if (x.second < 0 || y.second < 0) return x.first > y.first;
    }
};
// 在此处补充你的代码
int main() {
    string cmd;
    set<pair<int, int>, myComp> S;
    while (cin >> cmd) {
        if (cmd == "A") {
            int x, y;
            cin >> x >> y;
            S.insert(make_pair(x, y));
        } else if (cmd == "Qx") {
            int x;
            cin >> x;
            cout << S.lower_bound(make_pair(x, -1))->second << endl;
        } else if (cmd == "Qy") {
            int y;
            cin >> y;
            cout << S.lower_bound(make_pair(-1, y))->first << endl;
        } else {
            int x, y;
            cin >> x >> y;
            S.erase(make_pair(x, y));
        }
    }
    system("pause");
    return 0;
}
```
## 按要求输出
### 描述
根据输出完善程序。

```cpp
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;
int  a[10] = {0, 6, 7, 3, 9, 5, 8, 6, 4, 9};
int  b[10] = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
int main(int argc, char** argv) {
// 在此处补充你的代码
for(int i=0; i<10; i++) 
		c[a[i]] = b[i];
	for(it=c.begin(); it!=c.end(); it++) 
		cout<<it->second<<" ";
	return 0;
}
```
### 输入
```
None
```
### 输出

```
10 13 18 15 17 12 16 19
```
### Solution
这道题，可以观察到这里的迭代器输出的时候用的是``it->second``，因此直接选取``map``为STL容器，并且写出它的迭代器形式变量``it``。

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <vector>

using namespace std;
int a[10] = {0, 6, 7, 3, 9, 5, 8, 6, 4, 9};
int b[10] = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
int main(int argc, char** argv) {
    map<int, int> c;
    map<int, int>::iterator it;
    // 在此处补充你的代码
    for (int i = 0; i < 10; i++) c[a[i]] = b[i];
    for (it = c.begin(); it != c.end(); it++) cout << it->second << " ";
    system("pause");
    return 0;
}
```
## 去除重复元素排序
### 描述
根据输出完善程序。
```cpp
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;

int main() {
	int t;
	int  a[100];
	cin >> t;
	while(t--) {
		for(int i = 0;i < 12; ++i)
			cin >> a[i];
// 在此处补充你的代码
std::copy(b.begin(), b.end(), c);
		cout << endl;

	}
	return 0;
}
```
### 输入
第一行是个整数，表示输入数据组数。

每组数据一行,有12个整数。

```
2
34 5 4 6 3 9 8 34 5 3 3 18
31 2 4 6 2 9 8 31 5 3 3 18
```
### 输出
对每组数据, 将12个整数从小到大排序并去除重复元素后输出。

```
3 4 5 6 8 9 18 34 
2 3 4 5 6 8 9 18 31
``` 
### 提示
注意：行末都有一个空格。
### Solution
首先观察代码，发现这里输出只有一个``endl``。

结合之前做过的题目，可以联想起前面的``copy``语句，通过``ostream_iterator<int> c(cout," ")``声明，表示每次迭代器传变量到``cout``中，用``" "``隔开，这个用法比较少见。

接着，由于这里需要排序并且去重，因此笔者按照个人习惯选取了``vector``，不过用``set``肯定更方便。
```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <vector>

using namespace std;
int main() {
    int t;
    int a[100];
    cin >> t;
    while (t--) {
        for (int i = 0; i < 12; ++i) cin >> a[i];
        vector<int> b;
        for (int i = 0; i < 12; i++) {
            b.push_back(a[i]);
        }
        sort(b.begin(), b.end());
        auto las = unique(b.begin(), b.end());
        b.erase(las, b.end());
        ostream_iterator<int> c(cout, " ");
        // 在此处补充你的代码
        std::copy(b.begin(), b.end(), c);
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## 前k大的偶数
### 描述
输入n个整数，输出整数数列中大小排名前k的偶数。

```cpp
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <set>

using namespace std;
class MyQueue
{
// 在此处补充你的代码
};
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n, k;
		cin >> n >> k;
		MyQueue q(k);
		for (int i = 0; i < n; ++i)
			cin >> q;
		cout<<q;
		cout << endl;
	}
	return 0; 
}
```
### 输入
有多组数据，第一行是数据组数 $t$ 。

对每组数据：

第一行为整数 $n (n \geq 3)$ 和 $k$ 。  
接下来的一行为 $n$ 个整数，保证这些整数中至少有 $k$ 个偶数。

```
2
9 4
1 2 4 3 6 6 7 8 9
3 2
18 16 14
```
### 输出
对每组数据，输出 $k$ 个整数，降序排列，表示选出来的大小排名前 $k$ 的偶数。

```
8 6 6 4
18 16
```
### Solution
首先，看到输出前k肯定想的是优先队列，注意优先队列默认的是大根堆。

因此，需要对传入的数组取负数（或者使用``greater<int>``）将其转化为小根堆。

接着，需要重载输入运算符和输出运算符，由于出堆顺序，需要用一个``vector``读取出堆的数字并反转后再输出。
```cpp
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <vector>


using namespace std;
class MyQueue {
private:
    int tot, cnt;

public:
    priority_queue<int> q;
    MyQueue(int x) {
        tot = x;
        cnt = 0;
    }
    friend istream &operator>>(istream &is, MyQueue &t) {
        int dd;
        is >> dd;
        if (dd % 2)
            return is;
        else {
            t.q.push(-dd);
            t.cnt++;
            if (t.cnt > t.tot) t.q.pop();
            return is;
        }
    }
    friend ostream &operator<<(ostream &os, MyQueue &t) {
        vector<int> a;
        while (!t.q.empty()) {
            int x = -t.q.top();
            t.q.pop();
            a.push_back(x);
        }
        for (auto it = a.end() - 1; it >= a.begin(); it--) {
            os << *it << ' ';
        }
        return os;
    }
    // 在此处补充你的代码
};
int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, k;
        cin >> n >> k;
        MyQueue q(k);
        for (int i = 0; i < n; ++i) cin >> q;
        cout << q;
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## Three Sum
### 描述
给出一列备选整数，请问能否在其中选出三个（不能重复选取），使得它们的和等于一个给定数字呢？
```cpp
#include<cstdio>
#include<cstring>
#include<set>
using namespace std;

multiset<int> s;
int a[5000 + 5];

int main() {
	int n, T, k;
	scanf("%d", &T);
	while (T--) {
		s.clear();
		scanf("%d", &n);
		for (int i = 0; i < n; i ++) {
			scanf("%d", a + i);
			s.insert(a[i]);
		}
		bool flag = false;
		scanf("%d", &k);
		for (int i = 0; i < n; i ++) {
			for (int j = i + 1; j < n; j ++) {
				int target = k - a[i] - a[j], min_count = 1;
// 在此处补充你的代码
}
			if (flag) break;
		}
		puts(flag? "Yes": "No");
	}
}
```
### 输入
输入包括多组测试数据。第一行一个整数 $T(1 \leq T \leq 20)$ ，表示测试数据数量。  

接下来 $T$ 组测试数据分别输入，对于每组测试数据，第一行一个整数 $n(1 \leq n \leq 1000)$ ，表示给出备选数字的个数；第二行 $n$ 个用空格隔开的整数 $a_i(-3 \cdot 10^8 \leq ai \leq 3 \cdot 10^8)$ ，表示备选数字列表；第三行一个整数 $k(-10^9 \leq k \leq 10^9)$ ，表示希望组合的数字。

```
4
10
1 2 3 4 5 6 7 8 9 10
8
10
1 2 3 4 5 6 7 8 9 10
5
4
1 1 1 1
3
4
1 2 9 10
4
```
### 输出
对于每组测试数据输出一行答案，如果能够选出三个数合成 $k$ ，请输出"Yes"(不含引号)，否则输出"No".

```
Yes
No
Yes
No
```
### Solution
有点像力扣的三数之和这种题目，但是它没有采用枚举右维护左（或者枚举中间）的形式，先观察主函数代码。

这里的``min_count``，显然是为了防止查到重复值时，导致不满足条件，因此需要对重复值计数，并且判断剩下的重复值个数是否能够被取出。

```cpp
#include <cstdio>
#include <cstring>
#include <set>
using namespace std;

multiset<int> s;
int a[5000 + 5];

int main() {
    int n, T, k;
    scanf("%d", &T);
    while (T--) {
        s.clear();
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%d", a + i);
            s.insert(a[i]);
        }
        bool flag = false;
        scanf("%d", &k);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int target = k - a[i] - a[j], min_count = 1;
                if (s.find(target) != s.end()) {
                    if (target == a[i]) min_count++;
                    if (target == a[j]) min_count++;
                    if (min_count >= s.count(target)) flag = true;
                }
                // 在此处补充你的代码
            }
            if (flag) break;
        }
        puts(flag ? "Yes" : "No");
    }
    return 0;
}
```
## 排队看医生
### 描述
看病要排队是地球人都知道的常识。不过细心的Rainbow观察发现，医院里排队还是有讲究的：Rainbow所去的医院有三个医生同时看病。而看病的人病情有轻重，所以不能根据简单的先来先服务的原则。所以医院对每种病情规定了10种不同的优先级。级别为10的优先权最高，级别为1的优先权最低。医生在看病时，则会在他的队伍里面选择一个优先权最高的人进行诊治。如果遇到两个优先权一样的病人的话，则选择最早来排队的病人。

现在，请你来模拟一下这个看病的过程吧！

### 输入
输入数据包含多组测试。第一行一个整数 $T(1 \leq T \leq 20)$ ，表示测试数据数目。  

每组数据第一行有一个正整数 $N(1 \leq N \leq 20000)$ 表示发生事件的数目。  

接下来有 $N$ 行分别表示发生的事件。

一共有两种事件：

IN A B,表示有一个拥有优先级B的病人要求医生A诊治。 $(1 \leq A \leq 3, 1 \leq B \leq 10)$  

OUT A,表示医生A进行了一次诊治，诊治完毕后，病人出院。 $(1 \leq A \leq 3)$

```
2
7
IN 1 1
IN 1 2
OUT 1
OUT 2
IN 2 1
OUT 2
OUT 1 
2
IN 1 1
OUT 1
```
### 输出
对于每个”OUT A”事件，请在一行里面输出被诊治人的编号ID。如果该事件时无病人需要诊治，则输出”EMPTY”。  

诊治人的编号ID的定义为：在一组测试中，”IN A B”事件发生第 $K$ 次时，进来的病人ID即为 $K$ 。从1开始编号。

```
2
EMPTY
3
1
1
```
### Solution
首先，应该注意ID的定义，笔者看错在这里卡了一会。

由于有优先级这种存在，显然一看就是用优先队列的题目。

这里笔者选择使用将维护的变量转为结构体并重载运算符，事实上传入一个仿函数或者比较函数也可以。

注意，多测要清空。
```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
int t, n;
string x;
struct node {
    int id, se;
    bool operator<(node x) const {
        if (x.se == se)
            return id > x.id;
        else
            return se < x.se;
    }
};
int num;
int a, b;
priority_queue<node> q[4];
int main() {
    cin >> t;
    while (t--) {
        cin >> n;
        for (int i = 1; i <= 3; i++) {
            while (!q[i].empty()) {
                q[i].pop();
            }
            num = 0;
        }
        for (int i = 1; i <= n; i++) {
            cin >> x;
            if (x == "IN") {
                cin >> a >> b;
                num++;
                q[a].push(node{num, b});
            } else {
                cin >> a;
                if (q[a].empty()) {
                    cout << "EMPTY" << endl;
                    continue;
                } else {
                    node k = q[a].top();
                    q[a].pop();
                    cout << k.id << endl;
                    continue;
                }
            }
        }
    }
    system("pause");
    return 0;
}
```
## 宠物小精灵
### 描述
宠物小精灵的世界中，每位训练师都在收集自己的小精灵。但是，训练师的背包里只能同时携带6只小精灵。如果一位训练师抓到了更多的精灵，那么最早抓到的精灵将被自动传送到电脑中，保证持有的小精灵数量依然是6只。 训练师也可以随时从电脑中取出精灵，取出的精灵将从电脑中传送到训练师的背包里。取出的精灵同样被认为是最新的，导致背包中最早取出或抓到的精灵被替换到电脑中，训练师持有的精灵数量依然是6只。 初始状态下，所有训练师的背包中都没有小精灵，电脑中也没有任何训练师的精灵。

### 输入
输入数据包含多组测试。第一行一个整数 $T(1 \leq T \leq 20)$ ，表示测试数据数目。  

每组数据第一行有一个正整数 $N(1 \leq N \leq 20000)$ 表示发生事件的数目。  

接下来有 $N$ 行分别表示发生的事件。  

一共有两种事件：  

C X, Y 表示训练师 $X$ 抓到了精灵 $Y$ 。  
T X, Y 表示训练师 $X$ 试图从电脑中取出精灵 $Y$ 。

$X$ 和 $Y$ 都是长度在 $20$ 以下的由字母或数字构成的字符串。

小精灵的世界中同样存在着作恶多端的火箭队。他们试图利用电脑的漏洞，从电脑中取出本不属于自己的小精灵。因此，电脑需要识别并拒绝取出这种请求。注意，如果一只小精灵仅存在于训练师的背包中而未被传送至电脑，该训练师也不能取出这只精灵。相同训练师不会多次抓到相同名字的精灵。

```
1 10
C satoshi pikachu1
C satoshi pikachu2
C satoshi pikachu3
C satoshi pikachu4
C satoshi pikachu5
C satoshi pikachu6
C satoshi pikachu7
T satoshi pikachu2
T satoshi pikachu1
T pikachu pikachu2
```
### 输出
对于每次从电脑中取出小精灵的请求，输出一行。成功则输出Success，失败则输出Failed。

```
Failed
Success
Failed
```
### Solution
首先，还是多测记得清空。

这里看到有先进先出结构，因此选择使用队列进行维护，同时还需要建立人名到队列之间的映射关系，因此再套一层``map``。

同时，电脑也是分别属于每个训练师的，因此还需要用``map``建立人名到电脑的映射，然后因为有插入，再套一层``set``。

最后，笔者这里又建立了人名到队列元素数量的映射，不过可以直接用``queue``自带的``size``函数判断，因此有点画蛇添足。
```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
int t, n;
map<string, queue<string>> ma;
map<string, int> cnt;
map<string, set<string>> computer;
char op;
string x, y;
int main() {
    cin >> t;
    while (t--) {
        ma.clear();
        cnt.clear();
        computer.clear();
        cin >> n;
        for (int i = 1; i <= n; i++) {
            cin >> op;
            if (op == 'C') {
                cin >> x >> y;
                cnt[x]++;
                ma[x].push(y);
                if (cnt[x] >= 7) {
                    cnt[x]--;
                    string temp = ma[x].front();
                    ma[x].pop();
                    computer[x].insert(temp);
                }
            } else {
                cin >> x >> y;
                if (ma.find(x) != ma.end() && computer[x].find(y) != computer[x].end()) {
                    cout << "Success" << endl;
                    auto it = computer[x].find(y);
                    computer[x].erase(it);
                    ma[x].push(y);
                    cnt[x]++;
                    if (cnt[x] >= 7) {
                        cnt[x]--;
                        string temp = ma[x].front();
                        ma[x].pop();
                        computer[x].insert(temp);
                    }
                } else {
                    cout << "Failed" << endl;
                }
            }
        }
    }
    system("pause");
    return 0;
}
```
## 石油交易
### 描述
原油期货价格暴跌，甚至出现了负油价。有很多卖家想要低价卖出手中囤积的石油，同时也有部分买家想要低价抄底。

每位卖家和买家按时间顺序在交易平台依次发布交易信息。他们的交易流程如下：

卖家在交易平台发布自己希望卖出的石油桶数X， 以及这X桶石油每桶报价Y。当买家希望购买Z桶石油时，会从当前交易平台所有在售的石油中购买价格最低的Z桶， 但无法购买在其之后的卖家发布的石油。如果在买家购买Z桶石油之时，没有足够的石油在售，则不足的部分将按每桶40美元的价格购买， 所有卖家的价格均低于40美元。

现在请计算每位买家购买石油的总价。

### 输入
输入数据的第一行是一个正整数 $N(N < 100000)$ ，表明买卖信息的总数目。  

接下来 $N$ 行分别表示买卖的信息。  

一共有两种信息：  

SELL X Y，表示卖家希望卖出 $X$ 桶石油，每桶价格为 $Y$ 美元。

BUY Z，表示买家买入 $Z$ 桶石油。 

$0 < X，Z \leq 10000,Y$ 为整数。结果保证在INT范围内。

```
6
BUY 5
SELL 10 10
BUY 5
SELL 10 5
BUY 5
BUY 15
```
### 输出
对于每次买入石油的信息，输出一个正整数，表示该买家当次买入石油的总价。

```
200
50
25
275
```
### Solution
首先要注意的是，如果边遍历边删除迭代器的话，最好用``while``循环，或者去掉``for``循环的自增条件，否则会造成迭代器混乱。

然后看题目，这里需要使用``multimap``或者``multiset+pair``维护卖家卖出的两个信息，接着直接遍历即可。
```cpp
#include <bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x & (-x))
using namespace std;
string x;
ll cnt = 0;  // 库存
multimap<int, int> ma;
int n;
int a, b;
ll tot = 0;
int main() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> x;
        if (x == "BUY") {
            cin >> a;
            ll ans = 0;
            for (auto it = ma.begin(); it != ma.end();) {
                if (a <= 0) break;
                if (it->second <= a) {
                    a -= it->second;
                    ans += it->second * it->first;
                    tot -= it->second * it->first;
                    cnt -= it->second;
                    it = ma.erase(it);
                } else {
                    ans += it->first * a;
                    it->second -= a;
                    tot -= a * it->first;
                    cnt -= a;
                    a = 0;
                }
            }
            if (a > 0) ans += a * 40;
            cout << ans << endl;
        } else if (x == "SELL") {
            cin >> a >> b;
            ma.insert(make_pair(b, a));
            cnt += a;
            tot += a * b;
        }
    }
    system("pause");
    return 0;
}
```
