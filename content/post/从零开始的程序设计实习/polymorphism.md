---
title: 从零开始的多态
date: 2025-03-07
categories:
    - 算法
slug: 从零开始的多态
hidden: true
seriesOrder: 4
---
感觉可能会有同学搞混多态这个概念，简洁来说，就是若基类函数使用``虚函数(virtual)``定义，同时派生类中存在同名函数，则``基类指针/引用``根据指向的对象类型调用对应的同名函数。

例如，请看以下代码：

```cpp
class Base {
public:
    virtual void f() { cout << "Base::f\n"; }
};

class Derived : public Base {
public:
    void f() { cout << "Derived::f\n"; }
};

int main() {
    Base* p = new Derived();
    Base* q = new Base();
    p->f();
    q->f();
}
```

此时的输出应该为：

```
Derived::f
Base::f
```

同时，非虚函数则看指针的静态类型，再看以下代码：

```cpp
class A {
private:
    int nVal;

public:
    void Fun() { cout << "A::Fun" << endl; };
    void Do() { cout << "A::Do" << endl; }
};
class B : public A {
public:
    virtual void Do() { cout << "B::Do" << endl; }
};
class C : public B {
public:
    void Do() { cout << "C::Do" << endl; }
    void Fun() { cout << "C::Fun" << endl; }
};
int main() {
    C c;
    B* p = &c;
    p->Fun();
}
```

此时的输出应该为：
```cpp
A::Fun
```

