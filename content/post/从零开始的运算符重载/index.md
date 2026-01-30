---
title: 从零开始的运算符重载
date: 2025-02-26
categories:
    - 程序设计实习
---
## MyString
### 描述
补足MyString类，使程序输出指定结果

```cpp
#include <iostream>
#include <string>
#include <cstring>
using namespace std;
class MyString {
	char * p;
public:
	MyString(const char * s) {
		if( s) {
			p = new char[strlen(s) + 1];
			strcpy(p,s);
		}
		else
			p = NULL;

	}
	~MyString() { if(p) delete [] p; }
// 在此处补充你的代码
};
int main()
{
	char w1[200],w2[100];
	while( cin >> w1 >> w2) {
		MyString s1(w1),s2 = s1;
		MyString s3(NULL);
		s3.Copy(w1);
		cout << s1 << "," << s2 << "," << s3 << endl;

		s2 = w2;
		s3 = s2;
		s1 = s3;
		cout << s1 << "," << s2 << "," << s3 << endl;
		
	}
}
```
### 输入
多组数据，每组一行，是两个不带空格的字符串

```
abc def
123 456
```
### 输出
对每组数据，先输出一行，打印输入中的第一个字符串三次  

然后再输出一行，打印输入中的第二个字符串三次

```
abc,abc,abc
def,def,def
123,123,123
456,456,456
```
### Solution
可以看到的是，题目已经帮我们写好了一个转换构造函数和一个析构函数，由于有``MyString s2=s1``这一行，还需要再写一个拷贝构造函数。

同时，还能观察到，要重载``=``运算符和输出运算符，注意输出运算符需要使用友元函数声明``friend``，因为需要允许``标准IO类``访问这个类的**私有成员**。

接着，还需要加入``Copy``这个成员函数，直接将成员变量全部赋值即可。

```cpp
#include <cstring>
#include <iostream>
#include <string>

using namespace std;
class MyString {
    char *p;

public:
    MyString(const char *s) {
        if (s) {
            p = new char[strlen(s) + 1];
            strcpy(p, s);
        } else
            p = NULL;
    }
    ~MyString() {
        if (p) delete[] p;
    }
    MyString(const MyString &s) {
        if (s.p) {
            p = new char[strlen(s.p) + 1];
            strcpy(p, s.p);
        } else {
            p = NULL;
        }
    }
    MyString &operator=(const MyString &s) {
        if (s.p) {
            if (p) delete[] p;
            p = new char[strlen(s.p) + 1];
            strcpy(p, s.p);
        } else {
            p = NULL;
        }
        return *this;  // 这行老忘写
    }
    void Copy(const MyString &s) {
        if (p) delete[] p;
        if (s.p) {
            p = new char[strlen(s.p) + 1];
            strcpy(p, s.p);
        } else {
            p = NULL;
        }
    }
    friend ostream &operator<<(ostream &os, MyString &s) {
        if (s.p) {
            os << s.p;
        }
        return os;
    }
};
int main() {
    char w1[200], w2[100];
    while (cin >> w1 >> w2) {
        MyString s1(w1), s2 = s1;
        MyString s3(NULL);
        s3.Copy(w1);
        cout << s1 << "," << s2 << "," << s3 << endl;

        s2 = w2;
        s3 = s2;
        s1 = s3;
        cout << s1 << "," << s2 << "," << s3 << endl;
    }
}
```
## 看上去好坑的运算符重载
### 描述
根据输出完善程序。

```cpp
#include <iostream> 
using namespace std;
class MyInt 
{ 
	int nVal; 
	public: 
	MyInt( int n) { nVal = n ;}
// 在此处补充你的代码
}; 
int Inc(int n) {
	return n + 1;
}
int main () { 
	int n;
	while(cin >>n) {
		MyInt objInt(n); 
		objInt-2-1-3; 
		cout << Inc(objInt);
		cout <<","; 
		objInt-2-1; 
		cout << Inc(objInt) << endl;
	}
	return 0;
}
```
### 输入
多组数据，每组一行，整数 $n$

```
20
30
```
### 输出
对每组数据，输出一行，包括两个整数， $n-5$ 和 $n-8$

```
15,12
25,22
```
### Solution
观察代码，由``ObjInt``这一行，发现需要重载一个减号，而且因为它作为语句，应该直接对该对象进行修改，因此应该返回一个引用，也就是``*this``，这样就可以实现链式调用了。

同时，在``Inc``函数中，一个``MyInt``型对象作为``int``型对象被传入，因此需要重载它的强制类型转换函数。

```cpp
#include <iostream>
using namespace std;
class MyInt {
    int nVal;

public:
    MyInt(int n) { nVal = n; }
    MyInt &operator-(int x) {
        nVal = nVal - x;
        return *this;
    }
    operator int() { return nVal; }
    // 在此处补充你的代码
};
int Inc(int n) { return n + 1; }
int main() {
    int n;
    while (cin >> n) {
        MyInt objInt(n);
        objInt - 2 - 1 - 3;
        cout << Inc(objInt);
        cout << ",";
        objInt - 2 - 1;
        cout << Inc(objInt) << endl;
    }
    return 0;
}
```
## 惊呆！Point竟然能这样输入输出
### 描述
根据输出完善程序。

