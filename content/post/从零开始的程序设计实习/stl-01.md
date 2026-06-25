---
title: 从零开始的STL(1)
date: 2025-04-18
categories:
    - 程序设计实习
slug: 从零开始的stl1
hidden: true
seriesOrder: 15
---
## goodcopy
### 描述
编写GoodCopy类模板，使得程序按指定方式输出。
```cpp
#include <iostream>
using namespace std;


template <class T>
struct GoodCopy {
// 在此处补充你的代码
};

int a[200];
int b[200];
string c[200];
string d[200];

template <class T>
void Print(T s,T e) {
	for(; s != e; ++s)
		cout << * s << ",";
	cout << endl;
}

int main()
{
	int t;
	cin >> t;
	while( t -- ) {
		int m ;
		cin >> m;
		for(int i = 0;i < m; ++i)
			cin >> a[i];
		GoodCopy<int>()(a,a+m,b);
		Print(b,b+m);
		GoodCopy<int>()(a,a+m,a+m/2);
		Print(a+m/2,a+m/2 + m);

		for(int i = 0;i < m; ++i)
			cin >> c[i];
		GoodCopy<string>()(c,c+m,d);
		Print(c,c+m);
		GoodCopy<string>()(c,c+m,c+m/2);
		Print(c+m/2,c+m/2 + m);
	}
	return 0;
}
```
### 输入
第一行是整数 $t$ ,表示数据组数。

每组数据第一行是整数 $n,n < 50$ 。

第二行是 $n$ 个整数，第三行是 $n$ 个字符串。 

```
2
4
1 2 3 4
Tom Jack Marry Peking
1
0
Ted
```
### 输出
将输入的整数原序输出两次，用","分隔。

然后将输入的字符串原序输出两次，也用 ","分隔。  

```
1,2,3,4,
1,2,3,4,
Tom,Jack,Marry,Peking,
Tom,Jack,Marry,Peking,
0,
0,
Ted,
Ted,
``` 
### Solution


看这句语法``GoodCopy<int>(a,a+m,b)``，它通过默认构造函数创建了一个GoodCopy类对象（结构体，不用管public，自动public的），然后这个类通过重载``()``运算符对传入参数进行操作，类似于函数，在之后的学习中，这种形式通常被称为``仿函数``。

然后，这里重载的``()``运算符接受一个起始指针``T*``，一个终止指针``T*``，还有一个目的指针``T*``，将起始指针到终止指针之间的部分复制到目的指针处。

注意，这里复制应该``从后往前``复制，否则可能覆盖数据。

```cpp
#include <iostream>
using namespace std;
template <class T>
struct GoodCopy {
public:
    void operator()(T* a, T* b, T* c) {
        for (int i = b - a - 1; i >= 0; i--) {
            *(c + i) = *(a + i);
        }
    }
    // 在此处补充你的代码
};

int a[200];
int b[200];
string c[200];
string d[200];

template <class T>
void Print(T s, T e) {
    for (; s != e; ++s) cout << *s << ",";
    cout << endl;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int m;
        cin >> m;
        for (int i = 0; i < m; ++i) cin >> a[i];
        GoodCopy<int>()(a, a + m, b);
        Print(b, b + m);
        GoodCopy<int>()(a, a + m, a + m / 2);
        Print(a + m / 2, a + m / 2 + m);

        for (int i = 0; i < m; ++i) cin >> c[i];
        GoodCopy<string>()(c, c + m, d);
        Print(c, c + m);
        GoodCopy<string>()(c, c + m, c + m / 2);
        Print(c + m / 2, c + m / 2 + m);
    }
    system("pause");
    return 0;
}
```
## 按距离排序
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <cmath>
#include <algorithm>
#include <string>
using namespace std;
template <class T1,class T2>
struct Closer {
// 在此处补充你的代码
};

