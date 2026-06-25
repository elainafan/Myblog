---
title: 从零开始的上机(5)
date: 2025-04-13
categories:
    - 程序设计实习
slug: 从零开始的上机5
hidden: true
seriesOrder: 13
---
本次上机涉及内容：类与对象、运算符重载、继承、多态
## Hero和Priest
### 描述
根据输出完善程序。

```cpp
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
观察代码，发现``Priest``类由``Hero``类派生，从而这里需要用到多态的相关知识。

再看主函数，首先调用``h.defense()``，再创建了一个指向``Priest``对象的``Hero*``指针，那么此时想必要使用多态了。

观察输出，发现``Attack``调用的是``Hero``的，而``Defense``则调用的是``Priest``的，即``Defense``是虚函数/多态，而``Attack``不是。

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

## 统计动物数量
### 描述
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
void print() {
	cout << Animal::number << " animals in the zoo, " << Dog::number << " of them are dogs, " << Cat::number << " of them are cats" << endl;
}

int main() {
	print();
	Dog d1, d2;
	Cat c1;
	print();
	Dog* d3 = new Dog();
	Animal* c2 = new Cat;
	Cat* c3 = new Cat;
	print();
	delete c3;
	delete c2;
	delete d3;
	print();
}
```
### 输入
```
无
```
### 输出
```
0 animals in the zoo, 0 of them are dogs, 0 of them are cats
3 animals in the zoo, 2 of them are dogs, 1 of them are cats
6 animals in the zoo, 3 of them are dogs, 3 of them are cats
3 animals in the zoo, 2 of them are dogs, 1 of them are cats
```
### Solution
观察代码，发现这里的``number``应该是``Animal``类、
``Dog``类和``Cat``类的某个静态成员变量，应该是来统计当前动物的数量的。

再看输出，可以发现每次创建一个对象时，总动物数量和对应动物的数量都需要加一，这应该写在构造函数里。

然后这里需要注意的是，需要将基类的析构函数写成虚函数形式，这样，在delete派生类对象的时候才会先执行派生类析构函数，再执行基类的析构函数，析构得干净。

还有一点要注意的是，由于几个``number``变量要初始化为0，因此需要在外面声明一下，这里的格式需要注意，可能忘了。

```cpp
#include <iostream>
using namespace std;
class Animal {
public:
    static int number;
    Animal() { number += 1; }
    virtual ~Animal() { number--; }
};
class Dog : public Animal {
public:
    static int number;
    Dog() { number += 1; }
    ~Dog() { number--; }
};
class Cat : public Animal {
public:
    static int number;
    Cat() { number += 1; }
    ~Cat() { number--; }
};
int Animal::number = 0;
int Dog::number = 0;
int Cat::number = 0;
// 在此处补充你的代码
void print() {
    cout << Animal::number << " animals in the zoo, " << Dog::number << " of them are dogs, " << Cat::number << " of them are cats" << endl;
}

int main() {
    print();
    Dog d1, d2;
    Cat c1;
    print();
    Dog* d3 = new Dog();
    Animal* c2 = new Cat;
    Cat* c3 = new Cat;
    print();
    delete c3;
    delete c2;
    delete d3;
    system("pause");
    print();
}
```

## 还是Fun和Do
### 描述
根据输出完善代码

```cpp
#include <iostream> 
using namespace std;

class A { 
	public: 
		virtual void Fun() { 
			cout << "A::Fun" << endl; 
		}; 
		virtual void Do() { 
			cout << "A::Do" << endl; 
		} 
};
// 在此处补充你的代码
{ 
	p.Fun(); 
	p.Do(); 
} 

void Call2(B p) {
	p.Fun();
	p.Do();
}



int main() { 
	C c;
	B b;
	Call1(b);
	Call1(c); 
	Call2(c);
	return 0;
}
```

### 输入

```
None
```

### 输出

```
A::Fun
B::Do
C::Fun
C::Do
A::Fun
B::Do
```

### Solution
观察代码，发现是要完善``B``类、``C``类和``Call1``函数的定义。

从基类``A``的定义看出，这题是很明显的虚函数/多态题目。

再观察输出，可以发现传进``B``类对象的却输出了``A::Fun``，因此``B``应该没有自己的``Fun``函数，但是有自己的``Do``函数。

往下看，``Call1(c)``传入一个``C``类对象，输出``C::Fun``和``C::Do``，由于``Call1``能传进``B``类对象，因此参数类型必然不是``C&``或``C``，于是得出结论：传入的是``B&``类型，虚函数调用``C``中对应函数。

最后，再用``Call2(c)``验证刚才的猜想就行~