```cpp
#include <iostream> 
using namespace std;
class Point { 
	private: 
		int x; 
		int y; 
	public: 
		Point() { };
// 在此处补充你的代码
}; 
int main() 
{ 
 	Point p;
 	while(cin >> p) {
 		cout << p << endl;
	 }
	return 0;
}
```
### 输入
多组数据，每组两个整数

```
2 3
4 5
```
### 输出
对每组数据，输出一行，就是输入的两个整数

```
2,3
4,5
```
### Solution 
观察``main``函数，发现需要重载输入和输出两个运算符，它们都需要使用**友元**声明。

同时，需要注意``istream``输入的重载是不能使用``const``引用的，而应该直接使用引用，因为它会修改当前对象的成员变量！

```cpp
#include <iostream>
using namespace std;
class Point {
private:
    int x;
    int y;

public:
    Point() {};
    friend istream &operator>>(istream &is, Point &p) {
        is >> p.x >> p.y;
        return is;
    }  // 输入不能有const
    friend ostream &operator<<(ostream &os, const Point &p) {
        os << p.x << ',' << p.y;
        return os;
    }
    // 在此处补充你的代码
};
int main() {
    Point p;
    while (cin >> p) {
        cout << p << endl;
    }
    return 0;
}
```
## 二维数组类
### 描述
根据输出，完善二维数组类Array2。

```cpp
#include <iostream>
#include <cstring>
using namespace std;

class Array2 {
// 在此处补充你的代码
};

int main() {
    Array2 a(3,4);
    int i,j;
    for(  i = 0;i < 3; ++i )
        for(  j = 0; j < 4; j ++ )
            a[i][j] = i * 4 + j;
    for(  i = 0;i < 3; ++i ) {
        for(  j = 0; j < 4; j ++ ) {
            cout << a(i,j) << ",";
        }
        cout << endl;
    }
    cout << "next" << endl;
    Array2 b;     b = a;
    for(  i = 0;i < 3; ++i ) {
        for(  j = 0; j < 4; j ++ ) {
            cout << b[i][j] << ",";
        }
        cout << endl;
    }
    return 0;
}
```
### 输入
```
None
```
### 输出
```
0,1,2,3,
4,5,6,7,
8,9,10,11,
next
0,1,2,3,
4,5,6,7,
8,9,10,11,
```
### Solution
这题在前期算是比较难的题目，这里作重点讲解，主要是要从给定代码中提取出要实现什么。

首先观察主函数，发现需要一个转换构造函数，声明给定长宽的``Array2``型对象。

接着，由``a[i][j]=i*4+j``这句，需要重载``[]``运算符。

随后，由``cout<<a(i,j)<<",";``这句，需要重载括号运算符，它应该输出一个``int&``引用便于``<<``传入（见上题）。

最后，由于``b=a``这句，需要重载赋值运算符。

下面开始实现，由于是二维数组，因此应该使用二维指针并用两个整型变量存长宽，也可以使用一维指针+新类对象（这个类的成员变量中含有一维指针），但是此题后者比较麻烦，因此不需要。

注意读者在学到这里的时候大概率还没有学``malloc``函数，因此这里要说明的是，无论是``malloc``还是``new``，都是针对一维指针而言，因此需要循环拓展堆内存。

随后，``[]``运算符应该返回``int*``型变量，即一行（因为``int*``类有自带的``[]``运算符），``()``运算符应该返回``int&``型变量，``=``运算符应该返回``Array2&``型变量，即使用``*this``指针，以便实现``a=b=c``的链式结构。

