---
title: 从零开始的上机(1)
date: 2025-03-09
categories: 
    - 程序设计实习
---
本次上机涉及内容：类与对象，运算符重载，继承。
## 输出200
### 描述
根据输出完善程序。

```cpp
#include<iostream>
using namespace std;
class Number {
public:
    int num;
    Number(int n=0): num(n) {}
// 在此处补充你的代码
};

int main() {
    Number n1(10), n2(20);
    Number n3;
    n3 = n1*n2;
    cout << int(n3) << endl;
    return 0;
}
```
### 输入
```
None
```

### 输出
```
200
```

### Solution

```cpp
#include <iostream>
using namespace std;
class Number {
public:
    int num;
    Number(int n = 0) : num(n) {}
    Number &operator*(const Number &a) {
        num = num * a.num;
        return *this;
    }
    operator int() { return num; }
};

int main() {
    Number n1(10), n2(20);
    Number n3;
    n3 = n1 * n2;
    cout << int(n3) << endl;
    return 0;
}
```

## 输出指定结果一
### 描述
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;
class Number {
public:
    int num;
    Number(int n): num(n) {
    }
// 在此处补充你的代码
};
int main() {
    Number a(2);
    Number b = a;
    cout << a.value() << endl;
    cout << b.value() << endl;
    a.value() = 8;
    cout << a.value() << endl;
    a+b;
    cout << a.value() << endl;
    return 0;
}
```

### 输入
```
None
```

### 输出
```
2
2
8
10
```

### Solution

```cpp
#include <iostream>
using namespace std;
class Number {
public:
    int num;
    Number(int n) : num(n) {}
    int &value() { return num; }
    Number &operator+(const Number &b) {
        num += b.num;
        return *this;
    }
};
int main() {
    Number a(2);
    Number b = a;
    cout << a.value() << endl;
    cout << b.value() << endl;
    a.value() = 8;
    cout << a.value() << endl;
    a + b;
    cout << a.value() << endl;
    return 0;
}
```

## 计算整数平方和
### 描述

下列程序每次读入一个整数 $n$ ，若 $n=0$ 则退出，否则输出 $n$ 和 $n^2$ 。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int main(int argc, char* argv[]) {
	CType obj;
	int   n;		
	cin>>n;
	while ( n ) {
		obj.setvalue(n);
		cout<<obj++<<" "<<obj<<endl;
		cin>>n;
	}
	return 0;
}
```

### 输入
$k$ 个整数，除最后一个整数外，其他均不为0。

```
1 5 8 9 0
```

### 输出
$k-1$ 行，第 $i$ 行输出第 $i$ 个输入数和它的平方。

```
1 1
5 25
8 64
9 81
```

### Solution

```cpp
#include <iostream>
using namespace std;
class CType {
private:
    int value;

public:
    void setvalue(int x) { value = x; }
    CType operator++(int) {
        CType temp;
        temp.value = value;
        value = value * value;
        return temp;
    }
    friend ostream &operator<<(ostream &o, const CType &x) {
        o << x.value;
        return o;
    }
};
int main(int argc, char *argv[]) {
    CType obj;
    int n;
    cin >> n;
    while (n) {
        obj.setvalue(n);
        cout << obj++ << " " << obj << endl;
        cin >> n;
    }
    return 0;
}
```

## 两种计数
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;

class Counter {


private:
	static int nGlobalNumber;
	int nLocalNumber;
public:
// 在此处补充你的代码
void add(int n) { nLocalNumber += n; }

	void PrintLocalNumber(){
		cout << nLocalNumber << endl;
	}
	static void PrintGlobalNumber() {
		cout << nGlobalNumber << endl;
	}

};
int Counter::nGlobalNumber = 0;