int Distance1(int n1,int n2) {
	return abs(n1-n2);
}
int Distance2(const string & s1, const string & s2)
{
	return abs((int)s1.length()- (int) s2.length());
}
int a[10] = { 0,3,1,4,7,9,20,8,10,15};
string b[6] = {"American","Jack","To","Peking","abcdefghijklmnop","123456789"};
int main()
{
	int n;string s;
	while( cin >> n >> s ) {
		sort(a,a+10,Closer<int ,int (*)(int ,int)> (n,Distance1));
		for(int i = 0;i < 10; ++i)
			cout << a[i] << "," ;
		cout << endl;
		sort(b,b+6,Closer<string,int (*)(const string &,const string &  )> (s,Distance2)); 
		for(int i = 0;i < 6; ++i)
			cout << b[i] << "," ;
		cout << endl;
	}
	return 0;
}
```
### 输入
多组数据，每组一行，是一个整数 $n$ 和一个字符串 $s$ 。

```
2 a123456
4 a12345
```
### 输出
定义两个整数的距离为两个整数差的绝对值，定义两个字符串的距离为两个字符串长度差的绝对值。

对每组数据： 

对数组 $a$ 按和 $n$ 的距离从小到大排序后输出。距离相同的，值小的排在前面。  

然后对数组 $b$ ，按照和 $s$ 的距离从小到大输出。距离相同的，字典序小的排在前面。

```
1,3,0,4,7,8,9,10,15,20,
American,Peking,123456789,Jack,To,abcdefghijklmnop,
4,3,1,7,0,8,9,10,15,20,
Peking,American,Jack,123456789,To,abcdefghijklmnop,
```
### Solution
这里可以看到，Closer生成了一个匿名对象，用于sort的比较器。  

同时，结合上一题的经验，它作为仿函数接受一个``int/string``类型参数和一个函数指针，即``int*(int,int)``和一个``int*(const string&,const string&)``，这里直接用``T1``和``T2``替代。

接着看，由于``sort``每次调用是采用``()``运算符，因此重载``()``运算符来实现仿函数的比较即可。

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

using namespace std;
template <class T1, class T2>
struct Closer {
    T1 val;
    T2 func;
    Closer(T1 val, T2 func) : val(val), func(func) {}
    bool operator()(T1 a, T1 b) {
        int c = func(a, val);
        int d = func(b, val);
        if (c != d) {
            return c < d;
        }
        return a < b;
    }
    // 在此处补充你的代码
};

int Distance1(int n1, int n2) { return abs(n1 - n2); }
int Distance2(const string &s1, const string &s2) { return abs((int)s1.length() - (int)s2.length()); }
int a[10] = {0, 3, 1, 4, 7, 9, 20, 8, 10, 15};
string b[6] = {"American", "Jack", "To", "Peking", "abcdefghijklmnop", "123456789"};
int main() {
    int n;
    string s;
    while (cin >> n >> s) {
        sort(a, a + 10, Closer<int, int (*)(int, int)>(n, Distance1));
        for (int i = 0; i < 10; ++i) cout << a[i] << ",";
        cout << endl;
        sort(b, b + 6, Closer<string, int (*)(const string &, const string &)>(s, Distance2));
        for (int i = 0; i < 6; ++i) cout << b[i] << ",";
        cout << endl;
    }
    return 0;
}
```
## 很难蒙混过关的CArray3D三维数组模板类
### 描述
实现一个三维数组模版CArray3D，可以用来生成元素为任意类型变量的三维数组，输出指定结果。