```cpp
##include <cstring>
#include <iostream>

using namespace std;

class Array2 {
private:
    int x, y;  // y才是行宽
    int **p;   // 指针要注意
public:
    Array2() {}
    Array2(int a, int b) {
        x = a;
        y = b;
        if (a > 0 && b > 0) {
            p = new int *[x];
            for (int i = 0; i < y; i++) {
                p[i] = new int[y];
            }
        } else {
            p = NULL;
        }
    }
    int *operator[](int t) {
        return p[t];  // 从p的位置开始，偏移了多少个变量
    }
    int &operator()(int a, int b) { return p[a][b]; }
    Array2 &operator=(const Array2 &b) {
        x = b.x;
        y = b.y;
        if (x > 0 && y > 0) {
            p = new int *[x];
            for (int i = 0; i < x; i++) {
                p[i] = new int[y];
                for (int j = 0; j <= y; j++) {
                    p[i][j] = b.p[i][j];
                }
            }
        } else {
            p = NULL;
        }
        return *this;
    }
    // 在此处补充你的代码
};

int main() {
    Array2 a(3, 4);
    int i, j;
    for (i = 0; i < 3; ++i)
        for (j = 0; j < 4; j++) a[i][j] = i * 4 + j;
    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 4; j++) {
            cout << a(i, j) << ",";
        }
        cout << endl;
    }
    cout << "next" << endl;
    Array2 b;
    b = a;
    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 4; j++) {
            cout << b[i][j] << ",";
        }
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## 别叫，这个大整数已经很简化了!
### 描述
根据输出完善程序。

```cpp
#include <iostream> 
#include <cstring> 
#include <cstdlib> 
#include <cstdio> 
using namespace std;
const int MAX = 110; 
class CHugeInt {
// 在此处补充你的代码
};
int  main() 
{ 
	char s[210];
	int n;

	while (cin >> s >> n) {
		CHugeInt a(s);
		CHugeInt b(n);

		cout << a + b << endl;
		cout << n + a << endl;
		cout << a + n << endl;
		b += n;
		cout  << ++ b << endl;
		cout << b++ << endl;
		cout << b << endl;
	}
	return 0;
}
```
### 输入
多组数据，每组数据是两个非负整数 $s$ 和 $n$ 。$s$ 最多可能200位， $n$ 用int能表示。

```
99999999999999999999999999888888888888888812345678901234567789 12
6 6
```
### 输出
对每组数据，输出6行，内容对应程序中6个输出语句。

```
99999999999999999999999999888888888888888812345678901234567801
99999999999999999999999999888888888888888812345678901234567801
99999999999999999999999999888888888888888812345678901234567801
25
25
26
12
12
12
13
13
14
```
### Solution
这题其实思维难度并不大，首先观察主函数，需要实现字符串和整型的转换构造函数。

然后很显然地，需要重载这个大整数类的友元输出运算符。

同时，观察给定的几句代码，需要重载``两个大整数类对象之间的加法运算符``、``大整数类在前、整数类在后的加法运算符``、``整数类在前、大整数类在后的加法运算符``、``大整数类的+=运算符``、``大整数类前自加运算符``、``大整数类后自加运算符``。

需要注意的是，仍然由于链式调用的原因，实现``大整数类在前、整数类在后的加法运算符``时建议返回引用，同时``前自加``没有空的``int``占位，且可以直接返回原对象的引用，而``后自加``则需要返回临时保存的对象，最后``整数类在前、大整数类在后的加法运算符``需要使用友元函数，因为编译器会先匹配左操作数，而这里的左操作数是``整型``，匹配不到合适的运算符，因此这个运算符本应是作为``普通函数``出现，但是此时需要把它封装到类里并能访问``private成员变量``，因此需要使用友元。

最后，联想到计概中学过的高精度，实现即可。
```cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
using namespace std;
const int MAX = 110;
class CHugeInt {
private:
    int c[210];
    int len;

public:
    CHugeInt() {
        len = 0;
        memset(c, 0, sizeof(c));
    }
    CHugeInt(char s[]) {
        memset(c, 0, sizeof(c));
        int l = strlen(s);
        for (int i = 0; i <= l - 1; i++) {
            c[i] = s[i] - '0';
        }
        len = l;
        int i = 0, j = len - 1;
        while (i < j) {
            swap(c[i], c[j]);
            i++;
            j--;
        }
    }
    CHugeInt(int n) {
        memset(c, 0, sizeof(c));
        int tem = n;
        len = 0;
        while (tem > 0) {
            c[len++] = tem % 10;
            tem /= 10;
        }
    }
    CHugeInt operator+(const CHugeInt &s) {
        CHugeInt temp;
        temp.len = max(len, s.len);
        for (int i = 0; i <= temp.len - 1; i++) {
            temp.c[i] = c[i] + s.c[i];
        }
        for (int i = 0; i <= temp.len - 1; i++) {
            if (temp.c[i] / 10) {
                temp.c[i + 1] += temp.c[i] / 10;
                temp.c[i] %= 10;
            }
        }
        if (temp.c[temp.len]) temp.len++;
        return temp;
    }
    CHugeInt &operator+(const int n) {
        CHugeInt temp(n);
        *this = this->operator+(temp);
        return *this;
    }
    CHugeInt &operator+=(int n) {
        CHugeInt temp(n);
        *this = this->operator+(temp);
        return *this;
    }
    CHugeInt &operator++() {
        CHugeInt temp(1);
        *this = this->operator+(temp);
        return *this;
    }
    CHugeInt operator++(int) {
        CHugeInt temp;
        for (int i = 0; i <= len - 1; i++) {
            temp.c[i] = c[i];
        }
        temp.len = len;
        *this = this->operator+(1);
        return temp;
    }
    friend CHugeInt operator+(int n, CHugeInt s) {
        CHugeInt temp(n);
        s = s + temp;
        return s;
    }
    friend ostream &operator<<(ostream &os, const CHugeInt &s) {
        for (int i = s.len - 1; i >= 0; i--) {
            os << s.c[i];
        }
        return os;
    }
};
int main() {
    char s[210];
    int n;

    while (cin >> s >> n) {
        CHugeInt a(s);
        CHugeInt b(n);

        cout << a + b << endl;
        cout << n + a << endl;
        cout << a + n << endl;
        b += n;
        cout << ++b << endl;
        cout << b++ << endl;
        cout << b << endl;
    }
    return 0;
}
```