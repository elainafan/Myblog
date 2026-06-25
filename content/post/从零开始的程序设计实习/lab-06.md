---
title: 从零开始的上机(6)
date: 2025-04-20
categories:
    - 程序设计实习
slug: 从零开始的上机6
hidden: true
seriesOrder: 16
---
本次上机涉及内容：模板、STL(1)
## 计算数列平方和
### 描述
请写出sum函数，使其可以计算输入数列的平方和。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int sqr(int n) {
    return n * n;
}
int main() {
    int t, n, a[0x100];
    cin >> t;
    for (int c = 0; c < t; ++c) {
        cin >> n;
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << sum(a, n, sqr) << endl;
    }
    return 0;
}
```

### 输入
第一行是一个整数 $t (t \leq 10)$ ，表示数据组数。

每组输入数据包含两行，第一行是一个整数 $n (n \leq 100)$ ，第二行是 $n$ 个用空格分隔开的整数。

```
2
2
4 3
3
0 1 2
```

### 输出
对每组输入数据，输出该组数据中 $n$ 个整数的平方和。

```
25
5
```

### Solution
这里是用了通过模板实例化来做，不过因为没有类型的变换直接把``T*``当成``int*``类型写成普通函数也行。

跟之前模板作业中的第一题一样，随着遍历和解指针，将操作后的值累计即可。

```cpp
#include <iostream>
using namespace std;
template <class T>
int sum(T* a, int n, int f(int x)) {
    int temp = 0;
    for (T* i = a; i <= a + n - 1; i++) {
        temp += f(*i);
    }
    return temp;
}
int sqr(int n) { return n * n; }
int main() {
    int t, n, a[0x100];
    cin >> t;
    for (int c = 0; c < t; ++c) {
        cin >> n;
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << sum(a, n, sqr) << endl;
    }
    return 0;
}
```

## 又见模板
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <string>
using namespace std;
// 在此处补充你的代码
int main() {
	
	int t;
	cin >> t;
	while( t -- ) { 
	    int b1[10];
	    for(int i = 0;i < 10; ++i) 	
	
	    	cin >> b1[i];
	    A<int, 10> a1 = b1;
	    cout << a1[2] << endl;
	    
	
	    double b2[5] ;
	    for(int i = 0;i < 5; ++i) 	
	    	cin >> b2[i];
	    
	    A<double, 5> a2 = b2;
	    cout << a2.sum() << endl;
	
		
	    string b3[4] ;
	    for(int i = 0;i < 4; ++i) 	
	    	cin >> b3[i];
	    
	    A<string, 4> a3 = b3;
	    cout << a3.sum() << endl;
	}
	return 0;
}
```
### 输入
第一行是整数 $n$ ，表示有 $n$ 组数据。
每组数据有3行，第一行是10个整数，第二行是5个小数，第三行是4个不带空格的字符串，它们之间用空格分隔。

```
1
1 2 3 4 5 6 7 8 9 10
4.2 0.0 3.1 2.7 5.2
Hello , world !
```
### 输出
先输出10个整数里面的第三个，再输出5个小数的和（不用考虑小数点后面几位，用cout直接输出即可），再输出4个字符串连在一起的字符串。

```
3
15.2
Hello,world!
```
### Solution
首先，这道题肯定是需要使用模板类的，因为有实例化，实例化的第二个参数不是模板类型，而应该直接是``int``。

其次，由于这里是在模拟数组，因此应该使用``T*``指针模拟内存中的过程，不要忘记向堆中取空间与析构释放空间（这里使用的空间少，就没写析构）。

接着往下看，需要使用一个``T*``类型的转换构造函数，同时需要``T&``类型的重载``[]``运算符，因为这里没有修改操作所以可以不使用引用。