```cpp
#include <iostream>
#include <iomanip> 
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
// 在此处补充你的代码
};

CArray3D<int> a(3,4,5);
CArray3D<double> b(3,2,2);
void PrintA()
{
	for(int i = 0;i < 3; ++i) {
		cout << "layer " << i << ":" << endl;
		for(int j = 0; j < 4; ++j) {
			for(int k = 0; k < 5; ++k) 
				cout << a[i][j][k] << "," ;
			cout << endl;
		}
	}
}
void PrintB()
{
	for(int i = 0;i < 3; ++i) {
		cout << "layer " << i << ":" << endl;
		for(int j = 0; j < 2; ++j) {
			for(int k = 0; k < 2; ++k) 
				cout << b[i][j][k] << "," ;
			cout << endl;
		}
	}
}

int main()
{

	int No = 0;
	for( int i = 0; i < 3; ++ i ) {
		a[i];
		for( int j = 0; j < 4; ++j ) {
			a[j][i];
			for( int k = 0; k < 5; ++k )
				a[i][j][k] = No ++;
			a[j][i][i];	
		}
	}
	PrintA();
	memset(a[1],-1 ,20*sizeof(int));	
	memset(a[1],-1 ,20*sizeof(int));
	PrintA(); 
	memset(a[1][1],0 ,5*sizeof(int));	
	PrintA();

	for( int i = 0; i < 3; ++ i )
		for( int j = 0; j < 2; ++j )
			for( int k = 0; k < 2; ++k )
				b[i][j][k] = 10.0/(i+j+k+1);
	PrintB();
	int n = a[0][1][2];
	double f = b[0][1][1];
	cout << "****" << endl;
	cout << n << "," << f << endl;
		
	return 0;
}
```
### 输入
```
None
```
### 输出
```
layer 0:
0,1,2,3,4,
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
20,21,22,23,24,
25,26,27,28,29,
30,31,32,33,34,
35,36,37,38,39,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
layer 0:
0,1,2,3,4,
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
layer 0:
0,1,2,3,4,
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
-1,-1,-1,-1,-1,
0,0,0,0,0,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
layer 0:
10,5,
5,3.33333,
layer 1:
5,3.33333,
3.33333,2.5,
layer 2:
3.33333,2.5,
2.5,2,
****
7,3.33333
```
### 提示
建议做法：

1. a[i][j][k] 这个表达式的第一个[]返回一个内部类的对象，该内部类也重载了[],且返回值为指针。

