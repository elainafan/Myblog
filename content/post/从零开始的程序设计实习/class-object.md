---
title: 从零开始的类与对象
date: 2025-02-19
categories:
    - 程序设计实习
slug: 从零开始的类与对象
hidden: true
seriesOrder: 1
---
## 学生信息处理程序
### 描述
实现一个学生信息处理程序，计算一个学生的四年平均成绩。

要求实现一个代表学生的类，并且类中所有成员变量都是**私有的**。

补充下列程序中的 Student 类以实现上述功能。

```cpp
#include <iostream>
#include <string>
#include <cstdio>
#include <cstring>
#include <sstream>
#include <cstdlib>
using namespace std;

class Student {
// 在此处补充你的代码
};

int main() {
	Student student;        // 定义类的对象
	student.input();        // 输入数据
	student.calculate();    // 计算平均成绩
	student.output();       // 输出数据
}
```

### 输入
输入数据为一行，包括：

姓名,年龄,学号,第一学年平均成绩,第二学年平均成绩,第三学年平均成绩,第四学年平均成绩。

其中姓名为由字母和空格组成的字符串（输入保证姓名不超过20个字符，并且空格不会出现在字符串两端），年龄、学号和学年平均成绩均为非负整数。信息之间用逗号隔开。

```
Tom Hanks,18,7817,80,80,90,70
```

### 输出
输出一行数据，包括：

姓名,年龄,学号,四年平均成绩。

信息之间用逗号隔开。

```
Tom Hanks,18,7817,80
```

### 提示
必须用类实现，其中所有成员变量都是私有的。

输出结果中，四年平均成绩不一定为整数。

### Solution
观察原代码，可以看到``Student``类有``input``、``calculate``、``output``三个成员函数。

而根据题意，需要记录姓名（字符串形式）、年龄、学号、以及四个学年的平均成绩，它们都是``Student``类中的``Private``变量，即无法被除``Student``类外的代码访问。

这里笔者当时完成的时候使用字符数组进行编写，是因为``cstring``这个库中不存在``string``类，因此无法使用``string``类进行快速编写。

```cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

class Student {
private:
    char c[25];
    char x;
    int age;
    int n = 0;
    int num;
    int aver_1;
    int aver_2;
    int aver_3;
    int aver_4;
    double aver;

public:
    void input() {
        while (c[++n] = getchar()) {
            if (c[n] == ',') {
                n--;
                break;
            }
        }
        cin >> age >> x >> num >> x >> aver_1 >> x >> aver_2 >> x >> aver_3 >> x >> aver_4;
    }
    void calculate() { aver = (double)((aver_1 + aver_2 + aver_3 + aver_4) / 4.0); }
    void output() {
        for (int i = 1; i <= n; i++) {
            cout << c[i];
        }
        cout << ',' << age << ',' << num << ',' << aver;
    }
};

int main() {
    Student student;      // 定义类的对象
    student.input();      // 输入数据
    student.calculate();  // 计算平均成绩
    student.output();     // 输出数据
}
```

## Complex类的成员函数
### 描述

请根据输出补足``Complex``类的成员函数，不能加成员变量。

```cpp
#include <iostream>
#include <cstring>
#include <cstdlib>
using namespace std;
class Complex {
private:
    double r,i;
public:
    void Print() {
        cout << r << "+" << i << "i" << endl;
    }
// 在此处补充你的代码
};
int main() {
    Complex a;
    a = "3+4i"; a.Print();
    a = "5+6i"; a.Print();
    return 0;
}
```

### 输入 

```
None
```
### 输出

```
3+4i
5+6i
```

### Solution
可以观察到这里需要写出一个构造函数，使得字符数组或者``string``类被转为一个``Complex``类对象，来实现程序功能。

也许学到后面的你会问，为什么这里是实现构造函数而不是重载等号运算符？事实上，构造函数的原理就是，首先它发现右边不是Complex类对象，因此尝试将其``隐式转换``为一个Complex类对象，再创建一个默认的``Complex复制构造函数``进行调用，将成员变量一一复制。

于是，只需要将这个字符串拆开即可，笔者当时完成的时候仍是使用字符数组。