再往下看，需要实现一个``sum``函数，一步步求和即可。
```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T, int siz>
class A {
private:
    T* p;

public:
    A(T* b) {
        p = new T[siz];
        for (int i = 0; i < siz; i++) {
            p[i] = b[i];
        }
    }
    T operator[](int id) { return p[id]; }
    T sum() {
        T temp = p[0];
        for (int i = 1; i < siz; i++) {
            temp += p[i];
        }
        return temp;
    }
};
int main() {
    int t;
    cin >> t;
    while (t--) {
        int b1[10];
        for (int i = 0; i < 10; ++i) cin >> b1[i];
        A<int, 10> a1 = b1;
        cout << a1[2] << endl;

        double b2[5];
        for (int i = 0; i < 5; ++i) cin >> b2[i];

        A<double, 5> a2 = b2;
        cout << a2.sum() << endl;

        string b3[4];
        for (int i = 0; i < 4; ++i) cin >> b3[i];

        A<string, 4> a3 = b3;
        cout << a3.sum() << endl;
    }
    return 0;
}
```
## 简单的计算
### 描述
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;
template <class T>
class Add{
public:
// 在此处补充你的代码
};

int main(){
	double f;
	int n;
	while( cin >> f >> n) {
		
		Add<double> a1(f);
		Add<int> a2(n);
		double x,y;
		int p,q;
		cin >> x >> y >> p >> q;
		cout << a1(x, y) << endl;
		cout << a2(p, q) << endl;
	}
	return 0;
}
```

### 输入
有若干组数据，每组数据三行。

第一行是一个浮点数 $f$ 和一个整数 $n$ 。

第二行是两个浮点数 $x$ 和 $y$ 。

第三行是两个整数 $p$ 和 $q$ 。

```
2.2 3
1.0 2.0
10 20
4.5 30
4.8 9.2
100 200
```

### 输出
对每组数据，先输出 $x + y - f$ ，再输出 $p + q - n$ 。

### Solution
这里需要实例化模板，先用转换构造函数存入最后需要减掉的值。

然后再观察主函数，重载``()``运算符，参数为两个加的值，计算后输出即可。

```cpp
#include <iostream>
using namespace std;
template <class T>
class Add {
public:
    T r;
    Add(T d) : r(d) {}
    T operator()(T x, T y) {
        T temp;
        temp = x + y - r;
        return temp;
    }
};

int main() {
    double f;
    int n;
    while (cin >> f >> n) {
        Add<double> a1(f);
        Add<int> a2(n);
        double x, y;
        int p, q;
        cin >> x >> y >> p >> q;
        cout << a1(x, y) << endl;
        cout << a2(p, q) << endl;
    }
    return 0;
}
```

## 反转
### 描述
根据输出完善程序。

```cpp
#include<iostream>
using namespace std;
template<class T>
// 在此处补充你的代码
int main()
{
	int a[5] = { 10, 21, 34, 4, 50 };
	double d[6] = { 4.1, 11.1, 10.1, 9.1, 8.1, 7.1 };
	f(a, 5);
	f(d, 6);
	for (int i = 0; i < 5; i++)
	{
		cout << a[i] << " ";
	}
	cout << endl;
	for (int j = 0; j < 6; j++)
	{
		cout << d[j] << " ";
	}
	cout << endl;
	return 0;
}
```

### 输入
```
None
```

### 输出

```
50 4 34 21 10
7.1 8.1 9.1 10.1 11.1 4.1
```

### Solution
题目需要反转整个数组，可以观察到需要实现函数``f``，传入的是数组开头和它的大小。

因此，只需枚举前半段的元素，将它与后半段中对称的元素交换即可。

```cpp
#include <iostream>
using namespace std;
template <class T>
void f(T* a, int x) {
    for (int i = 0; i < x / 2; i++) {
        swap(*(a + i), *(a + x - 1 - i));
    }
}
int main() {
    int a[5] = {10, 21, 34, 4, 50};
    double d[6] = {4.1, 11.1, 10.1, 9.1, 8.1, 7.1};
    f(a, 5);
    f(d, 6);
    for (int i = 0; i < 5; i++) {
        cout << a[i] << " ";
    }
    cout << endl;
    for (int j = 0; j < 6; j++) {
        cout << d[j] << " ";
    }
    cout << endl;
    return 0;
}
```

## 很眼熟的模板题
### 描述
根据输出完善代码。
```cpp
#include <cstdio>
#include <iostream>
#include <string>
#include <cstring>
using namespace std;
// 在此处补充你的代码
string int2string(int x) { return to_string(x); }
int int2squareint(int x) { return x * x; }

int string2int(string str) {
	int res = 0;
	for (string::iterator iter = str.begin(); iter != str.end(); ++iter)
		res += *iter;
	return res;
}
string string2longerstring(string str) { return str + str; }