2. 必要时需重载对象到指针的强制类型转换运算符。
### Solution
这道题绝对是前期的难题，建议先看之前作业中笔者对二维题目的解释[elainafan-运算符重载](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD/#%E4%BA%8C%E7%BB%B4%E6%95%B0%E7%BB%84%E7%B1%BB)。

好的，开始看这题代码，首先看主函数。

可以看到使用模板类先实例化了``a``和``b``，转换构造函数传入的三个参数分别是三个维度的大小，于是使用``T*``指针向堆取这么多的空间。

其实这样更符合计算机内部的行为，也就是无论多少维数组的空间都是连续的。

然后往下看，由于有``a[i][j][k]``这种语句，而这次使用的不是三维指针，因此需要在其内部声明一个``CArray2D``模板类，这个类也有一个``T*``指针，而重载``CArray3D``类的``[]``运算符时，直接返回``CArray2D``类，它的``T*``指针可以通过计算机寻址方式得出，顺便也可以传入它的各维参数。

对于``CArray2D``类，直接重载它的``[]``，按照计算机的模拟寻址方式，返回一个``T*``指针，然后最后一个``[]``，就根据``T*``自带的就行。

最后，由于主函数中有``memset(a[1],-1,20*sizeof(int))``这样的函数，而根据平时使用的惯例，第一个参数都是数组开头，也就是一个指针，因此需要实现将``CArray2D``转换为``T*``的强制类型转换函数。

```cpp
#include <cstring>
#include <iomanip>
#include <iostream>

using namespace std;
template <class T>
class CArray3D {
public:
    int x, y, z;
    T* p;
    CArray3D(int x, int y, int z) : x(x), y(y), z(z) { p = new T[x * y * z]; }
    class CArray2D {
    private:
        T* dd;
        int k;

    public:
        CArray2D(T* pd, int id) : dd(pd), k(id) {}
        T* operator[](int index) {
            T* ddg = dd + index * k;
            return ddg;
        }
        operator T*() { return dd; }
    };
    CArray2D operator[](int index) {
        T* dd = p + index * y * z;
        return CArray2D(dd, z);
    }
};

CArray3D<int> a(3, 4, 5);
CArray3D<double> b(3, 2, 2);
void PrintA() {
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 5; ++k) cout << a[i][j][k] << ",";
            cout << endl;
        }
    }
}
void PrintB() {
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 2; ++j) {
            for (int k = 0; k < 2; ++k) cout << b[i][j][k] << ",";
            cout << endl;
        }
    }
}

int main() {
    int No = 0;
    for (int i = 0; i < 3; ++i) {
        a[i];
        for (int j = 0; j < 4; ++j) {
            a[j][i];
            for (int k = 0; k < 5; ++k) a[i][j][k] = No++;
            a[j][i][i];
        }
    }
    PrintA();
    memset(a[1], -1, 20 * sizeof(int));
    memset(a[1], -1, 20 * sizeof(int));
    PrintA();
    memset(a[1][1], 0, 5 * sizeof(int));
    PrintA();

    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 2; ++j)
            for (int k = 0; k < 2; ++k) b[i][j][k] = 10.0 / (i + j + k + 1);
    PrintB();
    int n = a[0][1][2];
    double f = b[0][1][1];
    cout << "****" << endl;
    cout << n << "," << f << endl;

    return 0;
}
```
## 函数对象的过滤器
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <vector>
using namespace std;


struct A {
	int v;
	A() { }
	A(int n):v(n) { };
	bool operator<(const A & a) const {
		return v < a.v;
	}
};
// 在此处补充你的代码
template <class T>
void Print(T s,T e)
{
	for(;s!=e; ++s)
		cout << *s << ",";
	cout << endl;
}
template <class T1, class T2,class T3>
T2 Filter( T1 s,T1 e, T2 s2, T3 op) 
{
	for(;s != e; ++s) {
		if( op(*s)) {
			* s2 = * s;
			++s2;
		}
	}
	return s2;
}

ostream & operator <<(ostream & o,A & a)
{
	o << a.v;
	return o;
}
vector<int> ia;
vector<A> aa; 
int main()
{
	int m,n;
	while(cin >> m >> n) {
		ia.clear();
		aa.clear(); 
		int k,tmp;
		cin >> k;
		for(int i = 0;i < k; ++i) {
			cin >> tmp; 
			ia.push_back(tmp);
			aa.push_back(tmp); 
		}
		vector<int> ib(k);
		vector<A> ab(k);
		vector<int>::iterator p =  Filter(ia.begin(),ia.end(),ib.begin(),FilterClass<int>(m,n));
		Print(ib.begin(),p);
		vector<A>::iterator pp = Filter(aa.begin(),aa.end(),ab.begin(),FilterClass<A>(m,n));
		Print(ab.begin(),pp);
		
	}
	return 0;
}
```
### 输入
多组数据，每组数据两行。

第一行是两个整数 $m$ 和 $n$ ，第二行先是一个整数 $k$ ,然后后面跟着 $k$ 个整数。

```
1 3
1 2
2 8
5 1 2 3 4 9
```
### 输出
对每组数据，按原顺序输出第二行的后 $k$ 个整数中，大于 $m$ 且小于 $n$ 的数输出两遍，数据保证一定能找到符合要求的整数。

```
2,
2,
3,4,
3,4,
```
### Solution
本题还是要求通过仿函数实现一个``FilterClass``类，它传入``m``和``n``作为转换构造函数的参数。

然后，再看给定的``Filter``函数，它的``op``就是传入的``FilterClass``类对象，因此应该重载``()``函数进行判断。

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct A {
    int v;
    A() {}
    A(int n) : v(n) {};
    bool operator<(const A& a) const { return v < a.v; }
};
template <class T>
class FilterClass {
public:
    T m, n;
    FilterClass(T m, T n) : m(m), n(n) {}
    bool operator()(T val) { return (m < val) && (val < n); }
};
// 在此处补充你的代码
template <class T>
void Print(T s, T e) {
    for (; s != e; ++s) cout << *s << ",";
    cout << endl;
}
template <class T1, class T2, class T3>
T2 Filter(T1 s, T1 e, T2 s2, T3 op) {
    for (; s != e; ++s) {
        if (op(*s)) {
            *s2 = *s;
            ++s2;
        }
    }
    return s2;
}

ostream& operator<<(ostream& o, A& a) {
    o << a.v;
    return o;
}
vector<int> ia;
vector<A> aa;
int main() {
    int m, n;
    while (cin >> m >> n) {
        ia.clear();
        aa.clear();
        int k, tmp;
        cin >> k;
        for (int i = 0; i < k; ++i) {
            cin >> tmp;
            ia.push_back(tmp);
            aa.push_back(tmp);
        }
        vector<int> ib(k);
        vector<A> ab(k);
        vector<int>::iterator p = Filter(ia.begin(), ia.end(), ib.begin(), FilterClass<int>(m, n));
        Print(ib.begin(), p);
        vector<A>::iterator pp = Filter(aa.begin(), aa.end(), ab.begin(), FilterClass<A>(m, n));
        Print(ab.begin(), pp);
    }
    return 0;
}
```
## 白给的list排序
### 描述
根据输出完善程序。
```cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <list>
using namespace std;
int main()
{	
	double a[] = {1.2,3.4,9.8,7.3,2.6};
	list<double> lst(a,a+5);
	lst.sort(
// 在此处补充你的代码
);
	
	for(list<double>::iterator i  = lst.begin(); i != lst.end(); ++i) 
		cout << * i << "," ;
    return 0;
}
```
### 输入
```
None
```
### 输出
```
9.8,7.3,3.4,2.6,1.2,
```
### Solution 
这道题确实白给，原因是STL提供了降序排序仿函数``greater<T>()``和升序排序仿函数``less<T>()``，于是就做完了。

```cpp
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <list>

using namespace std;
int main() {
    double a[] = {1.2, 3.4, 9.8, 7.3, 2.6};
    list<double> lst(a, a + 5);
    lst.sort(greater<double>()
             // 在此处补充你的代码
    );

    for (list<double>::iterator i = lst.begin(); i != lst.end(); ++i) cout << *i << ",";
    return 0;
}
```
## 我自己的ostream_iterator
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <list>
#include <string>
using namespace std;

template <class T1,class T2>
void Copy(T1 s,T1 e, T2 x)
{
	for(; s != e; ++s,++x)
		*x = *s;
}

 
template<class T>
class myostream_iteraotr
{
// 在此处补充你的代码
};


int main()
{	const int SIZE = 5;
	int a[SIZE] = {5,21,14,2,3};
	double b[SIZE] = { 1.4, 5.56,3.2,98.3,3.3};
	list<int> lst(a,a+SIZE);
	myostream_iteraotr<int> output(cout,",");
	Copy( lst.begin(),lst.end(),output); 
	cout << endl;
	myostream_iteraotr<double> output2(cout,"--");
	Copy(b,b+SIZE,output2);
	return 0;
}
```
### 输入
```
无
```
### 输出
```
5,21,14,2,3,
1.4--5.56--3.2--98.3--3.3--
```
### Solution
在[elainafan-从零开始的输入输出与模板](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E8%BE%93%E5%85%A5%E8%BE%93%E5%87%BA%E5%92%8C%E6%A8%A1%E6%9D%BF/)中，有一道``山寨版istream_iterator``的题，当时需要参考``istream_iterator``的正确实现做题。

这里查找资料，如下：
```cpp
	ostream_iterator& operator=(const _Ty& _Val) { // insert value into output stream, followed by delimiter
        *_Myostr << _Val;
        if (_Mydelim) {
            *_Myostr << _Mydelim;
        }

        return *this;
    }

    _NODISCARD ostream_iterator& operator*() noexcept /* strengthened */ {
        return *this;
    }

    ostream_iterator& operator++() noexcept /* strengthened */ {
        return *this;
    }
```
于是这里看懂了，也就是它的转换构造函数需要传入一个``ostream&``类变量和一个用于分隔输出的字符串进行运算。

同时，还需要重载``=``、``前自加``和``*``三个预算符，按照上面的实现即可，不要忘记加上分隔符。

```cpp
#include <iostream>
#include <list>
#include <string>
using namespace std;

template <class T1, class T2>
void Copy(T1 s, T1 e, T2 x) {
    for (; s != e; ++s, ++x) *x = *s;
}

template <class T>
class myostream_iteraotr {
private:
    ostream& ost;
    string k;

public:
    myostream_iteraotr(ostream& ost, string x) : ost(ost), k(x) {}
    myostream_iteraotr& operator++() { return *this; }
    myostream_iteraotr& operator*() { return *this; }
    void operator=(const T& other) { ost << other << k; }
    // 在此处补充你的代码
};

int main() {
    const int SIZE = 5;
    int a[SIZE] = {5, 21, 14, 2, 3};
    double b[SIZE] = {1.4, 5.56, 3.2, 98.3, 3.3};
    list<int> lst(a, a + SIZE);
    myostream_iteraotr<int> output(cout, ",");
    Copy(lst.begin(), lst.end(), output);
    cout << endl;
    myostream_iteraotr<double> output2(cout, "--");
    Copy(b, b + SIZE, output2);
    system("pause");
    return 0;
}
```