由于创建了转换构造函数，因此系统不会生成默认构造函数，从而``Complex a``这一句会报错，此时需要新建一个空的默认构造函数。

```cpp
#include <cstdlib>
#include <cstring>
#include <iostream>

using namespace std;
class Complex {
private:
    double r, i;

public:
    void Print() { cout << r << "+" << i << "i" << endl; }
    Complex() {}
    Complex(char c[]) {
        r = c[0] - '0';
        i = c[2] - '0';
    }
};
int main() {
    Complex a;
    a = "3+4i";
    a.Print();
    a = "5+6i";
    a.Print();
    return 0;
}
```

## Apple
### 描述

根据以下输出完善程序。

```cpp
#include <iostream>
using namespace std;
class Apple {
// 在此处补充你的代码
static void PrintTotal() {
		cout << nTotalNumber << endl; 
	}

};
int Apple::nTotalNumber = 0;
Apple Fun(const Apple & a) {
	a.PrintTotal();
	return a;
}
int main()
{
	Apple * p = new Apple[4];
	Fun(p[2]);
	Apple p1,p2;
	Apple::PrintTotal ();
	delete [] p;
	p1.PrintTotal ();
	return 0;
}
```

### 输入 

```
None
```
### 输出

```
4
5
1
```

### Solution
先观察程序，程序中``nTotalNumber``必然是一个静态成员变量，它只有一个并且不属于任何类对象，同时``PrintTotal``函数作为静态成员函数，负责打印出这个变量。

再看主函数，首先创建了一个类型为``Apple``，4个变量的数组，指针``p``指向下标0，然后通过``Fun``函数打印出``nTotalNumber``的值，注意它这里是值返回，并且调用的是``拷贝构造函数``，再新建两个``Apple``类变量并打印出值，然后再删除一个``Apple``数组并打印出值。

根据样例很容易看出，逻辑应该是默认构造函数使``nTotalNumber``加一，然后析构函数使``nTotalNumber``减一，而``Fun``中由于返回值调用拷贝构造函数后作为临时变量被析构，因此``nTotalNumber``是减一的。

```cpp
#include <iostream>
using namespace std;
class Apple {
public:
    static int nTotalNumber;
    Apple() { nTotalNumber++; }
    ~Apple() { nTotalNumber--; }
    static void PrintTotal() { cout << nTotalNumber << endl; }
};
int Apple::nTotalNumber = 0;
Apple Fun(const Apple& a) {
    a.PrintTotal();
    return a;
}
int main() {
    Apple* p = new Apple[4];
    Fun(p[2]);
    Apple p1, p2;
    Apple::PrintTotal();
    delete[] p;
    p1.PrintTotal();
    system("pause");
    return 0;
}
// 调用系统自带的构造函数不会增加 但后续销毁临时变量会减少
```

## 返回什么才好呢
### 描述

根据以下输出完善程序。

```cpp
#include <iostream>
using namespace std;
class A {
public:
	int val;

	A(int
// 在此处补充你的代码
};
int main()
{
	int m,n;
	A a;
	cout << a.val << endl;
	while(cin >> m >> n) {
		a.GetObj() = m;
		cout << a.val << endl;
		a.GetObj() = A(n);
		cout << a.val<< endl;
	}
	return 0;
}
```

### 输入
多组数据，每组一行，是整数 $m$ 和 $n$ 。

```
2 3
4 5
```

### 输出
先输出一行：

1 2 3

然后对每组数据，输出两行，第一行是 $m$ ，第二行是 $n$ 。

```
123
2
3
4
5 
```

### Solution
根据``main``函数可以看出，此处``A``类型变量``a``在被声明后其``val``成员变量就为``123``，因此其中的转换构造函数应该使用缺省变量，或者写完这个函数再自己声明新的默认构造函数。

随后，发现``a``的``GetObj``成员函数可以修改``val``成员变量的值，那么它必然返回的是一个``A&``型变量（因为前面实现了转换构造函数，因此可以做到``a.GetObj()=m``），但是不能是``int&``型变量，因为有``a.GetObj()=A(n)``这一行。