```cpp
#include <iostream>
using namespace std;

class A {
public:
    virtual void Fun() { cout << "A::Fun" << endl; }
    virtual void Do() { cout << "A::Do" << endl; }
};
class B : public A {
public:
    void Do() { cout << "B::Do" << endl; }
};
class C : public B {
public:
    void Fun() { cout << "C::Fun" << endl; }
    void Do() { cout << "C::Do" << endl; }
};
void Call1(B &p)
// 在此处补充你的代码
{
    p.Fun();
    p.Do();
}

void Call2(B p) {
    p.Fun();
    p.Do();
}

int main() {
    C c;
    B b;
    Call1(b);
    Call1(c);
    Call2(c);
    system("pause");
    return 0;
}
```

## 多态
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;

class Base {
public:
   virtual Base& fun() { cout << "base fun" << endl; return *this; }
   virtual Base& foo() { cout << "base foo" << endl; return *this; }
};

class Derived: public Base {
public:
   Base& fun() { cout << "derived fun" << endl; return *this; }
   Base& foo() { cout << "derived foo" << endl; return *this; }
};

Base& foo();
Base& fun();
// 在此处补充你的代码
int main() {
   foo().fun().foo();
   fun().foo().fun();
   return 0;
}
```
### 输入
```
None
```
### 输出
```
derived foo
derived fun
derived foo
base fun
base foo
base fun
```
### Solution
首先观察到题目中有虚函数，因此可能发生多态。

这里比较少见的是``Base& foo();``这个语句，它是用来先声明这个函数的定义的，后续需要再次实现函数的具体内容。

于是，题目的要求就变成实现``foo``和``fun``函数了，它们都返回一个``Base&``对象。

要返回对象引用，自然需要在函数中声明一个，这道题最需要注意的点是，声明的这个对象必须要是``静态对象``，为什么？

因为这个静态对象只能创建一次，并且在函数结束后不会被销毁，否则原来的临时变量会被销毁，根本没有引用这一说。

随后再观察输出，便能写出代码了，此处为了简化作了压行。
```cpp
#include <iostream>
using namespace std;

class Base {
public:
   virtual Base& fun() { cout << "base fun" << endl; return *this; }
   virtual Base& foo() { cout << "base foo" << endl; return *this; }
};

class Derived: public Base {
public:
   Base& fun() { cout << "derived fun" << endl; return *this; }
   Base& foo() { cout << "derived foo" << endl; return *this; }
};

Base& foo();
Base& fun();
Base& foo(){
   static Derived d;
   return d.foo();
}
Base& fun(){
   static Base b;
   return b.fun();
}
// 在此处补充你的代码
int main() {
   foo().fun().foo();
   fun().foo().fun();
   system("pause");
   return 0;
}
```

## 又双叒叕是Fun和Do！
### 描述
根据输出完善代码。

```cpp
#include <iostream>
using namespace std;

class A{
public:
    int n;
    A(int m):n(m) {}
    virtual void Do(){
        cout <<"A::Do()" << n << endl;
        Fun();
    }
// 在此处补充你的代码
void CallFun(){
        Fun();
    }
};

class B: public A{
public:
    B(int n):A(n){ }
    void Do(){
        cout <<"B::Do()" << ++n << endl;
        CallFun();
    }
    void Fun(){
        cout <<"B::Fun()" << ++n << endl;
    }
};

int main(){
    B bb(1);
    A aa = bb;
    aa.Do();
    A *bp = &bb;
    bp->Do();
    return 0;
}
```

### 输入

```
None
```

### 输出

```
A::Do()1
A::Fun()2
B::Do()2
B::Fun()3
```

### Solution
观察代码，可以发现需要补充的是``A``的``Fun``部分，而且``B``的``Do``函数中，有一个``CallFun``的调用，``A``的``Do``中，有一个``Fun``的调用。

于是，根据``B``中``Fun``的写法，抄一遍到``A``中来即可。

再往下看，``A* bp=&bb``，这是非常典型的多态写法，由输出可以看出，它调用的是``B``的``Do``函数，却输出的是``B::Fun``，因此``A``中的``Fun``应该是虚函数。

```cpp
#include <iostream>
using namespace std;

class A {
public:
    int n;
    A(int m) : n(m) {}
    virtual void Do() {
        cout << "A::Do()" << n << endl;
        Fun();
    }
    virtual void Fun() { cout << "A::Fun()" << ++n << endl; }
    // 在此处补充你的代码
    void CallFun() { Fun(); }
};

class B : public A {
public:
    B(int n) : A(n) {}
    void Do() {
        cout << "B::Do()" << ++n << endl;
        CallFun();
    }
    void Fun() { cout << "B::Fun()" << ++n << endl; }
};