int main() {

	int t;
	cin >> t;
	while (t--) {
		int b1[10];
		for (int i = 0; i < 10; ++i)

			cin >> b1[i];
		A<int, 10> a1 = b1;
		cout << a1.sum(2, 6, int2squareint) << endl;
		cout << a1.sum(2, 6, int2string) << endl;

		string b2[4];
		for (int i = 0; i < 4; ++i)
			cin >> b2[i];

		A<string, 4> a2 = b2;
		cout << a2.sum(0, 3, string2int) << endl;
		cout << a2.sum(0, 3, string2longerstring) << endl;
	}
	return 0;
}
```
### 输入
第一行是整数 $n$ ，表示有 $n$ 组数据，每组数据有2行。  

第一行是10个整数，第二行是4个不带空格的字符串，它们之间用空格分隔。 

```
1
1 2 3 4 5 6 7 8 9 10
Machine , Learning !
```
### 输出
先输出10个整数里面的第3个到第7个的平方和，再输出10个整数里从第3个到第7个，按照字符串的方式，顺序连接的结果。

再输出4个字符串里，第1个到第4个串中，所有字符的ASCII码加和得到的整数，再输出4个字符串里，第1个到第4个串，分别复制一遍后，按照字符串的方式，顺序连接的结果。  

```
135
34567
1586
MachineMachine,,LearningLearning!!
```
### 提示
3^2 + 4^2 + 5^2 + 6^2 + 7^2 = 135。

“Machine,Learning!”中所有字符的ASCII码相加为1586。
### Solution
这里类的定义和转换构造函数都应该和``又见模板``这道题一样，就不多说了。

然后观察到，需要重载一个``sum``函数，这个函数传入了两个``int``类型变量和一个函数，由于观察到这里传入的函数的参数类型和输出类型跟原本模板类的类型不大一样，因此再次在模板类中``创建模板函数``，并最终实例化。

```cpp
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>

using namespace std;
template <class T, int siz>
class A {
private:
    T* p;

public:
    A(T* b) {
        p = new T[siz];
        for (int i = 0; i < siz; i++) {
            p[i] = b[i];
        }
    }
    template <class T1, class T2>
    T1 sum(int x, int y, T1 f(T2 k)) {
        T1 temp = f(p[x]);
        for (int i = x + 1; i <= y; i++) {
            temp += f(p[i]);
        }
        return temp;
    }
};
string int2string(int x) { return to_string(x); }
int int2squareint(int x) { return x * x; }

int string2int(string str) {
    int res = 0;
    for (string::iterator iter = str.begin(); iter != str.end(); ++iter) res += *iter;
    return res;
}
string string2longerstring(string str) { return str + str; }