然后，就是``GetObj``返回对当前``A``对象的引用，这里需要用到``this``指针，可以认为它是指向当前对象的一个指针，因此需要返回``*this``对其解引用，从而拿到当前对象的引用，注意指针和引用很容易混淆。

```cpp
#include <iostream>
using namespace std;
class A {
public:
    int val;

    A(int m = 123) { val = m; }  // 这是构造函数
    A& GetObj() { return *this; }  // 注意这个引用号 生成的不是临时变量而是引用
};
int main() {
    int m, n;
    A a;
    cout << a.val << endl;
    while (cin >> m >> n) {
        a.GetObj() = m;
        cout << a.val << endl;
        a.GetObj() = A(n);
        cout << a.val << endl;
    }
    return 0;
}
```

## Big&Base 封闭类问题
### 描述
根据以下输出完善程序。

```cpp
#include <iostream>
#include <string>
using namespace std;
class Base {
public:
	int k;
	Base(int n):k(n) { }
};
class Big
{
public:
	int v;
	Base b;
// 在此处补充你的代码
};
int main()
{
	int n;
	while(cin >>n) {
		Big a1(n);
		Big a2 = a1;
		cout << a1.v << "," << a1.b.k << endl;
		cout << a2.v << "," << a2.b.k << endl;
	}
}
```

### 输入
多组数据，每组一行，是一个整数。

```
3
4
```

### 输出
对每组数据，输出两行，每行把输入的整数打印两遍

```
3,3
3,3
4,4
4,4
```

### Solution
这里注意到``Big``类有一个``Base``类成员对象，再看``main``函数，得知需要编写一个``Big``类转换构造函数，这个转换构造函数需要将成员变量``v``赋值，同时调用``Base``类的转换构造函数。

```cpp
#include <iostream>
#include <string>
using namespace std;
class Base {
public:
    int k;
    Base(int n) : k(n) {}
};
class Big {
public:
    int v;
    Base b;
    Big(int n) : v(n), b(n) {}  // 构造v和k

    // 在此处补充你的代码
};
int main() {
    int n;
    while (cin >> n) {
        Big a1(n);
        Big a2 = a1;
        cout << a1.v << "," << a1.b.k << endl;
        cout << a2.v << "," << a2.b.k << endl;
    }
}
```

## 奇怪的类复制
### 描述
根据以下输出完善程序。

```cpp
#include <iostream>
using namespace std;
class Sample {
public:
	int v;
// 在此处补充你的代码
};
void PrintAndDouble(Sample o)
{
	cout << o.v;
	cout << endl;
}
int main()
{
	Sample a(5);
	Sample b = a;
	PrintAndDouble(b);
	Sample c = 20;
	PrintAndDouble(c);
	Sample d;
	d = a;
	cout << d.v;
	return 0;
}
```

### 输入

```
None
```
### 输出

```
9
22
5
```

### Solution
首先，这里需要实现一个转换构造函数。

随后，观察样例，发现好像不是一个转换构造函数就能实现的事情，因此考虑实现一个拷贝构造函数。

实现之后，发现``b=a``跟``PrintAndDouble``传入值时会调用一次拷贝构造函数，注意``d=a``不会调用，因为此时``d``已经由默认构造函数（此处由于声明了转换构造函数，需要自己声明）声明过了，因此只会调用默认的赋值运算符而已。

然后，根据给出的输出观察到默认构造函数的行为是将``v``置零，转换构造函数的行为是将``x``赋值给``v``，拷贝构造函数将``x+2``赋值给``v``。

```cpp
#include <iostream>
using namespace std;
class Sample {
public:
    int v;
    Sample() { v = 0; }
    Sample(int x) : v(x) {}
    Sample(const Sample& s) : v(s.v + 2) {}
    // 在此处补充你的代码
};
void PrintAndDouble(Sample o) {
    cout << o.v;
    cout << endl;
}
int main() {
    Sample a(5);
    Sample b = a;
    PrintAndDouble(b);
    Sample c = 20;
    PrintAndDouble(c);
    Sample d;
    d = a;
    cout << d.v;
    system("pause");
    return 0;
}
```