int main() {
    B bb(1);
    A aa = bb;
    aa.Do();
    A *bp = &bb;
    bp->Do();
    system("pause");
    return 0;
}
```

## 变来变去的数
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;

class myobject {
public:
// 在此处补充你的代码
};

class producer : public myobject {
public:
	virtual void work() {
		counter = counter + 5;
		print_avaliable();
	}
};

int myobject::counter = 0;

int main(){
	producer *pro = new producer();
	myobject *con = new myobject();
	pro->work(); pro->work(); cout << endl;
	con->work(); con->work(); con->work(); cout << endl;
	pro->work(); cout << endl;
	con->work(); con->work(); cout << endl;
}
```
### 输入
```
None
```
### 输出
```
5 10
6 2 2
7
3 3
```
### Solution
首先，观察到``producer``类中有一个``print_avaiable``函数，因此需要在``myobject``内实现。

接着，观察样例，发现``myobject``的``work``有以下规律：

$$
f(x)=
\begin{cases}
x-4, \quad x \geq 4 \\\\
x, \quad 0 \leq x \leq 3 \\\\
\end{cases}$$

于是完善代码即可。

```cpp
#include <iostream>
using namespace std;

class myobject {
public:
    static int counter;
    void work() {
        if (counter >= 4) counter -= 4;
        cout << counter << ' ';
    }
    void print_avaliable() { cout << counter << ' '; }
    // 在此处补充你的代码
};

class producer : public myobject {
public:
    virtual void work() {
        counter = counter + 5;
        print_avaliable();
    }
};

int myobject::counter = 0;

int main() {
    producer *pro = new producer();
    myobject *con = new myobject();
    pro->work();
    pro->work();
    cout << endl;
    con->work();
    con->work();
    con->work();
    cout << endl;
    pro->work();
    cout << endl;
    con->work();
    con->work();
    cout << endl;
    system("pause");
    return 0;
}
```
## MyClass
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;
class CMyClassA {
	int val;
public:
	CMyClassA(int);
	void virtual print();
};
CMyClassA::CMyClassA(int arg) {
	val = arg;
	printf("A:%d\n", val);
}
void CMyClassA::print() {
	printf("%d\n", val);
	return;
}
// 在此处补充你的代码
int main(int argc, char** argv) {
	CMyClassA a(3), *ptr;
	CMyClassB b(5);
	ptr = &a; ptr->print();
	a = b;
	a.print();
	ptr = &b; ptr->print();
	return 0;
}
```
### 输入
```
None
```

### 输出
```
A:3
A:15
B:5
3
15
5
```
### Solution
这道题，由``a=b``，很容易可以看出``CMyClassB``应该是继承自``CMyCalss``类的。

再观察输出，``a.print()``输出``A:15``，代表``B``类初始化时用传入值的三倍，顺便初始化了``A``类构造函数，注意这里的写法，可能已经忘了。同时``B``类和``A``类的构造函数都需要输出当前值，而先执行的是基类构造函数，因此先输出``A::15``。

接下来完善``print``函数，并用剩下的样例验证即可。

```cpp
#include <iostream>
using namespace std;
class CMyClassA {
    int val;

public:
    CMyClassA(int);
    void virtual print();
};
CMyClassA::CMyClassA(int arg) {
    val = arg;
    printf("A:%d\n", val);
}
void CMyClassA::print() {
    printf("%d\n", val);
    return;
}
class CMyClassB : public CMyClassA {
public:
    int val;
    CMyClassB(int x) : CMyClassA(3 * x) {
        val = x;
        printf("B:%d\n", val);
    }
    void print() { printf("%d\n", val); }
};
// 在此处补充你的代码
int main(int argc, char** argv) {
    CMyClassA a(3), *ptr;
    CMyClassB b(5);
    ptr = &a;
    ptr->print();
    a = b;
    a.print();
    ptr = &b;
    ptr->print();
    system("pause");
    return 0;
}
```

## 输出指定结果二
### 描述
根据输出完善程序。

```cpp
#include <iostream>
#include <map>
using namespace std;
// 在此处补充你的代码
int A::count = 0;
void func(B b) {  }
int main()
{
	A a1(5),a2;
	cout << A::count << endl;
	B b1(4);
	cout << A::count << endl;
	func(b1);
	cout << A::count << endl;
	A * pa = new B(4);
	cout << A::count << endl;
	delete pa;
	cout << A::count << endl;
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
3
B::destructor
A::destructor
3
4
B::destructor
A::destructor
3
B::destructor
A::destructor
A::destructor
A::destructor
```

### Solution
观察代码，很容易发现``A``类有一个静态成员变量``count``，同时它有默认构造函数和转换构造函数，并且每次新建变量``count``会加一。

再往下看，发现``B``新建时``A``也增加了，因此``B``是``A``的派生类，而``count``用于统计的是``A``的数量。

再往下看，``func``传入一个``B``型变量，注意此时编译器的行为是，将当前``B``型变量通过``拷贝构造函数``拷贝出一个新的``B``型变量并传入，因此结合``count``的含义，需要实现``A``类的拷贝构造函数。

最后，需要实现两者的析构函数以打印所需，注意到``B``类先于``A``类析构，因此``A``类析构函数应该是虚析构函数。

```cpp
#include <iostream>
#include <map>
using namespace std;
class A {
public:
    static int count;
    A(int x) { count++; }
    A() { count++; }
    A(const A& other) { count++; }
    virtual ~A() {
        cout << "A::destructor" << endl;
        count--;
    }
};
class B : public A {
public:
    B(int x) {}
    ~B() { cout << "B::destructor" << endl; }
};
// 在此处补充你的代码
int A::count = 0;
void func(B b) {}
int main() {
    A a1(5), a2;
    cout << A::count << endl;
    B b1(4);
    cout << A::count << endl;
    func(b1);
    cout << A::count << endl;
    A* pa = new B(4);
    cout << A::count << endl;
    delete pa;
    cout << A::count << endl;
    system("pause");
    return 0;
}
```

## 构造与析构
### 描述
根据输出完善程序。

```cpp
#include<cstdio>
#include<iostream>
#include<algorithm>
#include<cstring>
using namespace std;
// 在此处补充你的代码
int main(){
	int n;
	cin >> n;
	for (int i = 1; i<=n; i++) {
		int x;
		cin >> x;
		if (x == 0) {
			A *a = new A();
			delete a;
		}else {
			A *a = new B();
			delete a;
		}
	}
	return 0;	
}
```

### 输入

```
3
1 0 1
```

### 输出

```
New A
New B
Delete B
Delete A
New A 
Delete A
New A
New B
Delete B
Delete A
```

### Solution
观察主函数代码，发现需要实现``A``类和``B``类，并且由``A* a=new B()``得知，``B``是``A``的派生类。

接着，观察输出，发现``A``先于``B``被构造，并且``B``先于``A``被析构，因此``A``中析构函数为虚析构函数，再根据输出填入打印语句即可。

```cpp
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <iostream>

using namespace std;
class A {
public:
    A() { cout << "New A" << endl; }
    virtual ~A() { cout << "Delete A" << endl; }
};
class B : public A {
public:
    B() { cout << "New B" << endl; }
    ~B() { cout << "Delete B" << endl; }
};
// 在此处补充你的代码
int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        if (x == 0) {
            A *a = new A();
            delete a;
        } else {
            A *a = new B();
            delete a;
        }
    }
    system("pause");
    return 0;
}
```

## 卖肉付牛肉
### 描述
根据输出完善程序。

```cpp
#include<bits/stdc++.h>
using namespace std;