因为``p``只会到``A``类和``B``类中找``Fun``。
## 看上去像多态
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class B { 
	private: 
		int nBVal; 
	public: 
		void Print() 
		{ cout << "nBVal="<< nBVal << endl; } 
		void Fun() 
		{cout << "B::Fun" << endl; } 
		B ( int n ) { nBVal = n;} 
};
// 在此处补充你的代码
int main() { 
	B * pb; D * pd; 
	D d(4); d.Fun(); 
	pb = new B(2); pd = new D(8); 
	pb -> Fun(); pd->Fun(); 
	pb->Print (); pd->Print (); 
	pb = & d; pb->Fun(); 
	pb->Print(); 
	return 0;
}
```
### 输入
```
None
```
### 输出
```
D::Fun
B::Fun
D::Fun
nBVal=2
nBVal=24
nDVal=8
B::Fun
nBVal=12
```
### Solution
标题给了我们一个很好的提示，"看起来是多态"，说明实际上不是多态。

抛开这一点，接着观察原来的代码，需要实现一个类``D``，而``D``类对象``pd``能调用``B``类的函数，则必然``D``类是``B``类的派生类。

需要注意的是，此处由于基类没有``虚函数``定义，因此不是多态，所以派生类也可以实现自己的同名函数``Print``和``Fun``，根据``指针类型``进行判断调用哪个。同时，可以注意到``D``类的转换构造函数中基类的值是传入的三倍。
```cpp
#include <iostream>
using namespace std;
class B {
private:
    int nBVal;

public:
    void Print() { cout << "nBVal=" << nBVal << endl; }
    void Fun() { cout << "B::Fun" << endl; }
    B(int n) { nBVal = n; }
};
class D : public B {
private:
    int nDVal;

public:
    D(int n) : B(3 * n) { nDVal = n; }
    void Fun() { cout << "D::Fun" << endl; }
    void Print() {
        B::Print();
        cout << "nDVal=" << nDVal << endl;
    }
};
int main() {
    B* pb;
    D* pd;
    D d(4);
    d.Fun();
    pb = new B(2);
    pd = new D(8);
    pb->Fun();
    pd->Fun();
    pb->Print();
    pd->Print();
    pb = &d;
    pb->Fun();
    pb->Print();
    system("pause");
    return 0;
}
```

## Fun和Do
### 描述
根据输出完善程序。
```cpp
#include <iostream> 
using namespace std;
class A { 
	private: 
	int nVal; 
	public: 
	void Fun() 
	{ cout << "A::Fun" << endl; }; 
	void Do() 
	{ cout << "A::Do" << endl; } 
}; 
class B:public A { 
	public: 
	virtual void Do() 
	{ cout << "B::Do" << endl;} 
}; 
class C:public B { 
	public: 
	void Do( ) 
	{ cout <<"C::Do"<<endl; } 
	void Fun() 
	{ cout << "C::Fun" << endl; } 
}; 
void Call(
// 在此处补充你的代码
) { 
	p.Fun(); p.Do(); 
} 
int main() { 
	C c; 
	Call( c); 
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
C::Do
```
### Solution
观察给定代码，可以发现``B``类中的``Do``是虚函数，因此指向``B``类的指针或引用根据声明对象的类型调用对应的``Do``函数。

再看输出，发现``Call``中传入一个``C类型变量c``，并且``Fun``对应的是``A::Fun``，``Do``对应的是``C::Do``。

但是，要输出``C::Do``，说明``Call``的参数类型可能是``B类引用/C类对象/C类引用``，但是后面两者输出的都应是``C::Fun``，因此此处输入的应该是``B &p``。

注：若有``B* p=new C();``，要输出``A::Do``，可以使用``p->A::Do();``语句，读者可以想想为什么。

```cpp
#include <iostream>
using namespace std;
class A {
private:
    int nVal;

public:
    void Fun() { cout << "A::Fun" << endl; };
    void Do() { cout << "A::Do" << endl; }
};
class B : public A {
public:
    virtual void Do() { cout << "B::Do" << endl; }
};
class C : public B {
public:
    void Do() { cout << "C::Do" << endl; }
    void Fun() { cout << "C::Fun" << endl; }
};
void Call(B &p) {
    p.Fun();
    p.Do();
}
int main() {
    C c;
    Call(c);
    return 0;
}
```

## 这是什么鬼delete
### 描述
根据输出完善程序。
```cpp
#include <iostream> 
using namespace std;
class A 
{ 
public:
	A() { }
// 在此处补充你的代码
}; 
class B:public A { 
	public: 
	~B() { cout << "destructor B" << endl; } 
}; 
int main() 
{ 
	A * pa; 
	pa = new B; 
	delete pa; 
	return 0;
}
```
### 输入
```
None
```
### 输出
```
destructor B
destructor A
```
### Solution
阅读代码，发现``B``类的析构函数比``A``类的析构函数先调用，这与非虚析构函数的调用顺序相反。
回顾课上讲的，对于虚析构函数的多态情况，先执行``派生类``的析构函数，再执行``基类``的虚构函数，以析构干净，因此可以得出``A``类的析构函数是``虚析构函数``。
```cpp
#include <iostream>
using namespace std;
class A {
public:
    A() {}
    virtual ~A() { cout << "destructor A" << endl; }
};
class B : public A {
public:
    ~B() { cout << "destructor B" << endl; }
};
int main() {
    A* pa;
    pa = new B;
    delete pa;
    system("pause");
    return 0;
}
```

## 怎么又是Fun和Do
### 描述
根据输出完善程序。
```cpp
#include <iostream>
using namespace std;
class A {
	private:
	int nVal;
	public:
	void Fun()
	{ cout << "A::Fun" << endl; };
	virtual void Do()
	{ cout << "A::Do" << endl; }
};
class B:public A {
	public:
	virtual void Do()
	{ cout << "B::Do" << endl;}
};
class C:public B {
	public:
	void Do( )
	{ cout <<"C::Do"<<endl; }
	void Fun()
	{ cout << "C::Fun" << endl; }
};
void Call(
// 在此处补充你的代码
) {
	p->Fun(); p->Do();
}
int main() {
	Call( new A());
	Call( new C());
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
A::Do
A::Fun
C::Do
```
### Solution
首先由主函数的``new``可以明确的是，括号里填的是指针。
 
随后可以观察到，这题与上面不同的点是，``A``的``Do``也是虚函数。

接着再看输出，传入指向``A``类对象指针时，输出``A::Fun``和``A::Do``，这说明输入的是``A*``，因为``B*``跟``A*``之间不存在隐式转换，``C*``跟``A*``也是。

传入指向``C``类对象指针时，输出``A::Fun``和``C::Do``，前者说明输入的是``A*``或者``B*``，否则将会输出``C::Fun``，后者则说明不了什么。

综上，答案应为``A* p``。
```cpp
#include <iostream>
using namespace std;
class A {
private:
    int nVal;

public:
    void Fun() { cout << "A::Fun" << endl; };
    virtual void Do() { cout << "A::Do" << endl; }
};
class B : public A {
public:
    virtual void Do() { cout << "B::Do" << endl; }
};
class C : public B {
public:
    void Do() { cout << "C::Do" << endl; }
    void Fun() { cout << "C::Fun" << endl; }
};
void Call(A *p) {
    p->Fun();
    p->Do();
}
int main() {
    Call(new A());
    Call(new C());
    system("pause");
    return 0;
}
```