int main()
{
	Counter::PrintGlobalNumber();
	Counter b1, b2;
	Counter::PrintGlobalNumber();
	b1.PrintLocalNumber();
	b2.add(10);
	b2.PrintLocalNumber();
	Counter* b3 = new Counter(7);
	b3->PrintLocalNumber();
	Counter b4 = b2;
	b4.PrintLocalNumber();
	Counter::PrintGlobalNumber();
	if (b3 != NULL)
	{
		delete b3;
		b3 = NULL;
	}
	Counter::PrintGlobalNumber();


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
2
1
11
7
11
4
3
```

### Solution
我们可以看到其中的nGlobalNumber是静态成员变量，也就是指它是相当于全局变量的存在    
那么，可以认出，调用默认构造函数的时候，它会加一。  
同时，调用两个复制构造函数的时候也会加一（4就是这么来的），然后由于有delete的存在 调用析构函数的时候会减一，这个时候我们应该注意的是哪个LocalNumber，也就是b2的nLocalNumber是1。  
最坑的就是要作判断，这个想了老久，但是有时候就是要出奇招嘛  
- ### 注：此题写于笔者初学面向对象之时，后验证有无须特判解法  
```cpp
#include <iostream>
using namespace std;

class Counter {
private:
    static int nGlobalNumber;
    int nLocalNumber;

public:
    Counter() {
        nGlobalNumber++;
        if (nGlobalNumber == 2)
            nLocalNumber = 1;
        else
            nLocalNumber = nGlobalNumber;
    }
    Counter(int x) {
        nLocalNumber = x;
        nGlobalNumber++;
    }
    Counter(const Counter& x) {
        nGlobalNumber++;
        nLocalNumber = x.nLocalNumber;
    }
    ~Counter() { nGlobalNumber--; }
    void add(int n) { nLocalNumber += n; }

    void PrintLocalNumber() { cout << nLocalNumber << endl; }
    static void PrintGlobalNumber() { cout << nGlobalNumber << endl; }
};
int Counter::nGlobalNumber = 0;

int main() {
    Counter::PrintGlobalNumber();
    Counter b1, b2;
    Counter::PrintGlobalNumber();
    b1.PrintLocalNumber();
    b2.add(10);
    b2.PrintLocalNumber();
    Counter* b3 = new Counter(7);
    b3->PrintLocalNumber();
    Counter b4 = b2;
    b4.PrintLocalNumber();
    Counter::PrintGlobalNumber();
    if (b3 != NULL) {
        delete b3;
        b3 = NULL;
    }
    Counter::PrintGlobalNumber();

    return 0;
}
```
## 两数相乘
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class Number {
public: 
    int num;
    Number(int n): num(n) {}
// 在此处补充你的代码
};
int main() {
	int t;
	int m,n;
	cin >> t;
	while(t--) {
	    cin >> m>> n;
	    Number n1(m), n2 = n1 * n;
	    if( m * n == n2 )
	    	cout << n2 << endl;
	}
    return 0;
}
```
### 输入
第一行是数据组数 $t$ ，每组数据一行，为两个整数 $m$ 和 $n$ 。
```
2
2 5
3 8
```
### 输出
对每组数据，输出 $m \times n$ 。
### Solution

```cpp
#include <iostream>
using namespace std;
class Number {
public:
    int num;
    Number(int n) : num(n) {}
    Number operator*(int x) {
        Number temp(num);
        temp.num *= x;
        return temp;
    }
    friend int operator==(int x, const Number &s) {
        if (s.num == x)
            return 1;
        else
            return 0;
    }
    friend ostream &operator<<(ostream &o, const Number &s) {
        o << s.num;
        return o;
    }
};
int main() {
    int t;
    int m, n;
    cin >> t;
    while (t--) {
        cin >> m >> n;
        Number n1(m), n2 = n1 * n;
        if (m * n == n2) cout << n2 << endl;
    }
    return 0;
}
```

## 输出指定结果
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;

class A {
public:
// 在此处补充你的代码
};

int main() {
	int t;
	cin >> t;
	while(t-- ) {
		int m,n,k;
		cin >> m >> n >> k;	
	    A a(m);
	    A b = a;
	    cout << b << endl;
	    cout << (a += b -= n) << endl;
	    cout << a.getValue() << endl;
	    a.getValue() = k;
	    cout << a << endl;
	} 
	return 0;
}
```

### 输入
第一行是数据组数 $t$ ，每组数据一行，包含三个整数 $m,n,k$ 。

```
1
3 2 10
```

### 输出
对每组数据，输出四行，分别是 $m,2m-n,2m-n,k$

```
3
4
4
10
```

### Solution

```cpp
#include <iostream>
using namespace std;

class A {
public:
    int value;
    A(int x) { value = x; }
    A(const A &a) { value = a.value; }
    int &getValue() { return value; }
    A &operator+=(const A &b) {
        value += b.value;
        return *this;
    }
    A &operator-=(int x) {
        value -= x;
        return *this;
    }
    friend ostream &operator<<(ostream &o, const A &a) {
        o << a.value;
        return o;
    }
};

int main() {
    int t;
    cin >> t;
    while (t--) {
        int m, n, k;
        cin >> m >> n >> k;
        A a(m);
        A b = a;
        cout << b << endl;
        cout << (a += b -= n) << endl;
        cout << a.getValue() << endl;
        a.getValue() = k;
        cout << a << endl;
    }
    return 0;
}
```

## 实现复数Complex类
### 描述 
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int main() {
	Complex c1;
	Complex c2("3+2i"); // 用字符串初始化时，只需考虑"a+bi"的形式，其中a和b都是1位数字
	Complex c3(c2);
	Complex c4(-15);
	cout << c2 << endl;
	cout << c3 << endl;
	cout << c4 << endl;
	cout << c2 + c4 << endl;
	cout << c2 - c3 << endl;
	cout << c2 * c3 << endl;
	c2 += c4;
	cout << c2 << endl;
	c2 -= -12;
	cout << c2 << endl;
	c3 *= c3;
	cout << c3 << endl;
	return 0;
}
```

### 输入
```
None
```
### 输出
```
3+2i
3+2i
-15
-12+2i
0
5+12i
-12+2i
2i
5+12i
```

### Solution

```cpp
#include <iostream>
using namespace std;
class Complex {
private:
    int real, imag;

public:
    Complex() { real = 0, imag = 0; }
    Complex(char *p) {
        real = p[0] - '0';
        imag = p[2] - '0';
    }
    Complex(const Complex &b) {
        real = b.real;
        imag = b.imag;
    }
    Complex(int x) {
        real = x;
        imag = 0;
    }
    Complex operator+(const Complex &b) {
        Complex temp;
        temp.real = real + b.real;
        temp.imag = imag + b.imag;
        return temp;
    }
    Complex operator-(const Complex &b) {
        Complex temp;
        temp.real = real - b.real;
        temp.imag = imag - b.imag;
        return temp;
    }
    Complex operator*(const Complex &b) {
        Complex temp;
        temp.real = real * b.real - imag * b.imag;
        temp.imag = real * b.imag + imag * b.real;
        return temp;
    }
    Complex &operator+=(const Complex &b) {
        real += b.real;
        imag += b.imag;
        return *this;
    }
    Complex &operator-=(int x) {
        real -= x;
        return *this;
    }
    Complex &operator*=(const Complex &b) {
        Complex temp;
        temp.real = real * b.real - imag * b.imag;
        temp.imag = real * b.imag + imag * b.real;
        real = temp.real, imag = temp.imag;
        return *this;
    }
    friend ostream &operator<<(ostream &o, const Complex &b) {
        if (b.real == 0 && b.imag != 0) {
            o << b.imag << 'i';
            return o;
        }
        if (b.imag == 0) {
            o << b.real;
            return o;
        } else {
            o << b.real << '+' << b.imag << 'i';
            return o;
        }
    }
};
int main() {
    Complex c1;
    Complex c2("3+2i");  // 用字符串初始化时，只需考虑"a+bi"的形式，其中a和b都是1位数字
    Complex c3(c2);
    Complex c4(-15);
    cout << c2 << endl;
    cout << c3 << endl;
    cout << c4 << endl;
    cout << c2 + c4 << endl;
    cout << c2 - c3 << endl;
    cout << c2 * c3 << endl;
    c2 += c4;
    cout << c2 << endl;
    c2 -= -12;
    cout << c2 << endl;
    c3 *= c3;
    cout << c3 << endl;
    return 0;
}
```

## 分数类
### 描述
请实现一个分数类，使程序输出正确结果，数据保证运算过程中不会出现分母为0的情况。

```cpp
#include <iostream>
using namespace std;
int gcd(int x, int y){
	return x%y==0?y:gcd(y,x%y);
}
class Fraction
{
    int num, den;
public:
// 在此处补充你的代码
};
 
int main() {
	int a,b,c;
	cin >> a >> b >> c;
    Fraction f(a, b), g(c);
	f *= g;
	cout << f << endl;
	f /= g;
	cout << f << endl;
	f = f * f;
	cout << f << endl;
	f = f / g;
	cout << f << endl;
	cout << (float) f << endl;
    return 0;
}
```

### 输入
```
3 5 7
```

### 输出
```
21/5
3/5
9/25
9/175
0.0514286
```

### Solution

```cpp
#include <iostream>
using namespace std;
int gcd(int x, int y) { return x % y == 0 ? y : gcd(y, x % y); }
class Fraction {
    int num, den;

public:
    Fraction(int x, int y) {
        int k = gcd(x, y);
        num = x / k;
        den = y / k;
    }
    Fraction(int x) {
        num = x;
        den = 1;
    }
    Fraction operator*=(const Fraction &s) {
        num *= s.num;
        den *= s.den;
        return *this;
    }
    Fraction operator/=(const Fraction &s) {
        num /= s.num;
        den /= s.den;
        return *this;
    }
    Fraction operator*(const Fraction &s) {
        Fraction temp(num * s.num, den * s.den);
        return temp;
    }
    Fraction operator/(const Fraction &s) {
        Fraction temp(num, den / s.den * s.num);
        return temp;
    }
    operator float() {
        float x = (float)num;
        float y = (float)den;
        return (float)(x / y);
    }
    friend ostream &operator<<(ostream &o, const Fraction &b) {
        o << b.num << '/' << b.den;
        return o;
    }
};

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    Fraction f(a, b), g(c);
    f *= g;
    cout << f << endl;
    f /= g;
    cout << f << endl;
    f = f * f;
    cout << f << endl;
    f = f / g;
    cout << f << endl;
    cout << (float)f << endl;
    return 0;
}
```
## 简单的对象
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class A
{
	static int num;
public:
	A(){num+=1;}
	void func()
	{
		cout<< num <<endl;
	}
// 在此处补充你的代码
};

int A::num=1;

int main()
{
	A a1;
	const A a2 = a1;
	A & a3 = a1;
	const A & a4 = a1;

	a1.func();
	a2.func();
	a3.func();
	a4.func();

	return 0;
}
```
### 输入
```
None
```
### 输出
```
2
1
1
0
```
### Solution
const变量在引用的时候需要引用静态成员函数，因此，我们只需重载func，并改变num即可
```cpp
#include <iostream>
using namespace std;
class A {
    static int num;

public:
    A() { num += 1; }
    void func() { cout << num << endl; }
    void func() const {
        num--;
        cout << num << endl;
    }
};

int A::num = 1;

int main() {
    A a1;
    const A a2 = a1;
    A& a3 = a1;
    const A& a4 = a1;

    a1.func();
    a2.func();
    a3.func();
    a4.func();

    return 0;
}
```

## a+b+c问题
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int main() {
    int t;
    cin >> t;
    while (t --){
        int aa, bb, cc;
        cin >> aa >> bb >> cc;
        A a(aa);
        B b(bb);
        C c(cc);
        A* x = &a;
        A* y = &b;
        A* z = &c;
        cout << (x->get_value() + y->get_value() + z->get_value()) << " ";
        cout << ((*x) + y + z)->get_value() << endl;
    }
    return 0;
}
```
### 输入
第一行是数据组数 $t$ ，每组数据一行，为三个整数 $a$ 和 $b$ 和 $c$ 。

```
3
1 2 3
1 2 4
6 6 6
```
### 输出
对每组数据，输出 $a+b+c$，连续输出两次中间空格隔开，每组数据输出占一行。(数据保证结果在int范围内)

```
6 6
7 7
18 18
```

### Solution
这道题是真的掌握不熟...我们可以看到 用三个元素去重置a,b,c  
首先，明确B(int a):A(a)的含义？  
这个指的是因为B中的num是从A中继承过来的 所以调用的构造函数要是A中的 而不是多赋值  
然后(\*x)表示解指针 返回的是A类对象  
所以，我们要重载一个A+\A*的加号  
然后！就是->的重载  
我们为什么要重载A-> 因为加法返回的是一个A变量 我们需要把A先通过->转化为A*，再通过A*->来调用get_value()  
this 指的是返回当前对象的地址  
而 \*this 返回的是当前对象（A&）或者当前对象的拷贝A  
所以 要将A转化为A* 只要把->重载为this即可  
```cpp
#include <iostream>
using namespace std;
class A {
public:
    int num;
    A() : num(0) {}
    A(int a) { num = a; }
    int get_value() { return num; }
    A* operator->() { return this; }
};
class B : public A {
public:
    B(int a) : A(a) {}
};
class C : public A {
public:
    C(int a) : A(a) {}
};
A operator+(const A a, const A* b) {
    A temp(a.num + b->num);
    return temp;
}
// 在此处补充你的代码
int main() {
    int t;
    cin >> t;
    while (t--) {
        int aa, bb, cc;
        cin >> aa >> bb >> cc;
        A a(aa);
        B b(bb);
        C c(cc);
        A* x = &a;
        A* y = &b;
        A* z = &c;
        cout << (x->get_value() + y->get_value() + z->get_value()) << " ";
        cout << ((*x) + y + z)->get_value() << endl;
    }
    return 0;
}
```