class Food {
public:
// 在此处补充你的代码
};

class Meat : public Food {
public:
	void Buy() { cout << "Buy Meat" << endl; }
	virtual void Pay() { cout << "Pay Meat" << endl; }
};

class Beef : public Meat {
public:
	void Buy() { cout << "Buy Beef" << endl; }
	void Pay() { cout << "Pay Beef" << endl; }
};
int main() {
	Beef bf;
	Meat* pmt = &bf;
	Food* pfd = &bf;

	pfd->Buy();
	pfd->Pay();
	pmt->Buy();
	pmt->Pay();
	return 0;
}
```

### 输入

```
None
```

### 输出

```
Buy Nothing
Pay Beef
Buy Meat
Pay Beef
```

### Solution
观察代码结构，发现主函数有一个``Meat*->Beef``，还有一个``Food*->Beef``。

先调用``Food*->Beef``的``Buy``，它输出了``Buy Nothing``，对比发现这应该是``Food``中的``Buy``函数，并且由定义看出，它不是虚函数。

再看``Food*->Beef``的``Pay``函数，它调用的是``Beef->Pay``，因此``Food``类的这个函数应该是虚函数，至于它应该输出什么，那不重要了。

接下来只需要用剩下的样例验证即可。

```cpp
#include <bits/stdc++.h>
using namespace std;

class Food {
public:
    void Buy() { cout << "Buy Nothing" << endl; }
    virtual void Pay() {}
    // 在此处补充你的代码
};

class Meat : public Food {
public:
    void Buy() { cout << "Buy Meat" << endl; }
    virtual void Pay() { cout << "Pay Meat" << endl; }
};

class Beef : public Meat {
public:
    void Buy() { cout << "Buy Beef" << endl; }
    void Pay() { cout << "Pay Beef" << endl; }
};
int main() {
    Beef bf;
    Meat* pmt = &bf;
    Food* pfd = &bf;

    pfd->Buy();
    pfd->Pay();
    pmt->Buy();
    pmt->Pay();
    system("pause");
    return 0;
}
```