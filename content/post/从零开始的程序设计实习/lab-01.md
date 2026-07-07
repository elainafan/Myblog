---
title: 从零开始的上机(1)
date: 2025-03-09
categories: 
    - 算法
slug: 从零开始的上机1
hidden: true
seriesOrder: 5
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
显然地，由于转换构造函数实现了缺省，因此不需额外实现默认构造函数。

只需要重载``Number``类的乘法运算符，再实现``int``的强制类型转换即可。

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
观察``main``函数，可以发现需要重载一个拷贝构造函数，一个转换构造函数，实现``value``函数，以及重载一个``Number``类之间的加法运算符。

需要注意的是，由于``a.value()=8``这一句可以得出``value``返回的应该是一个引用类型。

下面的代码没有实现拷贝构造函数，因为编译器会默认地将全部的成员变量都复制一遍，建议还是实现一下以养成好习惯。

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
可以观察到，需要实现一个名为``CType``的类，这个类通过``setvalue``函数接收参数。

同时，需要重载对应类的输出运算符，这在前面的博文中讲过，此处不多介绍。

然后就是需要重载一个``后自加``运算符，由于是后自加，因此此处返回的应该是一个与原对象相同的临时变量，而此处的自加在题目意义下相当于乘方，就可以解决了。

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
下面介绍的第一种做法不是正解，是考试的时候实在做不出来的一种技巧，想要看正解可以直接移步第二种方法。

可以看到``nGlobalNumber``是静态成员变量，也就是指它是相当于全局变量的存在。

那么从给定的样例可以读出，调用默认构造函数的时候，它会加一（从这个名字也可以看出来）。

同时可以读出，调用两个``转换构造函数``的时候，它也会加一（4就是这么来的），然后由于有``delete``的存在 调用析构函数的时候会减一。

根据样例或者变量名，可以读出``LocalNumber``应该是某个时间，例如创建对象时的``GlobalNumber``，然后进一步得出其关系。

如果赛时注意不到正确解法的话，可以采取某种特判的方法。例如，笔者好像在上机的时候就卡题了，然后就采用了特判，这种方法如果真正考试碰到也许可以救一命，但是平时练习还是建议看正解。 
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

下面是正解部分，一开始的讲解与原答案相同，唯一不同的就是默认构造函数的处理方式，没错，就是将``nLocalNumber``赋值为1！想不到吧，笔者就是^(*￣(oo)￣)^。

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
        nLocalNumber = 1;
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
    system("pause");
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
观察代码，可以发现需要重载一个乘法运算符，同时需要重载一个等号运算符，以及一个输出运算符。

需要注意的是，由于等号运算符的左操作数是整型，因此需要使用友元，因为编译器会先寻找左操作数的相关运算符，找不到就会报错，从而需要将这个运算符重载为普通函数，但又要放到类中，为使它能访问类的私有变量，需要使用友元。

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

## 输出指定结果二
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
观察代码，需要实现``A``的拷贝构造函数和转换构造函数，由于没有调用默认构造函数，因此无需实现默认构造函数。

同时，需要重载输出运算符，输出对应的``A``类对象。

再往下看，需要重载``+=``和``-=``运算符，同时它们返回的应该是引用类型，以实现链式调用。``getValue()``函数也应该返回引用，道理同上。

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
首先，根据高中数学知识，这个类一定有实部和虚部两个成员变量。

随后需要实现默认构造函数，字符串的转换构造函数，整型的转换构造函数，以及拷贝构造函数。

然后还需要重载输出运算符，``复数类之间的加、减、乘运算符``，``复数类之间的+=和*=运算符``、``复数类与整型的-=运算符``，即可。注意返回的是对象还是引用，这点不要搞错。

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
题目由于没有引入相关库，因此无法使用``__gcd``函数，不过非常好心地为我们提供了一个``gcd``函数，以便约分。

根据小学数学知识，分数类需要有分母和分子作为成员变量，如果是整数分母为1。

观察代码，需要实现``给定分子、分母``的转换构造函数，``给定分子、分母为1``的转换构造函数，其实可以使用缺省参数来写，这里为了清晰就写了两个。

随后，需要重载``*=、/=、*、/``这些运算符，由于没有链式调用，返回对象或者引用都没太大关系。

再往下看，还需要重载输出运算符和``float``强制类型转换函数，就做完了。

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
观察给定代码，发现``num``作为静态成员变量，可以看做全局的变量。

同时，根据输出可以观察到，``a2``和``a4``执行``func``时，将``num``减一并输出当前的``num``。

考虑到，这两个变量/引用的类型都是``const``，回想起非``const``对象优先匹配``非const成员函数``，``const``对象只能调用``const成员函数``，因此此时应该重载一个``func``，以``const成员函数的形式``。

注意，``const``函数不能改``this``指针指向的对象，但是``static``成员不属于对象，因此可以修改。
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
这道题算是比较难的题。

首先，要实现``A``、``B``、``C``三个类，且由下面的指针类型可以看出，它们应该是相互继承的关系，同时基类``A``还应该有``get_value``成员函数跟``num``成员变量，同时有转换构造函数和默认构造函数。相应地，在``B``类和``C``类的构造函数中也应该有``A``类的构造。

往下看，输出的第一行没有什么问题，但是第二行报错了，首先可以看到，它先将``x``解引用得到一个``A``类型变量，再与``y``跟``z``两个``A*``指针相加，因此这里必须重载这个加号。

可以发现，由于这里是链式调用，因此这个加号的返回类型，应该是一个``A``类型，笔者此处将其写在类外，应该封装进类里也是对的。

这时候会发现，``A``类型无法使用``->``运算符调用``get_value()``函数，而这样调用的应该是一个``A*``类型变量，此时选择重载``->``运算符，让它返回一个``A*``变量，也就是``this``指针。

比较令人费解的事情在于，这里只有一个``->``运算符，返回了一个``A*``变量后，剩下的部分怎么办呢？事实上，编译器这里拿到它后，相当于实现了``obj.operator->()->get_value()``，这样就可以调用了。
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