int main() {
    int t;
    cin >> t;
    while (t--) {
        int b1[10];
        for (int i = 0; i < 10; ++i) cin >> b1[i];
        A<int, 10> a1 = b1;
        cout << a1.sum(2, 6, int2squareint) << endl;
        cout << a1.sum(2, 6, int2string) << endl;

        string b2[4];
        for (int i = 0; i < 4; ++i) cin >> b2[i];

        A<string, 4> a2 = b2;
        cout << a2.sum(0, 3, string2int) << endl;
        cout << a2.sum(0, 3, string2longerstring) << endl;
    }
    return 0;
}
```
## 奇怪的container
### 描述
根据输出完善程序。

```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T> 
class container{
// 在此处补充你的代码
};
int main(){
	int n,m;
	cin >> n >> m;
	string s1,s2;
	cin >> s1 >> s2;
    container <int> a = n;
    container <int> b = m;
    cout<<a+b<<endl;
    cout<<a+m<<endl;
    container <string> sa = string(s1);
    container <string> sb = string(s2);
    cout<<sa+sb<<endl;
    cout<< sa + s2<<endl;
}
```

### 输入
第一行是整数 $n$ ，第二行是整数 $m$ ，第三行是字符串 $s_1$ ，第四行是字符串 $s_2$ 。

```
5
3
foo
bar
```

### 输出
第一行是 $n+2 \times m$ ，第二行是 $n + m$ ，第三行是 $s_1+s_2+s_2$ ，第四行是 $s_1+s_2$ 。

```
11
8
foobarbar
foobar
```

### Solution
首先观察主函数，发现需要实现转换构造函数，还需要重载模板类的加号，一种右操作数是当前类``T``，另一种右操作数是``container``类，注意后者右操作数需要加两遍，就做完了。

```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T>
class container {
private:
    T k;

public:
    container(T x) : k(x) {}
    T operator+(const container &other) {
        T temp;
        temp = k + other.k + other.k;
        return temp;
    }
    T operator+(T x) {
        T temp;
        temp = k + x;
        return temp;
    }
};
int main() {
    int n, m;
    cin >> n >> m;
    string s1, s2;
    cin >> s1 >> s2;
    container<int> a = n;
    container<int> b = m;
    cout << a + b << endl;
    cout << a + m << endl;
    container<string> sa = string(s1);
    container<string> sb = string(s2);
    cout << sa + sb << endl;
    cout << sa + s2 << endl;
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
重题，见[elainafan-从零开始的STL(1)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84stl1/#%E5%BE%88%E9%9A%BE%E8%92%99%E6%B7%B7%E8%BF%87%E5%85%B3%E7%9A%84carray3d%E4%B8%89%E7%BB%B4%E6%95%B0%E7%BB%84%E6%A8%A1%E6%9D%BF%E7%B1%BB)。

## 又是MyClass
### 描述
根据输出完善程序。

```cpp
#include <iostream>
#include <cstring> 
#include <vector>
#include <cstdio> 
using namespace std;
// 在此处补充你的代码
int  a[40];
int main(int argc, char** argv) {
	int t;
	scanf("%d",&t);
	while ( t -- ) {
		int m;
		scanf("%d",&m);
		for (int i = 0;i < m; ++i) 
			scanf("%d",a+i);
		char s[100];
		scanf("%s",s);
		CMyClass<int> b(a, m);
		CMyClass<char> c(s, strlen(s));
		printf("%d %c\n", b[5], c[7]);
	}
	return 0;
}
```

### 输入
第一行是整数t表示数据组数，每组数据有两行。

第一行开头是整数 $m$ ，然后后面是 $m(5 < m < 30)$ 个整数。

第二行是一个没有空格的字符串，长度不超过 $50$ 。

```
1
6 1 3 5 5095 8 8
helloworld
```

### 输出
对每组数据，先输出 $m$ 个整数中的第5个，然后输出字符串中的第7个字符。

第 $i$ 个中的 $i$ 是从0开始算的。

```
8 r
```

### Solution
观察主函数，发现这里需要一个模板类，每次通过转换构造函数传入一个``T*``变量代表数组，还有一个``int``变量代表数组大小。

同时跟之前一样，使用指针表示数组，转换构造函数需要先向堆取空间再初始化。

接着，发现需要重载``[]``运算符，由于这里不需要修改直接返回``T``类型即可。

```cpp
#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>

using namespace std;
template <class T>
class CMyClass {
private:
    int siz;
    T* p;

public:
    CMyClass(T* b, int s) : siz(s) {
        p = new T[siz];
        for (int i = 0; i < siz; i++) {
            p[i] = b[i];
        }
    }
    T operator[](int x) { return p[x]; }
};
int a[40];
int main(int argc, char** argv) {
    int t;
    scanf("%d", &t);
    while (t--) {
        int m;
        scanf("%d", &m);
        for (int i = 0; i < m; ++i) scanf("%d", a + i);
        char s[100];
        scanf("%s", s);
        CMyClass<int> b(a, m);
        CMyClass<char> c(s, strlen(s));
        printf("%d %c\n", b[5], c[7]);
    }
    return 0;
}
```

## 惊呆！分数竟然也能这样输入输出和运算！
### 描述
程序填空，使这段代码可以完成分数的输入、输出和乘法运算。

```cpp
#include <iostream>
using namespace std;
int gcd(int a, int b) { // 计算两个数的最大公约数
    return (!b) ? a : gcd(b, a % b);
}
class Fraction {
    int p, q;
public:
// 在此处补充你的代码
};

int main(){
    int testcases;
    cin >> testcases;
    while (testcases --) {
        Fraction a, b, two(2);
        cin >> a >> b;
        cout << a << " * " << b << " = " << a * b << endl;
        cout << "2 * " << a << " = " << two * a << endl;
        cout << b << " * 3 = " << b * 3 << endl;
    }
    return 0;
}
```

### 输入
多组数据，第一行一个数 $t(1 \leq t \leq 100)$ 表示数据组数。

接下来 $t$ 行，每行读入四个整数 $a, b, c, d$ ，表示两个分数 $\frac{a}{b}$ 和 $\frac{c}{d}$ 。$(1 \leq a,b,c,d \leq 100)$

```
2
1 2 8 3
5 18 12 2
```

### 输出
对每组数据都输出 $a \times b,2 \times a，b \times 3$ 的结果。

打印分数时，如果是整数，请直接输出整数；如果分子和分母可以约分，请约分后再输出。细节请参考样例。

### Solution
重题，解析见[elainafan-从零开始的上机(1)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E4%B8%8A%E6%9C%BA1/#%E5%88%86%E6%95%B0%E7%B1%BB)。

```cpp
#include <iostream>
using namespace std;
int gcd(int a, int b) {  // 计算两个数的最大公约数
    return (!b) ? a : gcd(b, a % b);
}
class Fraction {
    int p, q;

public:
    Fraction(int x) {
        p = x;
        q = 1;
    }
    Fraction() {}
    friend istream &operator>>(istream &is, Fraction &x) {
        is >> x.p >> x.q;
        int d = gcd(x.p, x.q);
        x.p /= d;
        x.q /= d;
        return is;
    }
    friend ostream &operator<<(ostream &os, const Fraction &f) {
        if (f.q == 1)
            os << f.p;
        else
            os << f.p << '/' << f.q;
        return os;
    }
    Fraction operator*(const Fraction &b) {
        Fraction temp;
        temp.p = p * b.p;
        temp.q = q * b.q;
        int d = gcd(temp.p, temp.q);
        temp.p /= d;
        temp.q /= d;
        return temp;
    }
    Fraction operator*(int x) {
        Fraction temp;
        temp.p = x * p;
        temp.q = q;
        int d = gcd(temp.p, temp.q);
        temp.p /= d;
        temp.q /= d;
        return temp;
    }
};

int main() {
    int testcases;
    cin >> testcases;
    while (testcases--) {
        Fraction a, b, two(2);
        cin >> a >> b;
        cout << a << " * " << b << " = " << a * b << endl;
        cout << "2 * " << a << " = " << two * a << endl;
        cout << b << " * 3 = " << b * 3 << endl;
    }
    return 0;
}
```

## 简单的整数类
### 描述
输入两个数 $m,n( 0 \leq m,n \leq 9)$ ，输出它们的乘积。
```cpp
#include <stdio.h>
#include <iostream>
using namespace std;
class MyNum{
public:
    char C;
    MyNum(char c='0'): C(c) {}
// 在此处补充你的代码
};

int main() { 
    char m,n;
    cin >> m >>  n;
    MyNum n1(m), n2(n);
    MyNum n3;
    n3 = n1*n2;
    cout << int(n3) << endl;
    return 0;
}
```
### 输入
两个数， $m,n$ ，确保乘积小于 $10$ 。
```
3 2
```
### 输出
它们的乘积。

```
6
```
### Solution
观察代码，首先可以发现需要重载乘法运算符，同时因为有默认行为不需要重载赋值运算符（其实重载也可以），再实现一个转换到整型的强制类型转换符。

但是有一个点要注意的是，乘积应该转换成什么，由于缺省参数是``0``字符，考虑类中所有的整数都以``0``字符为基准即可。

```cpp
#include <stdio.h>

#include <iostream>

using namespace std;
class MyNum {
public:
    char C;
    MyNum(char c = '0') : C(c) {}
    MyNum operator*(const MyNum &s) {
        int x = C - '0';
        int y = s.C - '0';
        int d = x * y;
        MyNum k;
        k.C = '0' + d;
        return k;
    }
    operator int() { return C - '0'; }
};

int main() {
    char m, n;
    cin >> m >> n;
    MyNum n1(m), n2(n);
    MyNum n3;
    n3 = n1 * n2;
    cout << int(n3) << endl;
    return 0;
}
```